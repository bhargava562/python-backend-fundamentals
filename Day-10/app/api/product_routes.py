from fastapi import APIRouter, HTTPException, status
from typing import List
from app.core.logger import logger
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.database import db

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        logger.info(f"Creating product: {product.name}")
        product_dict = product.model_dump()
        created_product = db.create_product(product_dict)
        logger.info(f"Product created successfully: {created_product['id']}")
        return created_product
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.get("/", response_model=List[ProductResponse])
async def get_all_products():
    """Get all products"""
    try:
        logger.debug("Fetching all products")
        products = db.get_all_products()
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        logger.debug(f"Fetching product with ID: {product_id}")
        product = db.get_product(product_id)
        if not product:
            logger.warning(f"Product not found: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate):
    """Update an existing product"""
    try:
        logger.info(f"Updating product: {product_id}")
        product = db.get_product(product_id)
        if not product:
            logger.warning(f"Product not found for update: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        
        update_data = product_update.model_dump(exclude_unset=True)
        updated_product = db.update_product(product_id, update_data)
        logger.info(f"Product updated successfully: {product_id}")
        return updated_product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update product")

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    """Delete a product"""
    try:
        logger.info(f"Deleting product: {product_id}")
        product = db.get_product(product_id)
        if not product:
            logger.warning(f"Product not found for deletion: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete_product(product_id)
        logger.info(f"Product deleted successfully: {product_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete product")
