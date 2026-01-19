import json


def parse_llm_json_response(response: str) -> str:
    try:
        response = response.strip().removeprefix("```json").removesuffix("```").strip()
        response_json = json.loads(response, strict=False)
        return str(response_json.get("explanation").strip())
    except json.JSONDecodeError:
        return response
