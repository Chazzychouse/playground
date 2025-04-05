from typing import List, Optional, Dict, Any
from datetime import datetime

from models import User, UserRole, UserStatus
from repository import UserRepository
from .password_service import PasswordService

class UserService:
    """
    Service for handling user-related business logic.
    
    This service separates business logic from repository data access.
    It handles password hashing, user creation/authentication, and other
    user-related operations.
    """
    
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service
    
    def create_user(self, username: str, password: str, email: str, 
                    role: UserRole = UserRole.USER) -> User:
        """
        Create a new user with a hashed password.
        
        Args:
            username: The username for the new user
            password: The plaintext password (will be hashed before storage)
            email: The user's email address
            role: The user's role (defaults to regular user)
            
        Returns:
            The newly created user
        """
        # Hash the password
        password_hash = self.password_service.hash_password(password)
        
        # Create the user with hashed password
        now = datetime.now()
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now
        )
        
        user_id = self.user_repository.create_user(user)
        user.id = user_id
        
        return user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: The username to authenticate
            password: The plaintext password to verify
            
        Returns:
            The authenticated user if successful, None otherwise
        """
        # Find the user
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None
        
        # Verify the password
        if not self.password_service.verify_password(password, user.password_hash):
            return None
        
        # Check if user is active
        if user.status != UserStatus.ACTIVE:
            return None
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        print(f"Getting user by ID: {user_id}")
        return self.user_repository.get_user_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.user_repository.get_user_by_username(username)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        return self.user_repository.get_user_by_email(email)
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.user_repository.get_all()
    
    def update_user(self, user: User) -> bool:
        """Update an existing user"""
        user.updated_at = datetime.now()
        return self.user_repository.update_user(user)
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change a user's password.
        
        Args:
            user_id: The ID of the user
            current_password: The current plaintext password for verification
            new_password: The new plaintext password
            
        Returns:
            True if password was changed successfully, False otherwise
        """
        # Get the user
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Verify current password
        if not self.password_service.verify_password(current_password, user.password_hash):
            return False
        
        # Hash and set new password
        user.password_hash = self.password_service.hash_password(new_password)
        user.updated_at = datetime.now()
        
        # Update the user
        return self.user_repository.update_user(user)
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.status = UserStatus.INACTIVE
        user.updated_at = datetime.now()
        
        return self.user_repository.update_user(user)
    
    def activate_user(self, user_id: int) -> bool:
        """Activate a user account"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.status = UserStatus.ACTIVE
        user.updated_at = datetime.now()
        
        return self.user_repository.update_user(user)
