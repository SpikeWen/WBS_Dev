from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import HTMLResponse

from app.api.dependencies import get_site_service
from app.application.site_service import SiteApplicationService
from app.infrastructure.site_preview_renderer import render_focused_preview, render_site_preview
from app.schemas.site import (
    ArticleCreateRequest,
    ArticleResponse,
    ArticleUpdateRequest,
    CaseCreateRequest,
    CaseResponse,
    CaseUpdateRequest,
    CompanyProfileRequest,
    CompanyProfileResponse,
    FAQCreateRequest,
    FAQResponse,
    FAQUpdateRequest,
    MediaAssetResponse,
    MediaAssetUpdateRequest,
    PageCreateRequest,
    PageResponse,
    PageUpdateRequest,
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
    PublishReadinessResponse,
    PublishResponse,
    ServiceCreateRequest,
    ServiceResponse,
    ServiceUpdateRequest,
    SiteCreateRequest,
    SiteListResponse,
    SiteProfileRequest,
    SiteProfileResponse,
    SiteResponse,
    SiteStatusResponse,
    SiteUpdateRequest,
)

router = APIRouter(tags=["sites"])
EXPORTS_DIR = Path(__file__).resolve().parents[3] / "exports"
STORAGE_DIR = Path(__file__).resolve().parents[3] / "storage"


@router.post("/sites", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
def create_site(
    payload: SiteCreateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> SiteResponse:
    site = service.create_site(payload)
    return SiteResponse.model_validate(site)


@router.get("/sites", response_model=list[SiteListResponse])
def list_sites(
    service: SiteApplicationService = Depends(get_site_service),
) -> list[SiteListResponse]:
    return [SiteListResponse.model_validate(site) for site in service.list_sites()]


@router.get("/sites/{site_id}", response_model=SiteResponse)
def get_site(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> SiteResponse:
    site = service.get_site(site_id)
    if site is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return SiteResponse.model_validate(site)


@router.patch("/sites/{site_id}", response_model=SiteResponse)
def update_site(
    site_id: str,
    payload: SiteUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> SiteResponse:
    site = service.update_site(site_id, payload)
    if site is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return SiteResponse.model_validate(site)


@router.get("/sites/{site_id}/status", response_model=SiteStatusResponse)
def get_site_status(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> SiteStatusResponse:
    status_model = service.get_site_status(site_id)
    if status_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return SiteStatusResponse.model_validate(status_model)


@router.get("/sites/{site_id}/profile", response_model=SiteProfileResponse)
def get_site_profile(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> SiteProfileResponse:
    profile = service.get_site_profile(site_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return SiteProfileResponse.model_validate(profile)


@router.put("/sites/{site_id}/profile", response_model=SiteProfileResponse)
def update_site_profile(
    site_id: str,
    payload: SiteProfileRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> SiteProfileResponse:
    profile = service.update_site_profile(site_id, payload)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return SiteProfileResponse.model_validate(profile)


@router.get("/sites/{site_id}/company-profile", response_model=CompanyProfileResponse)
def get_company_profile(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> CompanyProfileResponse:
    profile = service.get_company_profile(site_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return CompanyProfileResponse.model_validate(profile)


@router.put("/sites/{site_id}/company-profile", response_model=CompanyProfileResponse)
def update_company_profile(
    site_id: str,
    payload: CompanyProfileRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> CompanyProfileResponse:
    profile = service.update_company_profile(site_id, payload)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return CompanyProfileResponse.model_validate(profile)


@router.get("/sites/{site_id}/pages", response_model=list[PageResponse])
def list_pages(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[PageResponse]:
    pages = service.list_pages(site_id)
    if pages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [PageResponse.model_validate(page) for page in pages]


@router.post("/sites/{site_id}/pages", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def create_page(
    site_id: str,
    payload: PageCreateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> PageResponse:
    page = service.create_page(site_id, payload)
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return PageResponse.model_validate(page)


@router.patch("/pages/{page_id}", response_model=PageResponse)
def update_page(
    page_id: str,
    payload: PageUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> PageResponse:
    page = service.update_page(page_id, payload)
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="page not found")
    return PageResponse.model_validate(page)


@router.delete("/pages/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_page(
    page_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> None:
    if not service.delete_page(page_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="page not found")


@router.get("/sites/{site_id}/articles", response_model=list[ArticleResponse])
def list_articles(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[ArticleResponse]:
    articles = service.list_articles(site_id)
    if articles is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [ArticleResponse.model_validate(article) for article in articles]


@router.post("/sites/{site_id}/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    site_id: str,
    payload: ArticleCreateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> ArticleResponse:
    article = service.create_article(site_id, payload)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return ArticleResponse.model_validate(article)


@router.patch("/articles/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: str,
    payload: ArticleUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> ArticleResponse:
    article = service.update_article(article_id, payload)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="article not found")
    return ArticleResponse.model_validate(article)


@router.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> None:
    if not service.delete_article(article_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="article not found")


@router.get("/sites/{site_id}/products", response_model=list[ProductResponse])
def list_products(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[ProductResponse]:
    products = service.list_products(site_id)
    if products is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [ProductResponse.model_validate(product) for product in products]


@router.post("/sites/{site_id}/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    site_id: str,
    payload: ProductCreateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> ProductResponse:
    product = service.create_product(site_id, payload)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return ProductResponse.model_validate(product)


@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> ProductResponse:
    product = service.update_product(product_id, payload)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return ProductResponse.model_validate(product)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> None:
    if not service.delete_product(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")


@router.get("/sites/{site_id}/faqs", response_model=list[FAQResponse])
def list_faqs(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[FAQResponse]:
    faqs = service.list_faqs(site_id)
    if faqs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [FAQResponse.model_validate(faq) for faq in faqs]


@router.post("/sites/{site_id}/faqs", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
def create_faq(
    site_id: str,
    payload: FAQCreateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> FAQResponse:
    faq = service.create_faq(site_id, payload)
    if faq is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return FAQResponse.model_validate(faq)


@router.patch("/faqs/{faq_id}", response_model=FAQResponse)
def update_faq(
    faq_id: str,
    payload: FAQUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> FAQResponse:
    faq = service.update_faq(faq_id, payload)
    if faq is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="faq not found")
    return FAQResponse.model_validate(faq)


@router.delete("/faqs/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(
    faq_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> None:
    if not service.delete_faq(faq_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="faq not found")


@router.get("/sites/{site_id}/cases", response_model=list[CaseResponse])
def list_cases(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[CaseResponse]:
    cases = service.list_cases(site_id)
    if cases is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [CaseResponse.model_validate(case) for case in cases]


@router.post("/sites/{site_id}/cases", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    site_id: str,
    payload: CaseCreateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> CaseResponse:
    case = service.create_case(site_id, payload)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return CaseResponse.model_validate(case)


@router.patch("/cases/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: str,
    payload: CaseUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> CaseResponse:
    case = service.update_case(case_id, payload)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="case not found")
    return CaseResponse.model_validate(case)


@router.delete("/cases/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(
    case_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> None:
    if not service.delete_case(case_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="case not found")


@router.get("/sites/{site_id}/services", response_model=list[ServiceResponse])
def list_services(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[ServiceResponse]:
    services = service.list_services(site_id)
    if services is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [ServiceResponse.model_validate(item) for item in services]


@router.post("/sites/{site_id}/services", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    site_id: str,
    payload: ServiceCreateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> ServiceResponse:
    item = service.create_service(site_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return ServiceResponse.model_validate(item)


@router.patch("/services/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: str,
    payload: ServiceUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> ServiceResponse:
    item = service.update_service(service_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="service not found")
    return ServiceResponse.model_validate(item)


@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> None:
    if not service.delete_service(service_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="service not found")


@router.get("/sites/{site_id}/preview", response_class=HTMLResponse)
def preview_site(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_site_preview(site_id, service)


@router.get("/sites/{site_id}/preview/pages/{slug}", response_class=HTMLResponse)
def preview_page(
    site_id: str,
    slug: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_site_preview(site_id, service, active_slug=slug)


@router.get("/sites/{site_id}/preview/articles/{slug}", response_class=HTMLResponse)
def preview_article(
    site_id: str,
    slug: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_site_preview(site_id, service, active_content=("articles", slug))


@router.get("/sites/{site_id}/preview/products/{slug}", response_class=HTMLResponse)
def preview_product(
    site_id: str,
    slug: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_site_preview(site_id, service, active_content=("products", slug))


@router.get("/sites/{site_id}/preview/cases/{slug}", response_class=HTMLResponse)
def preview_case(
    site_id: str,
    slug: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_site_preview(site_id, service, active_content=("cases", slug))


@router.get("/sites/{site_id}/preview/services/{slug}", response_class=HTMLResponse)
def preview_service(
    site_id: str,
    slug: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_site_preview(site_id, service, active_content=("services", slug))


@router.get("/sites/{site_id}/preview/focus/{section}", response_class=HTMLResponse)
def preview_focused_section(
    site_id: str,
    section: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_focused_preview(site_id, section, None, service)


@router.get("/sites/{site_id}/preview/focus/{section}/{slug}", response_class=HTMLResponse)
def preview_focused_item(
    site_id: str,
    section: str,
    slug: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> HTMLResponse:
    return _render_focused_preview(site_id, section, slug, service)


def _render_site_preview(
    site_id: str,
    service: SiteApplicationService,
    active_slug: str | None = None,
    active_content: tuple[str, str] | None = None,
    static_links: bool = False,
) -> HTMLResponse:
    content = service.get_site_content(site_id)
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    html = render_site_preview(
        content,
        active_slug=active_slug,
        active_content=active_content,
        static_links=static_links,
    )
    if not html:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content not found")
    return HTMLResponse(content=html)


def _render_focused_preview(
    site_id: str,
    section: str,
    slug: str | None,
    service: SiteApplicationService,
) -> HTMLResponse:
    content = service.get_site_content(site_id)
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    html = render_focused_preview(content, section=section, slug=slug)
    if not html:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content not found")
    return HTMLResponse(content=html)


@router.post("/sites/{site_id}/publish", response_model=PublishResponse)
def publish_site(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> PublishResponse:
    content = service.get_site_content(site_id)
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    version = datetime.now(UTC).strftime("v%Y%m%d%H%M%S")
    output_dir = EXPORTS_DIR / site_id / version
    output_dir.mkdir(parents=True, exist_ok=True)
    html = render_site_preview(content, static_links=True)
    output_file = output_dir / "index.html"
    output_file.write_text(html, encoding="utf-8")
    for page in content.pages:
        if page.status == "hidden":
            continue
        page_dir = output_dir / page.slug
        page_dir.mkdir(parents=True, exist_ok=True)
        page_html = render_site_preview(
            content,
            active_slug=page.slug,
            static_links=True,
        )
        (page_dir / "index.html").write_text(page_html, encoding="utf-8")
    for section, items in (
        ("articles", content.articles),
        ("products", content.products),
        ("cases", content.cases),
        ("services", content.services),
    ):
        for item in items:
            if item.status == "hidden":
                continue
            item_dir = output_dir / section / item.slug
            item_dir.mkdir(parents=True, exist_ok=True)
            item_html = render_site_preview(
                content,
                active_content=(section, item.slug),
                static_links=True,
            )
            (item_dir / "index.html").write_text(item_html, encoding="utf-8")
    publish_url = f"/published/{site_id}/{version}/index.html"
    record = service.create_publish_record(
        site_id=site_id,
        version=version,
        publish_url=publish_url,
        output_path=str(output_file),
        message="published static preview",
    )
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return PublishResponse.model_validate(record)


@router.get("/sites/{site_id}/publish-readiness", response_model=PublishReadinessResponse)
def get_publish_readiness(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> PublishReadinessResponse:
    readiness = service.get_publish_readiness(site_id)
    if readiness is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return PublishReadinessResponse.model_validate(readiness)


@router.get("/sites/{site_id}/publishes", response_model=list[PublishResponse])
def list_publishes(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[PublishResponse]:
    records = service.list_publish_records(site_id)
    if records is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [PublishResponse.model_validate(record) for record in records]


@router.get("/sites/{site_id}/assets", response_model=list[MediaAssetResponse])
def list_assets(
    site_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> list[MediaAssetResponse]:
    assets = service.list_assets(site_id)
    if assets is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return [MediaAssetResponse.model_validate(asset) for asset in assets]


@router.post("/sites/{site_id}/assets", response_model=MediaAssetResponse, status_code=status.HTTP_201_CREATED)
async def upload_asset(
    site_id: str,
    file: UploadFile = File(...),
    alt_text: str = Form(""),
    service: SiteApplicationService = Depends(get_site_service),
) -> MediaAssetResponse:
    site = service.get_site(site_id)
    if site is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    raw = await file.read()
    safe_name = Path(file.filename or "asset").name.replace(" ", "_")
    stored_name = f"{uuid4().hex}_{safe_name}"
    site_asset_dir = STORAGE_DIR / "sites" / site_id / "assets"
    site_asset_dir.mkdir(parents=True, exist_ok=True)
    output_file = site_asset_dir / stored_name
    output_file.write_bytes(raw)
    url = f"/storage/sites/{site_id}/assets/{stored_name}"
    asset = service.create_asset(
        site_id=site_id,
        filename=safe_name,
        url=url,
        alt_text=alt_text,
        file_type=file.content_type or "application/octet-stream",
        size=len(raw),
    )
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="site not found")
    return MediaAssetResponse.model_validate(asset)


@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: str,
    service: SiteApplicationService = Depends(get_site_service),
) -> None:
    asset = service.get_asset(asset_id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="asset not found")
    storage_prefix = "/storage/"
    if asset.url.startswith(storage_prefix):
        storage_path = STORAGE_DIR / asset.url.removeprefix(storage_prefix)
        try:
            storage_path.unlink(missing_ok=True)
        except OSError:
            pass
    service.delete_asset(asset_id)


@router.patch("/assets/{asset_id}", response_model=MediaAssetResponse)
def update_asset(
    asset_id: str,
    payload: MediaAssetUpdateRequest,
    service: SiteApplicationService = Depends(get_site_service),
) -> MediaAssetResponse:
    asset = service.update_asset(asset_id, payload)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="asset not found")
    return MediaAssetResponse.model_validate(asset)
