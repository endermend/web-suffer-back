from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class UserIDDTO:
    """DTO User ID."""

    user_id: UUID
