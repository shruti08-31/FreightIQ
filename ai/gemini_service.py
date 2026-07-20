import logging
from ai.orchestrator import process_query
logger = logging.getLogger(__name__)
CONTACT_INFO = """
Information is not available in the current CDX database.

Please contact:
HEEP - Heavy Electrical Equipment Plant, BHEL, Haridwar
CFFP - Central Foundry Forge Plant, BHEL, Haridwar
PCRI - Pollution Control Research Institute, Haridwar
GSTIN: 05AAACB4146P1ZL
Corporate Office: BHEL House, Siri Fort, New Delhi
"""
# MAIN ENTRY POINT
def get_ai_response(user_query, shipments_payload=None):
    """
    Main interface for the application. 
    Delegates completely to the orchestrator to preserve the AI Explanation Layer architecture.
    
    Args:
        user_query (str): The natural language query from the user.
        shipments_payload (list, optional): A list of shipment dictionaries for load 
                                            optimization and consolidation workflows.
                                            Format: [{"id": "S1", "weight": 10, "length": 2000, "width": 1000, "height": 1000}]
    Returns:
        str: The AI-generated professional explanation based strictly on the database results.
    """
    if not user_query or not str(user_query).strip():
        return "Please provide a valid logistics query (e.g., 'Recommend a vehicle for 25MT' or 'Find route from Agra to Aligarh')."

    try:
        response = process_query(user_query, shipments_payload)
        # Check if the orchestrator couldn't find parameters or failed to fetch data
        if not response or "Information is not available" in response:
            return CONTACT_INFO
        
        if "couldn't identify the specific logistics parameters" in response:
            return f"{response}\n\n---\n{CONTACT_INFO}"
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing AI query in gemini_service: {str(e)}")
        return CONTACT_INFO
