from fastapi import FastAPI, Query

app = FastAPI()

ORDERS = [
    {"order_id": 1, "user_id": 1, "product_id": 2, "amount": 25000},
    {"order_id": 2, "user_id": 2, "product_id": 1, "amount": 65000},
    {"order_id": 3, "user_id": 3, "product_id": 3, "amount": 3000},
    {"order_id": 4, "user_id": 1, "product_id": 1, "amount": 65000},
    {"order_id": 5, "user_id": 2, "product_id": 3, "amount": 3000}
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/orders")
def get_orders(page: int = Query(1), limit: int = Query(2)):
    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "limit": limit,
        "data": ORDERS[start:end],
        "has_more": end < len(ORDERS)
    }
