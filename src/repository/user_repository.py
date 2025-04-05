from typing import List, Optional, Dict, Any
from .base_repository import BaseRepository
from models import User, UserRole, UserStatus
from datetime import datetime

class UserRepository(BaseRepository):
    def _map_to_user(self, record: Dict[str, Any]) -> User:
        return User.from_dict({
            'id': record['id'],
            'username': record['username'],
            'email': record['email'],
            'password_hash': record['password_hash'],
            'role': record['role'],
            'status': record['status'],
            'created_at': record['created_at'],
            'updated_at': record['updated_at']
        })

    def create_user(self, user: User) -> int:
        query = """
            INSERT INTO users (username, email, password_hash, role, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            user.username,
            user.email,
            user.password_hash,
            user.role.value,
            user.status.value,
            user.created_at or datetime.now(),
            user.updated_at or datetime.now()
        )
        return self.execute_insert(query, params)

    def get_all(self) -> List[User]:
        query = """
            SELECT id, username, email, password_hash, role, status, created_at, updated_at
            FROM users
        """
        results = self.execute_query(query)
        return [self._map_to_user(record) for record in results]
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = """
            SELECT id, username, email, password_hash, role, status, created_at, updated_at
            FROM users WHERE id = ?
        """
        print(f"Query: {query}")
        print(f"User ID: {user_id}")
        results = self.execute_query(query, (user_id,))
        print(f"Results: {results}")
        if not results:
            return None
        return self._map_to_user(results[0])
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        query = """
            SELECT id, username, email, password_hash, role, status, created_at, updated_at
            FROM users WHERE username = ?
        """
        results = self.execute_query(query, (username,))
        if not results:
            return None
        return self._map_to_user(results[0])
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        query = """
            SELECT id, username, email, password_hash, role, status, created_at, updated_at
            FROM users WHERE email = ?
        """
        results = self.execute_query(query, (email,))
        if not results:
            return None
        return self._map_to_user(results[0])
    
    def update_user(self, user: User) -> bool:
        if not user.id:
            raise ValueError("User ID is required for update")
        query = """
            UPDATE users 
            SET username = ?, email = ?, password_hash = ?, role = ?, status = ?, updated_at = ?
            WHERE id = ?
        """
        params = (
            user.username,
            user.email,
            user.password_hash,
            user.role.value,
            user.status.value,
            datetime.now(),
            user.id
        )
        affected_rows = self.execute_update(query, params)
        return affected_rows > 0
    
    def delete_user(self, user_id: int) -> bool:
        query = "DELETE FROM users WHERE id = ?"
        affected_rows = self.execute_delete(query, (user_id,))
        return affected_rows > 0
