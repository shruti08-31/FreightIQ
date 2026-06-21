from ai.gemini_service import model


def recommend_packaging(
    weight,
    length,
    width,
    height,
    fragile
):

    recommendations = []

    # =====================================
    # CONVERT MM → M
    # =====================================

    length_m = length / 1000
    width_m = width / 1000
    height_m = height / 1000

    # =====================================
    # TRUE VOLUME
    # =====================================

    volume = round(
        length_m *
        width_m *
        height_m,
        2
    )

    # =====================================
    # TRUE SURFACE AREA
    # =====================================

    surface_area = round(
        2 * (
            (length_m * width_m)
            + (width_m * height_m)
            + (length_m * height_m)
        ),
        2
    )

    # =====================================
    # OVERSIZED CHECK
    # =====================================

    oversized = (
        length > 6000
        or width > 3000
        or height > 3000
    )

    # =====================================
    # IMPROVED PACKAGING LOGIC
    # =====================================

    if weight <= 500 and volume <= 2:

        packaging_type = "Petty Wooden Packaging"

        packaging_category = "Light Duty"

        recommendations.append(
            "Suitable for small and light consignments."
        )

        recommendations.append(
            "Standard wooden packaging recommended."
        )

    elif weight <= 5000 and volume <= 20:

        packaging_type = "Wooden Box Packaging"

        packaging_category = "Medium Duty"

        recommendations.append(
            "Wooden box packaging recommended."
        )

        recommendations.append(
            "Additional structural support recommended."
        )

        recommendations.append(
            "Forklift handling provisions recommended."
        )

    else:

        packaging_type = "Steel Crate Packaging"

        packaging_category = "Heavy Duty"

        recommendations.append(
            "Heavy duty packaging required."
        )

        recommendations.append(
            "Steel reinforcement required."
        )

        recommendations.append(
            "Heavy lift handling provisions required."
        )

    # =====================================
    # OVERSIZED LOGIC
    # =====================================

    if oversized:

        recommendations.append(
            "Custom packaging design required."
        )

        recommendations.append(
            "Dimension verification required before dispatch."
        )

        recommendations.append(
            "Route clearance validation recommended."
        )

    # =====================================
    # FRAGILE LOGIC
    # =====================================

    if fragile == "Yes":

        recommendations.append(
            "Shock absorbers required."
        )

        recommendations.append(
            "Internal cushioning required."
        )

        recommendations.append(
            "Fragile handling precautions required."
        )

        recommendations.append(
            "Additional impact protection recommended."
        )

    # =====================================
    # ENGINEERING DRAWING
    # =====================================

    if (
        weight > 500
        or volume > 2
        or oversized
    ):

        engineering_drawing = "Required"

    else:

        engineering_drawing = "Optional"

    # =====================================
    # MATERIAL PLANNING
    # =====================================

    material_planning = "Required"

    # =====================================
    # STANDARD RECOMMENDATIONS
    # =====================================

    recommendations.append(
        "2D packaging drawing required."
    )

    recommendations.append(
        "Packaging design verification required."
    )

    recommendations.append(
        "Material sizing calculation required."
    )

    return {

        "packaging_type": packaging_type,

        "packaging_category": packaging_category,

        "engineering_drawing": engineering_drawing,

        "material_planning": material_planning,

        "surface_area": surface_area,

        "volume": volume,

        "oversized": oversized,

        "recommendations": recommendations
    }


def generate_packaging_summary(result):

    prompt = f"""
You are CDX Packaging Planning Assistant.

Use ONLY supplied data.

Packaging Type:
{result['packaging_type']}

Packaging Category:
{result['packaging_category']}

Engineering Drawing:
{result['engineering_drawing']}

Material Planning:
{result['material_planning']}

Volume:
{result['volume']} m³

Surface Area:
{result['surface_area']} m²

Oversized:
{result['oversized']}

Recommendations:
{result['recommendations']}

Explain:

1. Packaging Overview

2. Packaging Selection Reason

3. Volume Assessment

4. Surface Area Assessment

5. Engineering Drawing Requirement

6. Material Planning Requirement

7. Fragile Handling Considerations

8. Oversized Cargo Considerations

9. Packaging Verification Requirements

10. Final Packaging Assessment

Important:

- Use only supplied data.
- Do not invent regulations.
- Do not invent customer requirements.
- Keep explanation professional.
"""

    response = model.generate_content(prompt)

    return response.text