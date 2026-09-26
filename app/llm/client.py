from functools import lru_cache
from pathlib import Path
from typing import TypeVar

import instructor
from instructor import Instructor
from openai import OpenAI
from pydantic import BaseModel

from utils.files import load_config, llm_cache

ModelType = TypeVar("T", bound=BaseModel)

@lru_cache(maxsize=1)
def create_client() -> Instructor:
    DIR_PATH = Path(__file__).resolve().parent
    config = load_config(DIR_PATH / "config.toml")
    return instructor.from_openai(
        OpenAI(
            base_url=config["llm_url"],
            api_key=config["llm_api_key"],
            max_retries=5,
        ),  
        mode=instructor.Mode.JSON,
    )

@llm_cache
def create_chat(client: Instructor, messages: list[dict], response_model: type[ModelType]) -> ModelType:
    DIR_PATH = Path(__file__).resolve().parent
    config = load_config(DIR_PATH / "config.toml")

    result = client.chat.completions.create(
        model=config["llm_model"],
        messages=messages,
        response_model=response_model,
        temperature=config["llm_temperature"],
        max_retries=2,
    )

    return result