"""Review management routes for product reviews and ratings."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.database.config import get_db
from app.auth.security import get_current_user
from app.models.models import User, Product, Review, Order, OrderItem
from app.schemas.schemas import ReviewCreate, ReviewResponse, ProductReviewsResponse

# Router for product-level review operations (/products/{product_id}/reviews)
router = APIRouter(prefix="/products", tags=["Reviews"])

# Router for individual review operations (/reviews/{review_id})
review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/{product_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    product_id: int,
    review: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a product review.
    
    **Purchase Verification Logic:**
    - User MUST have purchased this product
    - Order status MUST be "delivered"
    - User can only leave ONE review per product
    
    Args:
        product_id: ID of product to review
        review: ReviewCreate with rating (1-5) and optional comment
        current_user: Currently authenticated user
        
    Returns: Created ReviewResponse
    
    Raises:
        404: Product not found
        403: User hasn't purchased and received the product
        400: User already reviewed this product or invalid rating
    """
    # Verify product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    # BUSINESS LOGIC VALIDATION 1: Check if user bought and received the product
    # Query for a delivered order containing this product by this user
    purchase_verification = db.query(OrderItem).join(Order).filter(
        Order.user_id == current_user.id,
        OrderItem.product_id == product_id,
        Order.status == "delivered"
    ).first()
    
    if not purchase_verification:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must purchase and receive this product to review it. "
                   "Please ensure your order is delivered."
        )
    
    # BUSINESS LOGIC VALIDATION 2: Check if user already reviewed this product
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.product_id == product_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product. "
                   "You can edit or delete your existing review."
        )
    
    # Create the review
    new_review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=review.rating,
        comment=review.comment
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review


@router.get("/{product_id}/reviews", response_model=ProductReviewsResponse)
def get_product_reviews(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a product with average rating.
    
    Public endpoint (no authentication required).
    
    Query Parameters:
        skip: Number of reviews to skip (default: 0)
        limit: Number of reviews to return (default: 10, max: 100)
        
    Returns: ProductReviewsResponse with:
        - reviews: List of ReviewResponse
        - average_rating: Average rating (null if no reviews)
        - total_reviews: Total number of reviews
        - product_id: Product ID
    
    Raises:
        404: Product not found
    """
    # Verify product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    # Get reviews
    reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    # Calculate average rating
    avg_rating_result = db.query(func.avg(Review.rating)).filter(
        Review.product_id == product_id
    ).scalar()
    
    average_rating = round(float(avg_rating_result), 2) if avg_rating_result else None
    
    # Get total review count
    total_reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).count()
    
    return ProductReviewsResponse(
        reviews=reviews,
        average_rating=average_rating,
        total_reviews=total_reviews,
        product_id=product_id
    )


@review_router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    updated_review: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a review (only by the review author).
    
    Args:
        review_id: ID of review to update
        updated_review: Updated ReviewCreate with new rating and/or comment
        current_user: Currently authenticated user
        
    Returns: Updated ReviewResponse
    
    Raises:
        404: Review not found
        403: User is not the review author
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    
    # Check ownership
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own reviews"
        )
    
    # Update review
    review.rating = updated_review.rating
    review.comment = updated_review.comment
    
    db.commit()
    db.refresh(review)
    
    return review


@review_router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a review (only by the review author or admin).
    
    Args:
        review_id: ID of review to delete
        current_user: Currently authenticated user
        
    Raises:
        404: Review not found
        403: User is not the review author
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    
    # Check ownership or admin status
    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )
    
    db.delete(review)
    db.commit()


@review_router.get("/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific review by ID.
    
    Public endpoint.
    
    Args:
        review_id: ID of review to retrieve
        
    Returns: ReviewResponse
    
    Raises:
        404: Review not found
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    
    return review
