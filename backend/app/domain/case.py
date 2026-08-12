from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class CaseStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


@dataclass(slots=True)
class CaseStudy:
    id: str
    site_id: str
    title: str
    slug: str
    client_name: str
    industry: str
    summary: str
    challenge: str
    solution: str
    result: str
    cover_image: str
    project_date: str
    status: CaseStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        title: str,
        slug: str,
        client_name: str,
        industry: str,
        summary: str,
        challenge: str,
        solution: str,
        result: str,
        cover_image: str,
        project_date: str,
    ) -> "CaseStudy":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            title=title,
            slug=slug,
            client_name=client_name,
            industry=industry,
            summary=summary,
            challenge=challenge,
            solution=solution,
            result=result,
            cover_image=cover_image,
            project_date=project_date,
            status=CaseStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        title: str | None = None,
        slug: str | None = None,
        client_name: str | None = None,
        industry: str | None = None,
        summary: str | None = None,
        challenge: str | None = None,
        solution: str | None = None,
        result: str | None = None,
        cover_image: str | None = None,
        project_date: str | None = None,
        status: CaseStatus | None = None,
    ) -> None:
        if title is not None:
            self.title = title
        if slug is not None:
            self.slug = slug
        if client_name is not None:
            self.client_name = client_name
        if industry is not None:
            self.industry = industry
        if summary is not None:
            self.summary = summary
        if challenge is not None:
            self.challenge = challenge
        if solution is not None:
            self.solution = solution
        if result is not None:
            self.result = result
        if cover_image is not None:
            self.cover_image = cover_image
        if project_date is not None:
            self.project_date = project_date
        if status is not None:
            self.status = status
        self.updated_at = datetime.now(UTC)
