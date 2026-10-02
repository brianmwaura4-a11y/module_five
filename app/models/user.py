from dataclasses import asdict, dataclass, field
from typing import ClassVar, FrozenSet, Optional
import uuid


@dataclass
class Member:
    VALID_ROLES: ClassVar[FrozenSet[str]] = frozenset({"admin", "manager", "employee"})

    first_name: str
    last_name: str
    email: str
    employee_id: Optional[str] = None
    dept_id: Optional[str] = None
    role: str = "employee"
    is_active: bool = True
    password_hash: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if self.role not in self.VALID_ROLES:
            raise ValueError(f"role must be one of {sorted(self.VALID_ROLES)}")

    def to_dict(self) -> dict:
        return asdict(self)

    def to_public_dict(self) -> dict:
        d = self.to_dict()
        d.pop("password_hash", None)
        return d
