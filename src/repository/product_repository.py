from typing import List, Optional, Dict, Any
from .base_repository import BaseRepository
from models import Product

class ProductRepository(BaseRepository):
    def create_product(self, product: Product) -> int:
        query = "INSERT INTO products (name, price) VALUES (?, ?)"
        params = (product.name, product.price)
        return self.execute_insert(query, params)

    def get_all(self) -> List[Product]:
        query = "SELECT id, name, price FROM products"
        results = self.execute_query(query)
        return [Product.from_dict(result) for result in results]
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        query = "SELECT id, name, price FROM products WHERE id = ?"
        results = self.execute_query(query, (product_id,))
        return Product.from_dict(results[0]) if results else None
    
    def update_product(self, product: Product) -> bool:
        if not product.id:
            raise ValueError("Product ID is required for update")
        query = "UPDATE products SET name = ?, price = ? WHERE id = ?"
        params = (product.name, product.price, product.id)
        affected_rows = self.execute_update(query, params)
        return affected_rows > 0
    
    def delete_product(self, product_id: int) -> bool:
        query = "DELETE FROM products WHERE id = ?"
        affected_rows = self.execute_delete(query, (product_id,))
        return affected_rows > 0 