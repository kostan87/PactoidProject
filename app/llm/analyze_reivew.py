from pathlib import Path

from utils.files import load_config
from app.llm.models import ReviewAnalysis, BatchAnalysis
from app.llm.client import create_client, create_chat

def analyze_review(review_text: str) -> ReviewAnalysis:
    DIR_PATH = Path(__file__).resolve().parent
    config_prompt = load_config(DIR_PATH / "config_prompts.toml")

    system_prompt = config_prompt["prompt"]
    few_shot = config_prompt["few_shot"]

    messages = [{"role": "system", "content": system_prompt}]
    for example in few_shot:
        messages.append({"role": "user", "content": example["review"]})
        messages.append({"role": "assistant", "content": example["output"]})
    messages.append({"role": "user", "content": review_text})

    client = create_client()
    result = create_chat(client=client, messages=messages, response_model=BatchAnalysis)
    return result.results