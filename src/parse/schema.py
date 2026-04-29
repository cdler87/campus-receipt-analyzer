from typing import List, Optional
from pydantic import BaseModel


class ReceiptItem(BaseModel):
    name: str
    quantity: Optional[int] = None
    price: Optional[float] = None


class ParsedReceipt(BaseModel):
    message_id: str
    vendor: Optional[str] = None
    timestamp: Optional[str] = None
    location: Optional[str] = None
    items: List[ReceiptItem] = []
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    parse_success: bool = True
    raw_model_output: Optional[str] = None
