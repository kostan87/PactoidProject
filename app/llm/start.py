import threading

from app.llm.review_analysis import build_review_text, get_reviews_from_db, remove_cached_reviews, analyze_reviews_batch, start_timer

batch_complited = threading.Event()

reviews_from_db = get_reviews_from_db(500)
reviews_for_analysis = remove_cached_reviews(reviews_from_db)
reviews_text = [build_review_text(review) for review in reviews_for_analysis]
reviews_batches = [reviews_text[x:x+5] for x in range(0, len(reviews_text), 5)]

for batch in reviews_batches:
    batch_complited.clear()

    batching = threading.Thread(target=analyze_reviews_batch, args=(batch_complited, batch,), daemon=True)
    batching.start()

    start_timer(batch_complited)