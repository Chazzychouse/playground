from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Product:
    name: str
    price: float
    id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary, excluding None values"""
        result = {
            "name": self.name,
            "price": self.price
        }
        if self.id is not None:
            result["id"] = self.id
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create a Product instance from a dictionary"""
        return cls(
            name=data['name'],
            price=data['price'],
            id=data.get('id')  # Use get to handle optional id
        ) 