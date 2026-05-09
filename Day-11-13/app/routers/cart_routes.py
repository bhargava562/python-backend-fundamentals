"""Cart management routes for shopping cart operations."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.config import get_db
from app.auth.security import get_current_user
from app.models.models import User, Cart, CartItem, Product
from app.schemas.schemas import CartResponse, CartItemCreate, CartItemResponse

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's shopping cart.
    
    Creates an empty cart if user doesn't have one yet.
    
    Returns: CartResponse with user's cart and items
    """
    # Fetch or create cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        # Create empty cart for user
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add an item to the cart or update quantity if item already exists.
    
    Args:
        item: CartItemCreate with product_id and quantity
        
    Returns: CartItemResponse
    
    Raises:
        404: Product not found
        400: Requested quantity exceeds available stock
    """
    # Get or create user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Fetch product
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {item.product_id} not found"
        )
    
    # Validate quantity against stock
    if item.quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requested quantity ({item.quantity}) exceeds available stock ({product.stock})"
        )
    
    # Check if product already in cart
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()
    
    if cart_item:
        # Update quantity
        new_quantity = cart_item.quantity + item.quantity
        if new_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Updated quantity ({new_quantity}) exceeds available stock ({product.stock})"
            )
        cart_item.quantity = new_quantity
    else:
        # Create new cart item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    
    return cart_item


@router.put("/items/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the quantity of a cart item.
    
    If quantity is 0, the item is deleted from cart.
    
    Args:
        item_id: ID of the cart item to update
        quantity: New quantity (>= 0)
        
    Returns: CartItemResponse or delete confirmation
    
    Raises:
        404: Cart item not found or doesn't belong to user
        400: Invalid quantity or exceeds stock
    """
    if quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity cannot be negative"
        )
    
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    # Get cart item
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart item with id {item_id} not found"
        )
    
    # If quantity is 0, delete the item
    if quantity == 0:
        db.delete(cart_item)
        db.commit()
        return {"message": "Item removed from cart"}
    
    # Validate against stock
    product = cart_item.product
    if quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quantity {quantity} exceeds available stock ({product.stock})"
        )
    
    # Update quantity
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    
    return cart_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove an item from the cart.
    
    Args:
        item_id: ID of the cart item to remove
        
    Raises:
        404: Cart item not found or doesn't belong to user
    """
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    # Get cart item
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart item with id {item_id} not found"
        )
    
    # Delete item
    db.delete(cart_item)
    db.commit()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Clear all items from the user's cart.
    
    Raises:
        404: Cart not found
    """
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    # Delete all cart items
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
