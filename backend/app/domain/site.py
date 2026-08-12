from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class SiteStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass(slots=True)
class Site:
    id: str
    tenant_id: str
    name: str
    template_id: str
    domain: str | None
    status: SiteStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        tenant_id: str,
        name: str,
        template_id: str,
        domain: str | None,
    ) -> "Site":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            tenant_id=tenant_id,
            name=name,
            template_id=template_id,
            domain=domain,
            status=SiteStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        name: str | None = None,
        template_id: str | None = None,
        domain: str | None = None,
        status: SiteStatus | None = None,
    ) -> None:
        if name is not None:
            self.name = name
        if template_id is not None:
            self.template_id = template_id
        if domain is not None:
            self.domain = domain
        if status is not None:
            self.status = status
        self.updated_at = datetime.now(UTC)

    def missing_fields(self) -> list[str]:
        missing: list[str] = []
        if not self.name:
            missing.append("name")
        if not self.template_id:
            missing.append("template_id")
        if not self.domain:
            missing.append("domain")
        return missing


@dataclass(slots=True)
class SiteStatusView:
    site_id: str
    status: SiteStatus
    missing_fields: list[str] = field(default_factory=list)

