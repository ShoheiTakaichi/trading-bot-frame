from pydantic import BaseModel


class Order(BaseModel):
    id: str
    timestamp: str
    symbol: str
    side: str
    price: float
    amount: float
