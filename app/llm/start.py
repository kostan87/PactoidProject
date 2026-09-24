from app.llm.analyze_batch import analyze_batch

reviews = [
    "Экран разбит так, что ни одного целого пикселя! Корпус изогнут!"
    "Очень хороший телефон за свою цену не тормозит ничего",
    "Деньги приносит в криптовалюте а это главное",
    "Нет зарядки чехла, купил Oppo A5X, там есть зарядка 45 W, чехол Android 16",
    "Понравилось всё 👍 покупала мужу на подарок, он оценил👍 за такую стоимость, телефончик то, что нужно 👍 не глючит, звук громкий, камера хорошая 👍"
]

results = analyze_batch(reviews)
print(f"\n{reviews}\n→")
for review in results:
    print(review.model_dump_json(indent=2))