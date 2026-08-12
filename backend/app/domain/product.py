from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class ProductStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


@dataclass(slots=True)
class Product:
    id: str
    site_id: str
    name: str
    slug: str
    category: str
    model: str
    summary: str
    description: str
    specifications: str
    cover_image: str
    price_note: str
    status: ProductStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        site_id: str,
        name: str,
        slug: str,
        category: str,
        model: str,
        summary: str,
        description: str,
        specifications: str,
        cover_image: str,
        price_note: str,
    ) -> "Product":
        now = datetime.now(UTC)
        return cls(
            id=str(uuid4()),
            site_id=site_id,
            name=name,
            slug=slug,
            category=category,
            model=model,
            summary=summary,
            description=description,
            specifications=specifications,
            cover_image=cover_image,
            price_note=price_note,
            status=ProductStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        name: str | None = None,
        slug: str | None = None,
        category: str | None = None,
        model: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        specifications: str | None = None,
        cover_image: str | None = None,
        price_note: str | None = None,
        status: ProductStatus | None = None,
    ) -> None:
        if name is not None:
            self.name = name
        if slug is not None:
            self.slug = slug
        if category is not None:
            self.category = category
        if model is not None:
            self.model = model
        if summary is not None:
            self.summary = summary
        if description is not None:
            self.description = description
        if specifications is not None:
            self.specifications = specifications
        if cover_image is not None:
            self.cover_image = cover_image
        if price_note is not None:
            self.price_note = price_note
        if status is not None:
            self.status = status
        self.updated_at = datetime.now(UTC)
