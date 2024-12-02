from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(unsafe_hash=True)
class User:
    oid: Optional[int] = field(default=None)
    username: str = field(default='')
    email: Optional[str] = field(default=None)
    registration_date: datetime = field(default_factory=datetime.now)
 
    
