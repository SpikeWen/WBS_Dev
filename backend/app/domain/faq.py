from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class FAQStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


@dataclass(slots=True)
class FAQItem:
    id: str
    site_id: str
    question: str
    answer: str
    category: str
    sort_order: int
    status: FAQStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        question: str,
        answer: str,
        category: str,
        sort_order: int,
    ) -> "FAQItem":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            question=question,
            answer=answer,
            category=category,
            sort_order=sort_order,
            status=FAQStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        question: str | None = None,
        answer: str | None = None,
        category: str | None = None,
        sort_order: int | None = None,
        status: FAQStatus | None = None,
    ) -> None:
        if question is not None:
            self.question = question
        if answer is not None:
            self.answer = answer
        if category is not None:
            self.category = category
        if sort_order is not None:
            self.sort_order = sort_order
        if status is not None:
            self.status = status
        self.updated_at = datetime.now(UTC)
