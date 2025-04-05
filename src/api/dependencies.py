from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from models import User, UserRole
from repository import UserRepository, Database
from services import UserService, PasswordService

# Authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create instances of services
database = Database("app.db")
user_repository = UserRepository(database)
password_service = PasswordService()
user_service = UserService(user_repository, password_service)

# Dependency to get database
def get_db():
    return database

# Dependency to get repositories
def get_user_repository():
    return user_repository

# Dependency to get services
def get_password_service():
    return password_service

def get_user_service():
    return user_service

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current authenticated user.
    In a real application, you would validate a JWT token here.
    This is a simplified example.
    """
    # This is where you would decode and validate the JWT token
    # For now, we just use the token as a username for simplicity
    user = user_service.get_user_by_username(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Authorization dependency - example for admin-only endpoints
async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the current user is an admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
