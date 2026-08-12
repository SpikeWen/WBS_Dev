from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class PageStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


@dataclass(slots=True)
class ContentPage:
    id: str
    site_id: str
    title: str
    slug: str
    h1: str
    body: str
    meta_title: str
    meta_description: str
    sort_order: int
    show_in_nav: bool
    status: PageStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        title: str,
        slug: str,
        h1: str,
        body: str,
        meta_title: str,
        meta_description: str,
        sort_order: int,
    ) -> "ContentPage":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            title=title,
            slug=slug,
            h1=h1,
            body=body,
            meta_title=meta_title,
            meta_description=meta_description,
            sort_order=sort_order,
            show_in_nav=True,
            status=PageStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        title: str | None = None,
        slug: str | None = None,
        h1: str | None = None,
        body: str | None = None,
        meta_title: str | None = None,
        meta_description: str | None = None,
        sort_order: int | None = None,
        show_in_nav: bool | None = None,
        status: PageStatus | None = None,
    ) -> None:
        if title is not None:
            self.title = title
        if slug is not None:
            self.slug = slug
        if h1 is not None:
            self.h1 = h1
        if body is not None:
            self.body = body
        if meta_title is not None:
            self.meta_title = meta_title
        if meta_description is not None:
            self.meta_description = meta_description
        if sort_order is not None:
            self.sort_order = sort_order
        if show_in_nav is not None:
            self.show_in_nav = show_in_nav
        if status is not None:
            self.status = status
        self.updated_at = datetime.now(UTC)
