import itertools
from database.db import get_connection


def recommend_vehicle(weight, length, width, height):
    """
    Kept for backwards compatibility with single-shipment workloads.
    """
    shipments = [{"id": "S1", "weight": weight, "length": length, "width": width, "height": height}]
    result = consolidate_shipments(shipments)
    if "error" in result:
        return {"error": result["error"]}
    
    # Map back to original single response format using the first processed item
    if result["loaded_shipments"]:
        return result["raw_original_metrics"]
    elif result["rejected_shipments"]:
        return {"error": f"Shipment rejected: {result['rejected_shipments'][0]['reasons'][0]}"}
    return {"error": "No suitable vehicle found for the given shipment profile."}


def get_best_vehicle(total_weight, max_length, max_width, max_height, conn):
    """
    Helper function to dynamically select the optimal baseline vehicle 
    capable of handling the entire aggregated consignment footprint.
    """
    return conn.execute(
        """
        SELECT *
        FROM vehicles
        WHERE
            Max_Weight_MT >= ?
            AND (Length_mm >= ? OR ODC_Allowed = 'Yes')
            AND (Width_mm >= ? OR ODC_Allowed = 'Yes')
            AND (Height_mm >= ? OR ODC_Allowed = 'Yes')
        ORDER BY Max_Weight_MT ASC
        LIMIT 1
        """,
        (total_weight, max_length, max_width, max_height)
    ).fetchone()


def consolidate_shipments(shipments: list) -> dict:
    """
    DYNAMIC LOAD CONSOLIDATION & VEHICLE RE-SELECTION ENGINE
    Continuously updates the optimal baseline asset based on the total consolidated footprint
    instead of lock-in on the primary item, matching standard TMS architectures.
    """
    if not shipments:
        return {"error": "No shipments provided for consolidation."}

    conn = get_connection()

    try:
        # =====================================================
        # AGGREGATED METRICS & DYNAMIC TARGETING (STEPS 2 & 3)
        # =====================================================
        total_weight = sum(s["weight"] for s in shipments)
        max_length = max(s["length"] for s in shipments)
        max_width = max(s["width"] for s in shipments)
        max_height = max(s["height"] for s in shipments)

        # Baseline check using initial first shipment to see if we ever change mid-run
        baseline_vehicle = conn.execute(
            """
            SELECT * FROM vehicles 
            WHERE ? BETWEEN Min_Weight_MT AND Max_Weight_MT 
            ORDER BY Max_Weight_MT ASC LIMIT 1
            """, 
            (shipments[0]["weight"],)
        ).fetchone()

        active_vehicle = get_best_vehicle(total_weight, max_length, max_width, max_height, conn)

        # Fallback to absolute best match if total weight configuration is too restrictive
        if not active_vehicle:
            active_vehicle = baseline_vehicle

        if not active_vehicle:
            return {"error": "No suitable vehicle configuration found for the consolidated shipment metrics."}

        # Determine if a systemic vehicle upgrade occurred relative to the initial item baseline
        vehicle_upgraded = False
        upgrade_reason = ""
        previous_vehicle = baseline_vehicle["Vehicle_Name"] if baseline_vehicle else None
        
        if baseline_vehicle and active_vehicle["Vehicle_Name"] != baseline_vehicle["Vehicle_Name"]:
            vehicle_upgraded = True
            upgrade_reason = f"Total consolidated weight and spatial footprint exceeded baseline capacity ({baseline_vehicle['Vehicle_Name']})."

        # Track cumulative capacity states
        current_weight = 0.0
        loaded_shipments = []
        rejected_shipments = []

        # Advanced Spatial Footprint Tracking
        current_row_length_used = 0
        max_row_width_used = 0
        total_length_consumed = 0
        global_odc_required = False
        global_vehicle_suitable = True
        
        alternative_vehicle = None
        alternative_category = None
        alternative_axles = None

        # =====================================================
        # CONSOLIDATION LOOP
        # =====================================================
        for item in shipments:
            s_id = item.get("id", f"S{len(loaded_shipments) + len(rejected_shipments) + 1}")
            s_weight = item["weight"]
            s_len = item["length"]
            s_wid = item["width"]
            s_hgt = item["height"]
            
            reasons = []

            # Evaluate ODC requirements against the dynamically active vehicle dimensions
            odc_required = (
                s_len > active_vehicle["Length_mm"]
                or s_wid > active_vehicle["Width_mm"]
                or s_hgt > active_vehicle["Height_mm"]
            )

            # Fallback Hydraulic Escalation Logic if the globally selected vehicle still lacks structural clearance
            if odc_required and active_vehicle["ODC_Allowed"] == "No":
                alternative = get_best_vehicle(current_weight + s_weight, s_len, s_wid, s_hgt, conn)
                
                # Filter specifically for an ODC asset by weight if normal search limits fail
                if not alternative or alternative["ODC_Allowed"] == "No":
                    alternative = conn.execute(
                        """
                        SELECT * FROM vehicles
                        WHERE ODC_Allowed='Yes' AND Max_Weight_MT >= ?
                        ORDER BY Max_Weight_MT ASC LIMIT 1
                        """, (current_weight + s_weight,)
                    ).fetchone()

                if alternative:
                    previous_vehicle = active_vehicle["Vehicle_Name"]
                    active_vehicle = alternative
                    global_odc_required = True
                    vehicle_upgraded = True
                    upgrade_reason = "Dynamic escalation to alternate heavy-haul asset due to ODC spatial constraints."
                    
                    alternative_vehicle = alternative["Vehicle_Name"]
                    alternative_category = alternative["Category"]
                    alternative_axles = alternative["Axles"]
                    odc_required = False
                else:
                    reasons.append("ODC asset escalation fallback failed. No alternate asset fits dimensions.")

            # --- Rule 1: Weight Capacity Validation ---
            if current_weight + s_weight > active_vehicle["Max_Weight_MT"]:
                exceeded_by = round((current_weight + s_weight) - active_vehicle["Max_Weight_MT"], 2)
                reasons.append(
                    f"Weight capacity exceeded by {exceeded_by} MT. (Remaining: {round(active_vehicle['Max_Weight_MT'] - current_weight, 2)} MT, Required: {s_weight} MT)"
                )

            # --- Rule 2: Advanced Geometric Placement (Orientation, Width & Length) ---
            orientations = [(s_len, s_wid), (s_wid, s_len)]
            fits_spatially = False
            best_placement = None 

            for l_opt, w_opt in orientations:
                if w_opt > active_vehicle["Width_mm"] and active_vehicle["ODC_Allowed"] == "No":
                    continue 
                
                # Placement Strategy A: Pack side-by-side in current longitudinal segment
                if (max_row_width_used + w_opt <= active_vehicle["Width_mm"]) and (max_row_width_used > 0):
                    needed_extension = max(0, l_opt - current_row_length_used)
                    if total_length_consumed + needed_extension <= active_vehicle["Length_mm"] or active_vehicle["ODC_Allowed"] == "Yes":
                        fits_spatially = True
                        best_placement = (needed_extension, max(current_row_length_used, l_opt), max_row_width_used + w_opt)
                        break
                
                # Placement Strategy B: Place sequentially down the deck (Start a new row)
                if total_length_consumed + l_opt <= active_vehicle["Length_mm"] or active_vehicle["ODC_Allowed"] == "Yes":
                    fits_spatially = True
                    best_placement = (l_opt, l_opt, w_opt)
                    break

            if not fits_spatially and not reasons:
                reasons.append(f"Spatial placement failure. Deck footprint insufficient for dimensions ({s_len}mm x {s_wid}mm).")

            # --- Decision Gate ---
            if reasons:
                rejected_shipments.append({
                    "id": s_id, "weight": s_weight, "length": s_len, "width": s_wid, "height": s_hgt, "reasons": reasons
                })
            else:
                current_weight += s_weight
                added_len, current_row_length_used, max_row_width_used = best_placement
                total_length_consumed += added_len
                if odc_required or active_vehicle["ODC_Allowed"] == "Yes":
                    global_odc_required = True

                loaded_shipments.append({
                    "id": s_id, "weight": s_weight, "length": s_len, "width": s_wid, "height": s_hgt, "status": "Loaded"
                })

        # =====================================================
        # CAPACITY METRICS GENERATION
        # =====================================================
        vehicle_volume_capacity = round(
            (active_vehicle["Length_mm"] * active_vehicle["Width_mm"] * active_vehicle["Height_mm"]) / 1000000000, 2
        )
        
        final_weight_pct = round((current_weight / active_vehicle["Max_Weight_MT"]) * 100, 1) if active_vehicle["Max_Weight_MT"] > 0 else 0
        final_deck_pct = round((total_length_consumed / active_vehicle["Length_mm"]) * 100, 1) if active_vehicle["Length_mm"] > 0 else 0
        
        final_weight_pct_capped = min(final_weight_pct, 100.0)
        final_deck_pct_capped = min(final_deck_pct, 100.0)

        weight_bar_ticks = int(final_weight_pct_capped // 5)
        deck_bar_ticks = int(final_deck_pct_capped // 5)
        
        weight_visual_bar = f"[{'█' * weight_bar_ticks}{'░' * (20 - weight_bar_ticks)}] {final_weight_pct}%"
        deck_visual_bar = f"[{'█' * deck_bar_ticks}{'░' * (20 - deck_bar_ticks)}] {final_deck_pct}%"

        last_processed_original_metrics = {
            "vehicle": active_vehicle["Vehicle_Name"],
            "category": active_vehicle["Category"],
            "axles": active_vehicle["Axles"],
            "min_weight": active_vehicle["Min_Weight_MT"],
            "max_weight": active_vehicle["Max_Weight_MT"],
            "length_capacity": active_vehicle["Length_mm"],
            "width_capacity": active_vehicle["Width_mm"],
            "height_capacity": active_vehicle["Height_mm"],
            "vehicle_volume_capacity": vehicle_volume_capacity,
            "odc_allowed": active_vehicle["ODC_Allowed"],
            "odc_required": global_odc_required,
            "vehicle_suitable": global_vehicle_suitable,
            "utilization_percent": final_weight_pct_capped,
            "alternative_vehicle": alternative_vehicle,
            "alternative_category": alternative_category,
            "alternative_axles": alternative_axles
        }

        return {
            "vehicle_upgraded": vehicle_upgraded,
            "previous_vehicle": previous_vehicle,
            "current_vehicle": active_vehicle["Vehicle_Name"],
            "upgrade_reason": upgrade_reason,
            "load_plan_summary": {
                "vehicle": active_vehicle["Vehicle_Name"],
                "category": active_vehicle["Category"],
                "axles": active_vehicle["Axles"],
                "total_weight_loaded_mt": round(current_weight, 2),
                "remaining_weight_capacity_mt": round(max(0.0, active_vehicle["Max_Weight_MT"] - current_weight), 2),
                "total_length_used_mm": total_length_consumed,
                "remaining_length_capacity_mm": max(0, active_vehicle["Length_mm"] - total_length_consumed),
                "weight_utilization_percent": final_weight_pct_capped,
                "deck_utilization_percent": final_deck_pct_capped,
                "odc_required": global_odc_required,
                "vehicle_suitable": global_vehicle_suitable
            },
            "visual_capacity_meters": {
                "weight_utilization_meter": weight_visual_bar,
                "deck_utilization_meter": deck_visual_bar
            },
            "loaded_shipments": loaded_shipments,
            "rejected_shipments": rejected_shipments,
            "raw_original_metrics": last_processed_original_metrics
        }

    finally:
        conn.close()


def evaluate_single_shipment_addition(current_load_plan: dict, next_shipment: dict, staged_shipments: list = None) -> dict:
    """
    Step 4 Validation Bridge.
    Runs a theoretical consolidation simulation incorporating the next layout element 
    to see if a macro fleet reassignment/upgrade flag shifts parameters.
    """
    if staged_shipments is None:
        staged_shipments = current_load_plan.get("loaded_shipments", [])

    # Simulate updated load profile setup
    temp_shipments = staged_shipments + [next_shipment]
    simulated_result = consolidate_shipments(temp_shipments)

    if "error" in simulated_result:
        return {"can_fit": False, "status": "cannot_fit", "reasons": [simulated_result["error"]]}

    # Check if a bigger capacity upgrade trigger occurred
    if simulated_result.get("vehicle_upgraded", False):
        return {
            "status": "can_fit_with_upgrade",
            "can_fit": True,
            "vehicle_changed": True,
            "old_vehicle": simulated_result["previous_vehicle"],
            "new_vehicle": simulated_result["current_vehicle"],
            "upgrade_reason": simulated_result["upgrade_reason"],
            "simulated_plan": simulated_result
        }

    # Handle explicit placement drop validations safely
    if any(r["id"] == next_shipment.get("id") for r in simulated_result.get("rejected_shipments", [])):
        rej_meta = next(r for r in simulated_result["rejected_shipments"] if r["id"] == next_shipment.get("id"))
        return {
            "status": "cannot_fit",
            "can_fit": False,
            "reasons": rej_meta["reasons"],
            "best_reason": rej_meta["reasons"][0]
        }

    return {"status": "can_fit", "can_fit": True, "vehicle_changed": False, "reasons": []}


def generate_comprehensive_load_profile(current_load_plan: dict) -> dict:
    """
    Transforms structural consolidation outputs into an enhanced metrics mapping dashboard.
    """
    raw_metrics = current_load_plan.get("raw_original_metrics", {})
    loaded = current_load_plan.get("loaded_shipments", [])
    
    v_max_weight = raw_metrics.get("max_weight", 0)
    v_length = raw_metrics.get("length_capacity", 0)
    v_width = raw_metrics.get("width_capacity", 0)
    v_height = raw_metrics.get("height_capacity", 0)
    
    weight_used = sum(s["weight"] for s in loaded)
    length_used = current_load_plan["load_plan_summary"]["total_length_used_mm"]
    width_used = max([s["width"] for s in loaded] + [0])
    height_used = max([s["height"] for s in loaded] + [0])

    utilization = current_load_plan["load_plan_summary"]["weight_utilization_percent"]

    def make_bar(used, max_val):
        pct = min(100, round((used / max_val) * 100)) if max_val > 0 else 0
        ticks = int(pct // 5)
        return f"{'█' * ticks}{'░' * (20 - ticks)}"

    return {
        "vehicle": current_load_plan["load_plan_summary"]["vehicle"],
        "vehicle_upgraded": current_load_plan.get("vehicle_upgraded", False),
        "previous_vehicle": current_load_plan.get("previous_vehicle"),
        "upgrade_reason": current_load_plan.get("upgrade_reason"),
        "loaded_shipments": loaded,
        "rejected_shipments": current_load_plan.get("rejected_shipments", []),
        "weight_used": round(weight_used, 2),
        "weight_left": round(max(0.0, v_max_weight - weight_used), 2),
        "deck_used": length_used,
        "deck_left": max(0, v_length - length_used),
        "width_used": width_used,
        "width_left": max(0, v_width - width_used),
        "height_used": height_used,
        "height_left": max(0, v_height - height_used),
        "utilization": utilization,
        "visual_metrics": {
            "weight": {"bar": make_bar(weight_used, v_max_weight), "pct": min(100, round((weight_used / v_max_weight) * 100)) if v_max_weight > 0 else 0},
            "length": {"bar": make_bar(length_used, v_length), "pct": min(100, round((length_used / v_length) * 100)) if v_length > 0 else 0},
            "width": {"bar": make_bar(width_used, v_width), "pct": min(100, round((width_used / v_width) * 100)) if v_width > 0 else 0},
            "height": {"bar": make_bar(height_used, v_height), "pct": min(100, round((height_used / v_height) * 100)) if v_height > 0 else 0},
        }
    }


def ai_optimize_load_plan(shipments: list) -> dict:
    """
    AI LOAD OPTIMIZER (Combinatorial Permutations & Knapsack Engine)
    Evaluates item combinations to maximize global weight, length, and spatial utilization metrics.
    """
    if not shipments:
        return {"error": "No shipments provided for optimization."}

    best_plan = None
    max_score = -1

    for r in range(1, len(shipments) + 1):
        for subset in itertools.combinations(shipments, r):
            for permutation in itertools.permutations(subset):
                current_plan = consolidate_shipments(list(permutation))
                if "error" in current_plan:
                    continue
                
                summary = current_plan["load_plan_summary"]
                score = (
                    (summary["weight_utilization_percent"] * 2.0) + 
                    (summary["deck_utilization_percent"] * 1.0) - 
                    (len(current_plan["rejected_shipments"]) * 15.0)
                )

                if score > max_score:
                    max_score = score
                    best_plan = current_plan

    if not best_plan:
        return consolidate_shipments(shipments)

    loaded_ids = {s["id"] for s in best_plan["loaded_shipments"]}
    for original_item in shipments:
        if original_item["id"] not in loaded_ids and not any(r["id"] == original_item["id"] for r in best_plan["rejected_shipments"]):
            best_plan["rejected_shipments"].append({
                **original_item,
                "reasons": ["Dropped by optimization engine to protect system volumetric utilization threshold."]
            })

    return best_plan
