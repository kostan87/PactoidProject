from pydantic import BaseModel, Field
from typing import Literal

class Aspect(BaseModel):
    aspect: Literal[
        # Product
        "экран", "камера", "звук", "микрофон",
        "зарядка", "батарея", "производительность", "память", "софт",
        "связь", "wi-fi", "bluetooth", "нагрев",
        "корпус", "внешний вид", "сенсор", "сборка",
        "комплектация", "работоспособность", "цена",
        # Service
        "продавец", "сервис", "доставка", "упаковка", "возврат",
        # Fallback
        "другое",
    ]
    type: Literal["defect", "advantage", "neutral"]
    sentiment: Literal["positive", "negative", "neutral"]
    detail: str = Field(description="Цитата или суть, до 12 слов. Сохраняй временные маркеры.")