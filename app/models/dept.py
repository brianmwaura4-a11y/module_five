from dataclasses import asdict, dataclass, field
from typing import Optional
import uuid


@dataclass
class Department:
    name: str
    parent_id: Optional[str] = None
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return asdict(self)
