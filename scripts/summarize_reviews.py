import httpx
import json
from pathlib import Path

from sqlalchemy import select, func, inspect

from app.db import SessionLocal
from app.models.database.review import Review
from utils.database import process_batch

def summarize(text: str) -> str:
    response = httpx.post(
        "http://host.docker.internal:11434/api/chat",
        json={
            "model": "Qwen2.5-7B-Instruct-Q4_K_M:latest",
            "messages": [
                {
                    "role": "system", 
                    "content": 
                    "Прочитай отзыв на смартфон.\n"
                    "Игнорируй информацию вне темы. Игнорируй слова об криптовалюте, родственниках.\n"
                    "Строго соблюдай грамматику, ставь пробелы и запятые где это возможно.\n"
                    "Верни JSON с полями defect, note, view.\n"
                    "Если есть информация о проблемах, поломках, дефектах, жалобы на срок работы — кратко напиши это в поле defect.\n"
                    "Если есть информация о комплектации, упаковке, доставке, цене, зарядке - кратко напиши это в поле note.\n"
                    "Если есть информация о хорошем качестве или конкретных характеристиках товара - кратко напиши опиши это в поле view.\n"
                    "Если в нет информации для поля — пиши в это поле null.\n"
                },
                {"role": "user", "content": text}
            ],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1},
        },
        timeout=120.0,
    )
    return response.json()["message"]["content"]

with SessionLocal.begin() as session:
    reviews = session.scalars(select(Review).where(
        (Review.root == 513853400) & (
            ((Review.text != "NULL") & (func.length(Review.text) > 30)) |
            ((Review.cons != "NULL") & (func.length(Review.cons) > 10)) | 
            ((Review.pros != "NULL") & (func.length(Review.pros) > 10))
        )
    ).limit(500)).all()

    data = []
    for review in reviews:
        parts = []
        if review.text: parts.append(f"Отзыв: {review.text.strip()}")
        if review.pros: parts.append(f"Плюсы: {review.pros.strip()}")
        if review.cons: parts.append(f"Минусы: {review.cons.strip()}")
        text = "\n".join(parts)

        result = json.loads(summarize(text))

        mapper = inspect(Review).mapper
        review = {col.key: getattr(review, col.key) for col in mapper.columns}

        analyzed_review = {k:v for k,v in review.items() if k not in [
            "created_date", 
            "global_user_id", 
            "parent_feedback_id", 
            "child_feedback_id"
        ]}
        analyzed_review["view"] = result["view"]
        analyzed_review["note"] = result["note"]
        analyzed_review["defect"] = result["defect"]

        data.append(analyzed_review)
        print (len(data))

    base_dir = Path(__file__).resolve().parents[1] 
    data_path = base_dir / "app" / "data" / "reviews_data.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")