"""In-memory database for demonstration purposes"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas import UserResponse, ProductResponse, OrderResponse

class FakeDB:
    """Fake database storing data in memory"""
    
    def __init__(self):
        self.users: Dict[int, Dict[str, Any]] = {}
        self.products: Dict[int, Dict[str, Any]] = {}
        self.orders: Dict[int, Dict[str, Any]] = {}
        self.user_id_counter = 0
        self.product_id_counter = 0
        self.order_id_counter = 0
        
        # Initialize with sample data
        self._seed_data()
    
    def _seed_data(self):
        """Seed with sample data"""
        # Sample users
        users_data = [
            {"name": "Alice Johnson", "email": "alice@example.com", "age": 28},
            {"name": "Bob Smith", "email": "bob@example.com", "age": 35},
            {"name": "Charlie Brown", "email": "charlie@example.com", "age": 42},
        ]
        
        for user_data in users_data:
            self.user_id_counter += 1
            self.users[self.user_id_counter] = {
                "id": self.user_id_counter,
                **user_data,
                "created_at": datetime.now()
            }
        
        # Sample products
        products_data = [
            {"name": "Laptop", "description": "High performance laptop", "price": 999.99, "stock": 50},
            {"name": "Mouse", "description": "Wireless mouse", "price": 29.99, "stock": 200},
            {"name": "Keyboard", "description": "Mechanical keyboard", "price": 79.99, "stock": 100},
            {"name": "Monitor", "description": "4K Monitor", "price": 399.99, "stock": 30},
        ]
        
        for product_data in products_data:
            self.product_id_counter += 1
            self.products[self.product_id_counter] = {
                "id": self.product_id_counter,
                **product_data,
                "created_at": datetime.now()
            }
    
    # User operations
    def create_user(self, user_data: dict) -> Dict[str, Any]:
        self.user_id_counter += 1
        user = {
            "id": self.user_id_counter,
            **user_data,
            "created_at": datetime.now()
        }
        self.users[self.user_id_counter] = user
        return user
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        return list(self.users.values())
    
    def update_user(self, user_id: int, user_data: dict) -> Optional[Dict[str, Any]]:
        if user_id not in self.users:
            return None
        self.users[user_id].update(user_data)
        return self.users[user_id]
    
    def delete_user(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    # Product operations
    def create_product(self, product_data: dict) -> Dict[str, Any]:
        self.product_id_counter += 1
        product = {
            "id": self.product_id_counter,
            **product_data,
            "created_at": datetime.now()
        }
        self.products[self.product_id_counter] = product
        return product
    
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        return self.products.get(product_id)
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        return list(self.products.values())
    
    def update_product(self, product_id: int, product_data: dict) -> Optional[Dict[str, Any]]:
        if product_id not in self.products:
            return None
        self.products[product_id].update(product_data)
        return self.products[product_id]
    
    def delete_product(self, product_id: int) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
    
    # Order operations
    def create_order(self, order_data: dict) -> Dict[str, Any]:
        self.order_id_counter += 1
        order = {
            "id": self.order_id_counter,
            **order_data,
            "created_at": datetime.now()
        }
        self.orders[self.order_id_counter] = order
        return order
    
    def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        return self.orders.get(order_id)
    
    def get_all_orders(self) -> List[Dict[str, Any]]:
        return list(self.orders.values())
    
    def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        return [order for order in self.orders.values() if order["user_id"] == user_id]

# Global database instance
db = FakeDB()
