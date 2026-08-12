from app.domain.article import Article
from app.domain.case import CaseStudy
from app.domain.faq import FAQItem
from app.domain.media import MediaAsset
from app.domain.page import ContentPage
from app.domain.product import Product
from app.domain.profile import CompanyProfile, SiteProfile
from app.domain.publish import PublishRecord, PublishStatus
from app.domain.readiness import ReadinessIssue, ReadinessLevel, SitePublishReadiness
from app.domain.repositories import SiteRepository
from app.domain.service_item import ServiceItem
from app.domain.site import Site, SiteStatus, SiteStatusView
from app.domain.site_content import SiteContent
from app.schemas.site import (
    CompanyProfileRequest,
    ArticleCreateRequest,
    ArticleUpdateRequest,
    CaseCreateRequest,
    CaseUpdateRequest,
    PageCreateRequest,
    PageUpdateRequest,
    FAQCreateRequest,
    FAQUpdateRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
    MediaAssetUpdateRequest,
    ServiceCreateRequest,
    ServiceUpdateRequest,
    SiteCreateRequest,
    SiteProfileRequest,
    SiteUpdateRequest,
)


class SiteApplicationService:
    def __init__(self, repository: SiteRepository) -> None:
        self._repository = repository

    def create_site(self, payload: SiteCreateRequest) -> Site:
        site = Site.create(
            tenant_id=payload.tenant_id,
            name=payload.name,
            template_id=payload.template_id,
            domain=payload.domain,
        )
        self._repository.add(site)
        return site

    def get_site(self, site_id: str) -> Site | None:
        return self._repository.get(site_id)

    def list_sites(self) -> list[Site]:
        return self._repository.list_sites()

    def update_site(self, site_id: str, payload: SiteUpdateRequest) -> Site | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        site.update(
            name=payload.name,
            template_id=payload.template_id,
            domain=payload.domain,
            status=payload.status,
        )
        self._repository.save(site)
        return site

    def get_site_status(self, site_id: str) -> SiteStatusView | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return SiteStatusView(
            site_id=site.id,
            status=site.status,
            missing_fields=site.missing_fields(),
        )

    def get_site_content(self, site_id: str) -> SiteContent | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return SiteContent(
            site=site,
            site_profile=self._repository.get_site_profile(site_id),
            company_profile=self._repository.get_company_profile(site_id),
            pages=self._repository.list_pages(site_id),
            articles=self._repository.list_articles(site_id),
            products=self._repository.list_products(site_id),
            faqs=self._repository.list_faqs(site_id),
            cases=self._repository.list_cases(site_id),
            services=self._repository.list_services(site_id),
        )

    def get_publish_readiness(self, site_id: str) -> SitePublishReadiness | None:
        content = self.get_site_content(site_id)
        if content is None:
            return None
        issues: list[ReadinessIssue] = []
        site_profile = content.site_profile
        company_profile = content.company_profile
        published_pages = [page for page in content.pages if page.status.value == "published"]
        published_articles = [article for article in content.articles if article.status.value == "published"]
        published_products = [product for product in content.products if product.status.value == "published"]
        published_cases = [case for case in content.cases if case.status.value == "published"]
        published_services = [service for service in content.services if service.status.value == "published"]
        published_faqs = [faq for faq in content.faqs if faq.status.value == "published"]

        if not content.site.name.strip():
            issues.append(ReadinessIssue(ReadinessLevel.ERROR, "site", "站点名称为空"))
        if not content.site.template_id.strip():
            issues.append(ReadinessIssue(ReadinessLevel.ERROR, "site", "模板 ID 为空"))
        if not site_profile.site_name.strip():
            issues.append(ReadinessIssue(ReadinessLevel.WARNING, "site_profile", "前台名称未填写"))
        if not site_profile.default_title.strip():
            issues.append(ReadinessIssue(ReadinessLevel.WARNING, "site_profile", "默认标题未填写"))
        if not company_profile.company_name.strip():
            issues.append(ReadinessIssue(ReadinessLevel.WARNING, "company_profile", "企业名称未填写"))
        if not company_profile.description.strip():
            issues.append(ReadinessIssue(ReadinessLevel.WARNING, "company_profile", "企业介绍未填写"))
        if not (company_profile.phone.strip() or company_profile.email.strip()):
            issues.append(ReadinessIssue(ReadinessLevel.WARNING, "company_profile", "电话或邮箱至少建议填写一个"))
        if not published_pages:
            issues.append(ReadinessIssue(ReadinessLevel.WARNING, "pages", "还没有已发布的固定页面"))
        if not published_services:
            issues.append(ReadinessIssue(ReadinessLevel.INFO, "services", "还没有已发布的服务项目"))
        if not published_products:
            issues.append(ReadinessIssue(ReadinessLevel.INFO, "products", "还没有已发布的产品"))
        if not published_cases:
            issues.append(ReadinessIssue(ReadinessLevel.INFO, "cases", "还没有已发布的案例"))
        if not published_articles:
            issues.append(ReadinessIssue(ReadinessLevel.INFO, "articles", "还没有已发布的文章"))
        if not published_faqs:
            issues.append(ReadinessIssue(ReadinessLevel.INFO, "faqs", "还没有已发布的 FAQ"))

        error_count = sum(1 for issue in issues if issue.level == ReadinessLevel.ERROR)
        return SitePublishReadiness(
            site_id=site_id,
            can_publish=error_count == 0,
            issue_count=len(issues),
            issues=issues,
        )

    def get_site_profile(self, site_id: str) -> SiteProfile | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.get_site_profile(site_id)

    def update_site_profile(
        self,
        site_id: str,
        payload: SiteProfileRequest,
    ) -> SiteProfile | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        profile = self._repository.get_site_profile(site_id)
        profile.update(
            site_name=payload.site_name,
            subtitle=payload.subtitle,
            logo=payload.logo,
            favicon=payload.favicon,
            default_title=payload.default_title,
            default_description=payload.default_description,
        )
        self._repository.save_site_profile(profile)
        return profile

    def get_company_profile(self, site_id: str) -> CompanyProfile | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.get_company_profile(site_id)

    def update_company_profile(
        self,
        site_id: str,
        payload: CompanyProfileRequest,
    ) -> CompanyProfile | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        profile = self._repository.get_company_profile(site_id)
        profile.update(
            company_name=payload.company_name,
            legal_name=payload.legal_name,
            industry=payload.industry,
            description=payload.description,
            phone=payload.phone,
            email=payload.email,
            address=payload.address,
            service_area=payload.service_area,
        )
        self._repository.save_company_profile(profile)
        return profile

    def list_pages(self, site_id: str) -> list[ContentPage] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_pages(site_id)

    def create_page(self, site_id: str, payload: PageCreateRequest) -> ContentPage | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        page = ContentPage.create(
            site_id=site_id,
            title=payload.title,
            slug=payload.slug,
            h1=payload.h1 or payload.title,
            body=payload.body or "",
            meta_title=payload.meta_title or payload.title,
            meta_description=payload.meta_description or "",
            sort_order=payload.sort_order,
        )
        self._repository.add_page(page)
        return page

    def update_page(self, page_id: str, payload: PageUpdateRequest) -> ContentPage | None:
        page = self._repository.get_page(page_id)
        if page is None:
            return None
        page.update(
            title=payload.title,
            slug=payload.slug,
            h1=payload.h1,
            body=payload.body,
            meta_title=payload.meta_title,
            meta_description=payload.meta_description,
            sort_order=payload.sort_order,
            show_in_nav=payload.show_in_nav,
            status=payload.status,
        )
        self._repository.save_page(page)
        return page

    def delete_page(self, page_id: str) -> bool:
        page = self._repository.get_page(page_id)
        if page is None:
            return False
        self._repository.delete_page(page_id)
        return True

    def get_page_by_slug(self, site_id: str, slug: str) -> ContentPage | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.get_page_by_slug(site_id, slug)

    def list_articles(self, site_id: str) -> list[Article] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_articles(site_id)

    def create_article(self, site_id: str, payload: ArticleCreateRequest) -> Article | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        article = Article.create(
            site_id=site_id,
            title=payload.title,
            slug=payload.slug,
            category=payload.category or "",
            summary=payload.summary or "",
            body=payload.body or "",
            cover_image=payload.cover_image or "",
        )
        self._repository.add_article(article)
        return article

    def update_article(self, article_id: str, payload: ArticleUpdateRequest) -> Article | None:
        article = self._repository.get_article(article_id)
        if article is None:
            return None
        article.update(
            title=payload.title,
            slug=payload.slug,
            category=payload.category,
            summary=payload.summary,
            body=payload.body,
            cover_image=payload.cover_image,
            status=payload.status,
        )
        self._repository.save_article(article)
        return article

    def delete_article(self, article_id: str) -> bool:
        article = self._repository.get_article(article_id)
        if article is None:
            return False
        self._repository.delete_article(article_id)
        return True

    def list_products(self, site_id: str) -> list[Product] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_products(site_id)

    def create_product(self, site_id: str, payload: ProductCreateRequest) -> Product | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        product = Product.create(
            site_id=site_id,
            name=payload.name,
            slug=payload.slug,
            category=payload.category or "",
            model=payload.model or "",
            summary=payload.summary or "",
            description=payload.description or "",
            specifications=payload.specifications or "",
            cover_image=payload.cover_image or "",
            price_note=payload.price_note or "",
        )
        self._repository.add_product(product)
        return product

    def update_product(self, product_id: str, payload: ProductUpdateRequest) -> Product | None:
        product = self._repository.get_product(product_id)
        if product is None:
            return None
        product.update(
            name=payload.name,
            slug=payload.slug,
            category=payload.category,
            model=payload.model,
            summary=payload.summary,
            description=payload.description,
            specifications=payload.specifications,
            cover_image=payload.cover_image,
            price_note=payload.price_note,
            status=payload.status,
        )
        self._repository.save_product(product)
        return product

    def delete_product(self, product_id: str) -> bool:
        product = self._repository.get_product(product_id)
        if product is None:
            return False
        self._repository.delete_product(product_id)
        return True

    def list_faqs(self, site_id: str) -> list[FAQItem] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_faqs(site_id)

    def create_faq(self, site_id: str, payload: FAQCreateRequest) -> FAQItem | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        faq = FAQItem.create(
            site_id=site_id,
            question=payload.question,
            answer=payload.answer or "",
            category=payload.category or "",
            sort_order=payload.sort_order,
        )
        self._repository.add_faq(faq)
        return faq

    def update_faq(self, faq_id: str, payload: FAQUpdateRequest) -> FAQItem | None:
        faq = self._repository.get_faq(faq_id)
        if faq is None:
            return None
        faq.update(
            question=payload.question,
            answer=payload.answer,
            category=payload.category,
            sort_order=payload.sort_order,
            status=payload.status,
        )
        self._repository.save_faq(faq)
        return faq

    def delete_faq(self, faq_id: str) -> bool:
        faq = self._repository.get_faq(faq_id)
        if faq is None:
            return False
        self._repository.delete_faq(faq_id)
        return True

    def list_cases(self, site_id: str) -> list[CaseStudy] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_cases(site_id)

    def create_case(self, site_id: str, payload: CaseCreateRequest) -> CaseStudy | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        case = CaseStudy.create(
            site_id=site_id,
            title=payload.title,
            slug=payload.slug,
            client_name=payload.client_name or "",
            industry=payload.industry or "",
            summary=payload.summary or "",
            challenge=payload.challenge or "",
            solution=payload.solution or "",
            result=payload.result or "",
            cover_image=payload.cover_image or "",
            project_date=payload.project_date or "",
        )
        self._repository.add_case(case)
        return case

    def update_case(self, case_id: str, payload: CaseUpdateRequest) -> CaseStudy | None:
        case = self._repository.get_case(case_id)
        if case is None:
            return None
        case.update(
            title=payload.title,
            slug=payload.slug,
            client_name=payload.client_name,
            industry=payload.industry,
            summary=payload.summary,
            challenge=payload.challenge,
            solution=payload.solution,
            result=payload.result,
            cover_image=payload.cover_image,
            project_date=payload.project_date,
            status=payload.status,
        )
        self._repository.save_case(case)
        return case

    def delete_case(self, case_id: str) -> bool:
        case = self._repository.get_case(case_id)
        if case is None:
            return False
        self._repository.delete_case(case_id)
        return True

    def list_services(self, site_id: str) -> list[ServiceItem] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_services(site_id)

    def create_service(self, site_id: str, payload: ServiceCreateRequest) -> ServiceItem | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        service = ServiceItem.create(
            site_id=site_id,
            name=payload.name,
            slug=payload.slug,
            category=payload.category or "",
            summary=payload.summary or "",
            scope=payload.scope or "",
            process=payload.process or "",
            deliverables=payload.deliverables or "",
            price_note=payload.price_note or "",
        )
        self._repository.add_service(service)
        return service

    def update_service(self, service_id: str, payload: ServiceUpdateRequest) -> ServiceItem | None:
        service = self._repository.get_service(service_id)
        if service is None:
            return None
        service.update(
            name=payload.name,
            slug=payload.slug,
            category=payload.category,
            summary=payload.summary,
            scope=payload.scope,
            process=payload.process,
            deliverables=payload.deliverables,
            price_note=payload.price_note,
            status=payload.status,
        )
        self._repository.save_service(service)
        return service

    def delete_service(self, service_id: str) -> bool:
        service = self._repository.get_service(service_id)
        if service is None:
            return False
        self._repository.delete_service(service_id)
        return True

    def create_publish_record(
        self,
        site_id: str,
        version: str,
        publish_url: str,
        output_path: str,
        message: str,
    ) -> PublishRecord | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        record = PublishRecord.create(
            site_id=site_id,
            version=version,
            status=PublishStatus.SUCCESS,
            preview_url=f"/api/sites/{site_id}/preview",
            publish_url=publish_url,
            output_path=output_path,
            message=message,
        )
        self._repository.add_publish_record(record)
        return record

    def list_publish_records(self, site_id: str) -> list[PublishRecord] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_publish_records(site_id)

    def list_assets(self, site_id: str) -> list[MediaAsset] | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        return self._repository.list_assets(site_id)

    def get_asset(self, asset_id: str) -> MediaAsset | None:
        return self._repository.get_asset(asset_id)

    def create_asset(
        self,
        site_id: str,
        filename: str,
        url: str,
        alt_text: str,
        file_type: str,
        size: int,
    ) -> MediaAsset | None:
        site = self._repository.get(site_id)
        if site is None:
            return None
        asset = MediaAsset.create(
            site_id=site_id,
            filename=filename,
            url=url,
            alt_text=alt_text,
            file_type=file_type,
            size=size,
        )
        self._repository.add_asset(asset)
        return asset

    def update_asset(self, asset_id: str, payload: MediaAssetUpdateRequest) -> MediaAsset | None:
        asset = self._repository.get_asset(asset_id)
        if asset is None:
            return None
        asset.update(alt_text=payload.alt_text)
        self._repository.save_asset(asset)
        return asset

    def delete_asset(self, asset_id: str) -> bool:
        asset = self._repository.get_asset(asset_id)
        if asset is None:
            return False
        self._repository.delete_asset(asset_id)
        return True
