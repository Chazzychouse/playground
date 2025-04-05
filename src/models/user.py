from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

@dataclass
class User:
    username: str
    email: str
    password_hash: str  # Store hashed password, not plain text
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            id=data.get('id'),
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            role=UserRole(data.get('role', UserRole.USER)),
            status=UserStatus(data.get('status', UserStatus.ACTIVE)),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
