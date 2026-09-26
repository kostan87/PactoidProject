import sys
import time
import threading
from pathlib import Path
from threading import Event

from sqlalchemy.orm import Session

from app.models.database import Review
from app.models.review_analysis import BatchAnalysis
from app.repositories.review_repo import save_reviews_analysis_to_db
from app.llm.client import create_client, create_chat
from utils.files import load_config

def build_review_text(review: Review) -> str:
    parts = []
    if review.text:
        parts.append(review.text.strip())
    if review.pros:
        parts.append(f"Плюсы: {review.pros.strip()}")
    if review.cons:
        parts.append(f"Минусы: {review.cons.strip()}")
    parts = "\n".join(parts) if parts else "(пусто)"
    return f"[ID: {review.id}] " + parts

def form_messages_for_analysis(reviews: list[str]) -> list[dict]:
    DIR_PATH = Path(__file__).resolve().parent
    config_prompt = load_config(DIR_PATH / "config_prompts.toml")

    batch_prompt = config_prompt["batch_prompt"]
    user_message = batch_prompt + "\n".join(reviews)
    
    system_prompt = config_prompt["prompt"]
    few_shot = config_prompt["few_shot"]

    messages = [{"role": "system", "content": system_prompt}]
    for example in few_shot:
        messages.append({"role": "user", "content": example["input"]})
        messages.append({"role": "assistant", "content": example["output"]})
    messages.append({"role": "user", "content": user_message})
    return messages

def analyze_reviews_batches(session: Session, reviews_batches: list[list[str]]) -> None:
    batch_complited = threading.Event()
    for reviews_batch in reviews_batches:
        batch_complited.clear()
        timer_thread  = threading.Thread(target=start_timer, args=(batch_complited,), daemon=True)
        timer_thread.start()
        try:
            client = create_client()
            messages = form_messages_for_analysis(reviews_batch)
            result = create_chat(client=client, messages=messages, response_model=BatchAnalysis)
            save_reviews_analysis_to_db(session, result.results)
            session.commit()
        except ConnectionError as e:
            print(f"Нет подключения: {e}")
            session.rollback()
            break
        except Exception as e:
            print(f"Батч упал: {e}")
            session.rollback()
        finally:
            batch_complited.set()
            timer_thread.join()

def start_timer(threadEvent: Event) -> None:
    start_time = time.time()
    while not threadEvent.is_set():
        elapsed = time.time() - start_time
        sys.stdout.write(f"\rРаботаю... {elapsed:6.1f} сек")
        sys.stdout.flush()
        threadEvent.wait(timeout=0.5)
    sys.stdout.write(f"\n")