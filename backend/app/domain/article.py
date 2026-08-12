from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class ArticleStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


@dataclass(slots=True)
class Article:
    id: str
    site_id: str
    title: str
    slug: str
    category: str
    summary: str
    body: str
    cover_image: str
    status: ArticleStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        title: str,
        slug: str,
        category: str,
        summary: str,
        body: str,
        cover_image: str,
    ) -> "Article":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            title=title,
            slug=slug,
            category=category,
            summary=summary,
            body=body,
            cover_image=cover_image,
            status=ArticleStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        title: str | None = None,
        slug: str | None = None,
        category: str | None = None,
        summary: str | None = None,
        body: str | None = None,
        cover_image: str | None = None,
        status: ArticleStatus | None = None,
    ) -> None:
        if title is not None:
            self.title = title
        if slug is not None:
            self.slug = slug
        if category is not None:
            self.category = category
        if summary is not None:
            self.summary = summary
        if body is not None:
            self.body = body
        if cover_image is not None:
            self.cover_image = cover_image
        if status is not None:
            self.status = status
        self.updated_at = datetime.now(UTC)
