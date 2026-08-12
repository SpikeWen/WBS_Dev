from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(slots=True)
class MediaAsset:
    id: str
    site_id: str
    filename: str
    url: str
    alt_text: str
    file_type: str
    size: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        filename: str,
        url: str,
        alt_text: str,
        file_type: str,
        size: int,
    ) -> "MediaAsset":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            filename=filename,
            url=url,
            alt_text=alt_text,
            file_type=file_type,
            size=size,
            created_at=now,
            updated_at=now,
        )

    def update(self, alt_text: str | None = None) -> None:
        if alt_text is not None:
            self.alt_text = alt_text
        self.updated_at = datetime.now(UTC)
