from pathlib import Path

from utils.files import load_config
from app.models.review_analysis import ReviewAnalysis, BatchAnalysis
from app.llm.client import create_client, create_chat

def analyze_batch(reviews: list[str]) -> list[ReviewAnalysis]:
    DIR_PATH = Path(__file__).resolve().parent
    config_prompt = load_config(DIR_PATH / "config_prompts.toml")

    batch_prompt = config_prompt["batch_prompt"]
    numbered = "\n".join(f"[{i+1}] {r}" for i, r in enumerate(reviews))
    user_message = batch_prompt + numbered
    
    system_prompt = config_prompt["prompt"]
    few_shot = config_prompt["few_shot"]

    messages = [{"role": "system", "content": system_prompt}]
    for example in few_shot:
        messages.append({"role": "user", "content": example["input"]})
        messages.append({"role": "assistant", "content": example["output"]})
    messages.append({"role": "user", "content": user_message})

    client = create_client()
    result = create_chat(client=client, messages=messages, response_model=BatchAnalysis)
    return result.results