import json

from pathlib import Path

from curl_cffi import requests

target = 513853400

host = requests.get(
    f"https://feedback-bt.wildberries.ru/feedback/api/v2/host?imt={target}",
    impersonate="chrome110"
).json()[0]

reviews = requests.get(
    f"{host}/feedbacks/v2/{target}",
    impersonate="chrome110"
)

print(len(reviews.json()["feedbacks"]))

data_path = Path("app/data/wb_reviews_raw.json")
data_path.parent.mkdir(parents=True, exist_ok=True)
data_path.write_text(json.dumps(reviews.json(), ensure_ascii=False, indent=2), encoding="utf-8")