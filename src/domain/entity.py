from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional



class User(BaseModel):
    """Пользователь - основной объект предметной области
    """
    oid: int
    username: str = Field(default='')
    email: Optional[str] = Field(default=None)
    registration_date: datetime = Field(default_factory=datetime.now)

    def __hash__(self):
        return hash(self.oid)
 
    
