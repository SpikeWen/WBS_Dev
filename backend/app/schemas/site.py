from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.article import ArticleStatus
from app.domain.case import CaseStatus
from app.domain.faq import FAQStatus
from app.domain.page import PageStatus
from app.domain.product import ProductStatus
from app.domain.publish import PublishStatus
from app.domain.readiness import ReadinessLevel
from app.domain.service_item import ServiceStatus
from app.domain.site import SiteStatus


class SiteCreateRequest(BaseModel):
    tenant_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    template_id: str = Field(min_length=1)
    domain: str | None = None


class SiteListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    template_id: str
    domain: str | None
    status: SiteStatus
    created_at: datetime
    updated_at: datetime


class SiteUpdateRequest(BaseModel):
    name: str | None = None
    template_id: str | None = None
    domain: str | None = None
    status: SiteStatus | None = None


class SiteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    template_id: str
    domain: str | None
    status: SiteStatus
    created_at: datetime
    updated_at: datetime


class SiteStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    site_id: str
    status: SiteStatus
    missing_fields: list[str]


class SiteProfileRequest(BaseModel):
    site_name: str | None = None
    subtitle: str | None = None
    logo: str | None = None
    favicon: str | None = None
    default_title: str | None = None
    default_description: str | None = None


class SiteProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    site_id: str
    site_name: str
    subtitle: str
    logo: str
    favicon: str
    default_title: str
    default_description: str
    created_at: datetime
    updated_at: datetime


class CompanyProfileRequest(BaseModel):
    company_name: str | None = None
    legal_name: str | None = None
    industry: str | None = None
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    service_area: str | None = None


class CompanyProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    site_id: str
    company_name: str
    legal_name: str
    industry: str
    description: str
    phone: str
    email: str
    address: str
    service_area: str
    created_at: datetime
    updated_at: datetime


class PageCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    h1: str | None = None
    body: str | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    sort_order: int = 0


class PageUpdateRequest(BaseModel):
    title: str | None = None
    slug: str | None = None
    h1: str | None = None
    body: str | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    sort_order: int | None = None
    show_in_nav: bool | None = None
    status: PageStatus | None = None


class PageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class ArticleCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    category: str | None = None
    summary: str | None = None
    body: str | None = None
    cover_image: str | None = None


class ArticleUpdateRequest(BaseModel):
    title: str | None = None
    slug: str | None = None
    category: str | None = None
    summary: str | None = None
    body: str | None = None
    cover_image: str | None = None
    status: ArticleStatus | None = None


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    category: str | None = None
    model: str | None = None
    summary: str | None = None
    description: str | None = None
    specifications: str | None = None
    cover_image: str | None = None
    price_note: str | None = None


class ProductUpdateRequest(BaseModel):
    name: str | None = None
    slug: str | None = None
    category: str | None = None
    model: str | None = None
    summary: str | None = None
    description: str | None = None
    specifications: str | None = None
    cover_image: str | None = None
    price_note: str | None = None
    status: ProductStatus | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class FAQCreateRequest(BaseModel):
    question: str = Field(min_length=1)
    answer: str | None = None
    category: str | None = None
    sort_order: int = 0


class FAQUpdateRequest(BaseModel):
    question: str | None = None
    answer: str | None = None
    category: str | None = None
    sort_order: int | None = None
    status: FAQStatus | None = None


class FAQResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    site_id: str
    question: str
    answer: str
    category: str
    sort_order: int
    status: FAQStatus
    created_at: datetime
    updated_at: datetime


class CaseCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    client_name: str | None = None
    industry: str | None = None
    summary: str | None = None
    challenge: str | None = None
    solution: str | None = None
    result: str | None = None
    cover_image: str | None = None
    project_date: str | None = None


class CaseUpdateRequest(BaseModel):
    title: str | None = None
    slug: str | None = None
    client_name: str | None = None
    industry: str | None = None
    summary: str | None = None
    challenge: str | None = None
    solution: str | None = None
    result: str | None = None
    cover_image: str | None = None
    project_date: str | None = None
    status: CaseStatus | None = None


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class ServiceCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    category: str | None = None
    summary: str | None = None
    scope: str | None = None
    process: str | None = None
    deliverables: str | None = None
    price_note: str | None = None


class ServiceUpdateRequest(BaseModel):
    name: str | None = None
    slug: str | None = None
    category: str | None = None
    summary: str | None = None
    scope: str | None = None
    process: str | None = None
    deliverables: str | None = None
    price_note: str | None = None
    status: ServiceStatus | None = None


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class PublishResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    site_id: str
    version: str
    status: PublishStatus
    preview_url: str
    publish_url: str
    output_path: str
    message: str
    created_at: datetime


class ReadinessIssueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    level: ReadinessLevel
    module: str
    message: str


class PublishReadinessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    site_id: str
    can_publish: bool
    issue_count: int
    issues: list[ReadinessIssueResponse]


class MediaAssetUpdateRequest(BaseModel):
    alt_text: str | None = None


class MediaAssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    site_id: str
    filename: str
    url: str
    alt_text: str
    file_type: str
    size: int
    created_at: datetime
    updated_at: datetime
