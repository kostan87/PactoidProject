import argparse
import json
import sys
from pathlib import Path

from curl_cffi import requests
from curl_cffi.requests.errors import RequestsError
from tenacity import retry, stop_after_attempt, wait_random, retry_if_exception_type

def get_root_from_argv() -> int:
    parser = argparse.ArgumentParser(description="fetch reviews from WB")
    parser.add_argument("target_id", type=int)
    args = parser.parse_args()
    return (args.target_id)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=6, max=9),
    retry=retry_if_exception_type(RequestsError)
)
def fetch_host(target_id: int) -> str:
    url = f"https://feedback-bt.wildberries.ru/feedback/api/v2/host?imt={target_id}"
    host = requests.get(url, impersonate="chrome110").json()[0]
    return host

@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=6, max=9),
    retry=retry_if_exception_type(RequestsError)
)
def fetch_reviews(host: str, target_id: int) -> dict:
    url = f"{host}/feedbacks/v2/{target_id}"
    reviews = requests.get(url, impersonate="chrome110").json()
    return reviews

def save_reviews(data: dict, target_id: int) -> Path:
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "app" / "data" / "reviews" / f"wb_reviews_raw_{target_id}.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data_path

def print_stats(data: dict) -> None:
    reviews_all = len(data)
    reviews_with_text = len([review for review in data if review.get("text") not in (None, "")])
    reviews_with_bables = len([review for review in data if "bables" in review])
    print("RESPONSE: "
        f"reviews_all {reviews_all} | "
        f"reviews_with_text {reviews_with_text} | "
        f"reviews_with_bables {reviews_with_bables}"
    )

def main() -> None:
    try:
        root = get_root_from_argv()
        host = fetch_host(root)
        data = fetch_reviews(host, root)
        if ("feedbacks" in data):
            path = save_reviews(data, root)
            print(f"Saved to {path}")
            print_stats(data["feedbacks"])
        else:
            print("Получен нестандартный JSON")
    except RequestsError as e:
        print(f"Не удалось получить данные после 3 попыток: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()