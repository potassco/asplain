"""
Utility functions for parsing an LLM response
"""

import json


def parse_llm_json_response(response: str) -> str:
    """
    Parses an LLM response in JSON format
    Args:
        response: A string containing the LLM response in JSON format.
    Returns:
        A string containing the natural language explanation.
    """
    try:
        response = response.strip().removeprefix("```json").removesuffix("```").strip()
        response_json = json.loads(response, strict=False)
        return str(response_json.get("explanation").strip())
    except json.JSONDecodeError:
        return response
