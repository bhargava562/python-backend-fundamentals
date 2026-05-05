from fastapi import APIRouter, Depends, HTTPException, status
from ..database.mongodb import get_database
from ..models.catalog import Product, ProductUpdate
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/products", tags=["Catalog"])

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product, db=Depends(get_database)):
    product_dict = product.model_dump(by_alias=True, exclude=["id"])
    result = await db["products"].insert_one(product_dict)
    
    product_dict["_id"] = result.inserted_id
    return product_dict

@router.get("/", response_model=List[Product])
async def list_products(category: str = None, min_price: float = None, db=Depends(get_database)):
    # Dynamic querying
    query = {}
    if category:
        query["category"] = category
    if min_price is not None:
        query["price"] = {"$gte": min_price} # MongoDB specific query operator
        
    products = await db["products"].find(query).to_list(100) # Limit to 100
    return products

@router.get("/{id}", response_model=Product)
async def get_product(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    product = await db["products"].find_one({"_id": ObjectId(id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=Product)
async def update_product(id: str, update_data: ProductUpdate, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    # Convert update_data to dict and remove None values
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No valid fields to update")
        
    # Using $set operator to update specific fields
    result = await db["products"].update_one(
        {"_id": ObjectId(id)}, {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made to the product")
        
    return await db["products"].find_one({"_id": ObjectId(id)})

@router.delete("/{id}")
async def delete_product(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    result = await db["products"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
        
    return {"message": "Product deleted successfully"}