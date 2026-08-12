from typing import Protocol

from app.domain.article import Article
from app.domain.case import CaseStudy
from app.domain.faq import FAQItem
from app.domain.media import MediaAsset
from app.domain.page import ContentPage
from app.domain.product import Product
from app.domain.profile import CompanyProfile, SiteProfile
from app.domain.publish import PublishRecord
from app.domain.service_item import ServiceItem
from app.domain.site import Site


class SiteRepository(Protocol):
    def add(self, site: Site) -> None:
        raise NotImplementedError

    def get(self, site_id: str) -> Site | None:
        raise NotImplementedError

    def save(self, site: Site) -> None:
        raise NotImplementedError

    def list_sites(self) -> list[Site]:
        raise NotImplementedError

    def get_site_profile(self, site_id: str) -> SiteProfile:
        raise NotImplementedError

    def save_site_profile(self, profile: SiteProfile) -> None:
        raise NotImplementedError

    def get_company_profile(self, site_id: str) -> CompanyProfile:
        raise NotImplementedError

    def save_company_profile(self, profile: CompanyProfile) -> None:
        raise NotImplementedError

    def list_pages(self, site_id: str) -> list[ContentPage]:
        raise NotImplementedError

    def add_page(self, page: ContentPage) -> None:
        raise NotImplementedError

    def get_page(self, page_id: str) -> ContentPage | None:
        raise NotImplementedError

    def get_page_by_slug(self, site_id: str, slug: str) -> ContentPage | None:
        raise NotImplementedError

    def save_page(self, page: ContentPage) -> None:
        raise NotImplementedError

    def delete_page(self, page_id: str) -> None:
        raise NotImplementedError

    def list_articles(self, site_id: str) -> list[Article]:
        raise NotImplementedError

    def add_article(self, article: Article) -> None:
        raise NotImplementedError

    def get_article(self, article_id: str) -> Article | None:
        raise NotImplementedError

    def save_article(self, article: Article) -> None:
        raise NotImplementedError

    def delete_article(self, article_id: str) -> None:
        raise NotImplementedError

    def list_products(self, site_id: str) -> list[Product]:
        raise NotImplementedError

    def add_product(self, product: Product) -> None:
        raise NotImplementedError

    def get_product(self, product_id: str) -> Product | None:
        raise NotImplementedError

    def save_product(self, product: Product) -> None:
        raise NotImplementedError

    def delete_product(self, product_id: str) -> None:
        raise NotImplementedError

    def list_faqs(self, site_id: str) -> list[FAQItem]:
        raise NotImplementedError

    def add_faq(self, faq: FAQItem) -> None:
        raise NotImplementedError

    def get_faq(self, faq_id: str) -> FAQItem | None:
        raise NotImplementedError

    def save_faq(self, faq: FAQItem) -> None:
        raise NotImplementedError

    def delete_faq(self, faq_id: str) -> None:
        raise NotImplementedError

    def list_cases(self, site_id: str) -> list[CaseStudy]:
        raise NotImplementedError

    def add_case(self, case: CaseStudy) -> None:
        raise NotImplementedError

    def get_case(self, case_id: str) -> CaseStudy | None:
        raise NotImplementedError

    def save_case(self, case: CaseStudy) -> None:
        raise NotImplementedError

    def delete_case(self, case_id: str) -> None:
        raise NotImplementedError

    def list_services(self, site_id: str) -> list[ServiceItem]:
        raise NotImplementedError

    def add_service(self, service: ServiceItem) -> None:
        raise NotImplementedError

    def get_service(self, service_id: str) -> ServiceItem | None:
        raise NotImplementedError

    def save_service(self, service: ServiceItem) -> None:
        raise NotImplementedError

    def delete_service(self, service_id: str) -> None:
        raise NotImplementedError

    def add_publish_record(self, record: PublishRecord) -> None:
        raise NotImplementedError

    def list_publish_records(self, site_id: str) -> list[PublishRecord]:
        raise NotImplementedError

    def list_assets(self, site_id: str) -> list[MediaAsset]:
        raise NotImplementedError

    def add_asset(self, asset: MediaAsset) -> None:
        raise NotImplementedError

    def get_asset(self, asset_id: str) -> MediaAsset | None:
        raise NotImplementedError

    def save_asset(self, asset: MediaAsset) -> None:
        raise NotImplementedError

    def delete_asset(self, asset_id: str) -> None:
        raise NotImplementedError
