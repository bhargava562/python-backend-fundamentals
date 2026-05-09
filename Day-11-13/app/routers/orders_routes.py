"""Order management routes for checkout and order processing."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from enum import Enum

from app.database.config import get_db
from app.auth.security import get_current_user, get_admin_user
from app.models.models import User, Cart, CartItem, Order, OrderItem, Product
from app.schemas.schemas import OrderResponse, OrderItemResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


class OrderStatus(str, Enum):
    """Valid order statuses."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Checkout the user's cart and create an order.
    
    **CRITICAL BUSINESS LOGIC:**
    - Validates cart is not empty
    - Checks stock availability for ALL items
    - Uses database transaction for atomicity (all-or-nothing)
    - If any item is out of stock, ENTIRE transaction is rolled back
    - Deducts stock only after all validations pass
    - Captures product prices at order time (won't change if price updates later)
    
    Returns: OrderResponse with created order and items
    
    Raises:
        400: Cart is empty or item out of stock
        500: Database transaction error
    """
    # Step A: Fetch user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty. Add items before checkout."
        )
    
    try:
        # Step B: Transaction begins (try block ensures rollback on failure)
        
        # Step C: Validate all items have sufficient stock
        validation_errors = []
        for cart_item in cart.items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                validation_errors.append(
                    f"Product '{product.name}': Only {product.stock} available, "
                    f"but {cart_item.quantity} requested"
                )
        
        if validation_errors:
            # Rollback happens automatically in except block
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock: " + " | ".join(validation_errors)
            )
        
        # Step D & E: Deduct stock and calculate total
        order_total = 0.0
        order_items_data = []
        
        for cart_item in cart.items:
            product = cart_item.product
            # Deduct stock
            product.stock -= cart_item.quantity
            # Capture price at time of order
            item_total = product.price * cart_item.quantity
            order_total += item_total
            # Store order item data
            order_items_data.append({
                'product_id': product.id,
                'quantity': cart_item.quantity,
                'price': product.price
            })
        
        # Step F: Create Order record
        order = Order(
            user_id=current_user.id,
            total=order_total,
            status=OrderStatus.PENDING.value
        )
        db.add(order)
        db.flush()  # Get order ID without committing
        
        # Create OrderItem records
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            db.add(order_item)
        
        # Step G: Clear cart items
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        
        # Step H: Commit transaction
        db.commit()
        db.refresh(order)
        
        return order
        
    except HTTPException:
        # Re-raise HTTP exceptions
        db.rollback()
        raise
    except Exception as exc:
        # Catch any database errors and rollback
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Checkout failed: {str(exc)}. Cart and stock remain unchanged."
        )


@router.get("", response_model=List[OrderResponse])
def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: Optional[OrderStatus] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's order history.
    
    Supports pagination and filtering by status.
    
    Query Parameters:
        skip: Number of orders to skip (default: 0)
        limit: Number of orders to return (default: 10, max: 100)
        status_filter: Filter by order status (optional)
        
    Returns: List of OrderResponse
    """
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    # Apply status filter if provided
    if status_filter:
        query = query.filter(Order.status == status_filter.value)
    
    # Apply pagination
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return orders


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update an order's status (Admin only).
    
    Typical flow: pending -> confirmed -> shipped -> delivered
    
    Args:
        order_id: ID of order to update
        new_status: New OrderStatus
        
    Returns: Updated OrderResponse
    
    Raises:
        404: Order not found
        403: User is not admin
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    old_status = order.status
    order.status = new_status.value
    db.commit()
    db.refresh(order)
    
    return order


@router.put("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a pending order and restore stock.
    
    **Important Business Logic:**
    - Only "pending" orders can be cancelled
    - Cannot cancel "shipped" or "delivered" orders
    - Automatically restores product stock when cancelled
    
    Args:
        order_id: ID of order to cancel
        
    Returns: Updated OrderResponse
    
    Raises:
        404: Order not found or doesn't belong to user
        400: Order cannot be cancelled (already shipped/delivered)
    """
    # Get order
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    # Check if order can be cancelled
    if order.status != OrderStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status '{order.status}'. "
                   f"Only pending orders can be cancelled."
        )
    
    try:
        # Restore stock for all items
        for order_item in order.items:
            product = order_item.product
            product.stock += order_item.quantity
        
        # Update order status
        order.status = OrderStatus.CANCELLED.value
        db.commit()
        db.refresh(order)
        
        return order
        
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel order: {str(exc)}"
        )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific order.
    
    Users can only view their own orders. Admins can view any order.
    
    Args:
        order_id: ID of order to retrieve
        
    Returns: OrderResponse with full details
    
    Raises:
        404: Order not found
        403: User doesn't have permission to view order
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    # Check permissions: user can only view own orders
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this order"
        )
    
    return order
