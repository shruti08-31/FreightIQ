# database/packaging_db.py
from database.db import get_connection

def get_similar_packaging(weight, length, width, height, geometry, high_value, export, lifting_method):
    conn = get_connection()
    cur = conn.cursor()
    
    # Mathematical Heuristic Order: Weight + Dimensions scaled down by 100
    cur.execute(
        """
        SELECT * FROM packaging
        ORDER BY (
            ABS(Weight_kg - ?) + 
            (ABS(Length_mm - ?) / 100.0) + 
            (ABS(Width_mm - ?) / 100.0) + 
            (ABS(Height_mm - ?) / 100.0)
        ) ASC
        LIMIT 5
        """,
        (weight, length, width, height)
    )
    rows = cur.fetchall()
    conn.close()
    
    similar_jobs = []
    for row_raw in rows:
        row = dict(row_raw)
        
        w = row['Weight_kg']
        l = row['Length_mm']
        wd = row['Width_mm']
        h = row['Height_mm']
        
        # Calculate localized mathematical similarity score
        tot_diff = abs(w - weight) + (abs(l - length) / 100.0) + (abs(wd - width) / 100.0) + (abs(h - height) / 100.0)
        base_scale = max(weight + (length / 100.0) + (width / 100.0) + (height / 100.0), 1)
        base_similarity = max(100.0 - (tot_diff / base_scale * 100), 50.0)
        
        # Apply structured bonus metrics for categorical matches
        bonus = 0.0
        if row['Geometry'] == geometry: bonus += 5.0
        if row['High_Value'] == high_value: bonus += 5.0
        if row['Export'] == export: bonus += 5.0
        if row['Lifting_Method'] == lifting_method: bonus += 5.0
        
        final_similarity = round(min(base_similarity + bonus, 100.0), 1)
        
        similar_jobs.append({
            "job_id": row['Shipment_ID'],
            "weight": w,
            "length": l,
            "width": wd,
            "height": h,
            "packaging_type": row['Packaging_Type'],
            "similarity": final_similarity,
            "technical_specs": {
                "product_type": row.get('Product_Type', 'Unknown'),
                "product_name": row.get('Product_Name', 'Unknown'),
                "geometry": row['Geometry'],
                "precision_surface": row['Precision_Surface'],
                "high_value": row['High_Value'],
                "export": row['Export'],
                "uneven_cg": row['Uneven_CG'],
                "projecting_parts": row['Projecting_Parts']
            },
            "logistics": {
                "lifting_method": row['Lifting_Method'],
                "base_support": row['Base_Support']
            },
            "engineering": {
                "drawing_required": row['Engineering_Drawing_Required'],
                "drawing_number": row['Drawing_Number'],
                "approval_status": row['Engineering_Approval']
            }
        })
    return similar_jobs
# if __name__ == "__main__":
#     print("Testing get_similar_packaging()...")
    
#     # Dummy inputs matching your function's arguments
#     test_results = get_similar_packaging(
#         weight=500.0,       # Weight_kg
#         length=1200.0,      # Length_mm
#         width=800.0,        # Width_mm
#         height=1000.0,      # Height_mm
#         geometry="Box",     # Geometry
#         high_value="Yes",   # High_Value
#         export="Yes",       # Export
#         lifting_method="Forklift" # Lifting_Method
#     )
    
#     print(f"Found {len(test_results)} similar jobs:")
#     import json
#     print(json.dumps(test_results, indent=2))