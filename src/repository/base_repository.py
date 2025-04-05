from typing import Any, List, Optional, Tuple, Dict
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    def __init__(self, database):
        self.database = database
    
    @abstractmethod
    def get_all(self) -> List[Tuple]:
        pass
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        with self.database.get_connection() as conn:
            conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
    
    def execute_insert(self, query: str, params: Optional[Tuple] = None) -> int:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount
            
    def execute_delete(self, query: str, params: Optional[Tuple] = None) -> int:
        return self.execute_update(query, params) 