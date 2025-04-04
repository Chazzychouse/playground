from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    password: str
    id: Optional[int] = None
    
    def to_tuple(self) -> tuple:
        return (self.username, self.password)
    
    @classmethod
    def from_tuple(cls, data: tuple) -> 'User':
        if len(data) == 2:
            return cls(username=data[0], password=data[1])
        elif len(data) == 3:
            return cls(username=data[1], password=data[2], id=data[0])
        raise ValueError("Invalid tuple format")
