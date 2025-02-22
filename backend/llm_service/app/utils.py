from typing import Dict, Any

def format_response(response: str) -> Dict[str, Any]:
    """Format the LLM response"""
    return {
        "status": "success",
        "data": response
    }

def format_error(error: str) -> Dict[str, Any]:
    """Format error responses"""
    return {
        "status": "error",
        "error": str(error)
    }
