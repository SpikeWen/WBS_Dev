from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class PublishStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(slots=True)
class PublishRecord:
    id: str
    site_id: str
    version: str
    status: PublishStatus
    preview_url: str
    publish_url: str
    output_path: str
    message: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        version: str,
        status: PublishStatus,
        preview_url: str,
        publish_url: str,
        output_path: str,
        message: str,
    ) -> "PublishRecord":
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            version=version,
            status=status,
            preview_url=preview_url,
            publish_url=publish_url,
            output_path=output_path,
            message=message,
            created_at=datetime.now(UTC),
        )
