from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass()
class User:
    oid: int
    username: str = field(default='')
    email: Optional[str] = field(default=None)
    registration_date: datetime = field(default_factory=datetime.now)

    def __hash__(self):
        return hash(self.oid)
 
    
