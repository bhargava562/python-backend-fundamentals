from typing import List
from pydantic import BaseModel, Field, model_validator
from .user import UserResponse
from .product import ProductResponse

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float

class Order(BaseModel):
    user: UserResponse
    items: List[OrderItem]
    status: str = Field(default="pending")
    total: float = 0.0

    @model_validator(mode='after')
    def validate_business_rules(self) -> 'Order':
        # Cross-field validation: Calculate total automatically
        calculated_total = sum(item.quantity * item.unit_price for item in self.items)
        if self.total != 0 and self.total != calculated_total:
            raise ValueError(f"Total mismatch. Expected {calculated_total}")
        self.total = calculated_total
        
        # Logic rule: Cannot have empty order
        if not self.items:
            raise ValueError("Orders must contain at least one item")
        return self