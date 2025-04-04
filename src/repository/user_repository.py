from typing import List, Optional
from .base_repository import BaseRepository
from models import User

class UserRepository(BaseRepository):
    def create_user(self, user: User) -> int:
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        return self.execute_insert(query, user.to_tuple())

    def get_all(self) -> List[User]:
        query = "SELECT id, username, password FROM users"
        results = self.execute_query(query)
        return [User.from_tuple(result) for result in results]
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = "SELECT id, username, password FROM users WHERE id = ?"
        results = self.execute_query(query, (user_id,))
        return User.from_tuple(results[0]) if results else None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        query = "SELECT id, username, password FROM users WHERE username = ?"
        results = self.execute_query(query, (username,))
        return User.from_tuple(results[0]) if results else None
    
    def update_user(self, user: User) -> bool:
        if not user.id:
            raise ValueError("User ID is required for update")
        query = "UPDATE users SET username = ?, password = ? WHERE id = ?"
        params = (*user.to_tuple(), user.id)
        affected_rows = self.execute_update(query, params)
        return affected_rows > 0
    
    def delete_user(self, user_id: int) -> bool:
        query = "DELETE FROM users WHERE id = ?"
        affected_rows = self.execute_delete(query, (user_id,))
        return affected_rows > 0
