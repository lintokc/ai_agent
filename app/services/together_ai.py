from together import Together
import json
import re
from app.config import config
from app.prompts import SYSTEM_PROMPT

client = Together(api_key=config.TOGETHER_AI_API_KEY)

def extract_valid_json(text: str) -> dict:
    """
    Extracts a valid JSON object from a response that might contain extra formatting.
    """
    try:
        text = text.strip()
        if text.startswith("json"):
            text = text[text.index("{"):]

        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            extracted_json = json_match.group(0)
            return json.loads(extracted_json)

    except (json.JSONDecodeError, ValueError):
        pass

    return None

def query_together_ai(user_prompt: str) -> dict:
    """
    Queries LLaMA 3.1 8B via Together AI.
    Parses output JSON to determine actions.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    output_text = response.choices[0].message.content.strip()

    parsed_json = extract_valid_json(output_text)
    if parsed_json:
        return parsed_json

    return {"action": "answer", "answer": output_text}
