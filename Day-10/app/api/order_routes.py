from fastapi import APIRouter, HTTPException, status
from typing import List
from app.core.logger import logger
from app.schemas import OrderCreate, OrderResponse
from app.database import db

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        logger.info(f"Creating order for user: {order.user_id}")
        
        # Validate user exists
        user = db.get_user(order.user_id)
        if not user:
            logger.warning(f"User not found: {order.user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate product exists
        product = db.get_product(order.product_id)
        if not product:
            logger.warning(f"Product not found: {order.product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Check stock availability
        if product["stock"] < order.quantity:
            logger.warning(f"Insufficient stock for product: {order.product_id}")
            raise HTTPException(status_code=400, detail="Insufficient stock")
        
        # Calculate total price
        total_price = product["price"] * order.quantity
        
        # Create order
        order_dict = order.model_dump()
        order_dict["total_price"] = total_price
        
        created_order = db.create_order(order_dict)
        
        # Update product stock
        db.update_product(order.product_id, {"stock": product["stock"] - order.quantity})
        
        logger.info(f"Order created successfully: {created_order['id']}")
        return created_order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create order")

@router.get("/", response_model=List[OrderResponse])
async def get_all_orders():
    """Get all orders"""
    try:
        logger.debug("Fetching all orders")
        orders = db.get_all_orders()
        logger.info(f"Retrieved {len(orders)} orders")
        return orders
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    """Get a specific order by ID"""
    try:
        logger.debug(f"Fetching order with ID: {order_id}")
        order = db.get_order(order_id)
        if not order:
            logger.warning(f"Order not found: {order_id}")
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch order")

@router.get("/user/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(user_id: int):
    """Get all orders for a specific user"""
    try:
        logger.debug(f"Fetching orders for user: {user_id}")
        user = db.get_user(user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        orders = db.get_user_orders(user_id)
        logger.info(f"Retrieved {len(orders)} orders for user: {user_id}")
        return orders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user orders")
