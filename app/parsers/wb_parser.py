def parse_product(raw: dict) -> dict | None:
    wb_id = raw.get("id")
    if not wb_id:
        return None
    
    brand = raw.get("brand") or None
    supplier = raw.get("supplier") or None

    sizes = raw.get("sizes") or []
    first = sizes[0] if sizes else None
    price = (first or {}).get("price") or {}
    price_basic = (price.get("basic") or 0) / 100
    price_product = (price.get("product") or 0) / 100

    return {
        "id": wb_id,
        "subject_id": raw.get("subjectId"),
        "name": raw.get("name"),
        "brand": brand,
        "supplier": supplier,
        "supplier_rating": raw.get("supplierRating"),
        "rating": raw.get("rating"),
        "review_rating": raw.get("reviewRating"),
        "feedbacks_count": raw.get("feedbacks") or 0,
        "price_basic": price_basic,
        "price_product": price_product
    }

def parse_products(data: dict) -> list[dict]:
    if not isinstance(data, dict):
        return []

    products = []
    for product in (data.get("products") or []):
        if isinstance(product, dict):
            parsed_product = parse_product(product)
            if parsed_product is not None:
                products.append(parsed_product)
    return products