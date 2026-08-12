from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class ServiceStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


@dataclass(slots=True)
class ServiceItem:
    id: str
    site_id: str
    name: str
    slug: str
    category: str
    summary: str
    scope: str
    process: str
    deliverables: str
    price_note: str
    status: ServiceStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        name: str,
        slug: str,
        category: str,
        summary: str,
        scope: str,
        process: str,
        deliverables: str,
        price_note: str,
    ) -> "ServiceItem":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            name=name,
            slug=slug,
            category=category,
            summary=summary,
            scope=scope,
            process=process,
            deliverables=deliverables,
            price_note=price_note,
            status=ServiceStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        name: str | None = None,
        slug: str | None = None,
        category: str | None = None,
        summary: str | None = None,
        scope: str | None = None,
        process: str | None = None,
        deliverables: str | None = None,
        price_note: str | None = None,
        status: ServiceStatus | None = None,
    ) -> None:
        if name is not None:
            self.name = name
        if slug is not None:
            self.slug = slug
        if category is not None:
            self.category = category
        if summary is not None:
            self.summary = summary
        if scope is not None:
            self.scope = scope
        if process is not None:
            self.process = process
        if deliverables is not None:
            self.deliverables = deliverables
        if price_note is not None:
            self.price_note = price_note
        if status is not None:
            self.status = status
        self.updated_at = datetime.now(UTC)
