from fastapi import APIRouter, HTTPException
from app.schemas.product import ProductCreate, ProductUpdate, Product
from app.crud.product import create_product, get_product, update_product, delete_product, get_products

router = APIRouter()

@router.post("/", response_model=Product)
async def create_new_product(product: ProductCreate):
    db_product = await create_product(product)
    return db_product

@router.get("/{product_id}", response_model=Product)
async def read_product(product_id: int):
    db_product = await get_product(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=Product)
async def update_existing_product(product_id: int, product: ProductUpdate):
    db_product = await update_product(product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", response_model=Product)
async def delete_existing_product(product_id: int):
    db_product = await delete_product(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/", response_model=list[Product])
async def read_products(skip: int = 0, limit: int = 10):
    products = await get_products(skip=skip, limit=limit)
    return products