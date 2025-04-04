from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    price: float
    id: Optional[int] = None
    
    def to_tuple(self) -> tuple:
        return (self.name, self.price)
    
    @classmethod
    def from_tuple(cls, data: tuple) -> 'Product':
        if len(data) == 2:
            return cls(name=data[0], price=data[1])
        elif len(data) == 3:
            return cls(name=data[1], price=data[2], id=data[0])
        raise ValueError("Invalid tuple format") 