from threading import Lock

from app.domain.article import Article
from app.domain.case import CaseStudy
from app.domain.faq import FAQItem
from app.domain.media import MediaAsset
from app.domain.page import ContentPage
from app.domain.product import Product
from app.domain.profile import CompanyProfile, SiteProfile
from app.domain.publish import PublishRecord
from app.domain.repositories import SiteRepository
from app.domain.service_item import ServiceItem
from app.domain.site import Site


class InMemorySiteRepository(SiteRepository):
    def __init__(self) -> None:
        self._items: dict[str, Site] = {}
        self._site_profiles: dict[str, SiteProfile] = {}
        self._company_profiles: dict[str, CompanyProfile] = {}
        self._pages: dict[str, ContentPage] = {}
        self._articles: dict[str, Article] = {}
        self._products: dict[str, Product] = {}
        self._faqs: dict[str, FAQItem] = {}
        self._cases: dict[str, CaseStudy] = {}
        self._services: dict[str, ServiceItem] = {}
        self._publish_records: dict[str, PublishRecord] = {}
        self._assets: dict[str, MediaAsset] = {}
        self._lock = Lock()

    def add(self, site: Site) -> None:
        with self._lock:
            self._items[site.id] = site

    def get(self, site_id: str) -> Site | None:
        with self._lock:
            return self._items.get(site_id)

    def save(self, site: Site) -> None:
        with self._lock:
            self._items[site.id] = site

    def list_sites(self) -> list[Site]:
        with self._lock:
            return list(self._items.values())

    def get_site_profile(self, site_id: str) -> SiteProfile:
        with self._lock:
            profile = self._site_profiles.get(site_id)
            if profile is None:
                profile = SiteProfile(site_id=site_id)
                self._site_profiles[site_id] = profile
            return profile

    def save_site_profile(self, profile: SiteProfile) -> None:
        with self._lock:
            self._site_profiles[profile.site_id] = profile

    def get_company_profile(self, site_id: str) -> CompanyProfile:
        with self._lock:
            profile = self._company_profiles.get(site_id)
            if profile is None:
                profile = CompanyProfile(site_id=site_id)
                self._company_profiles[site_id] = profile
            return profile

    def save_company_profile(self, profile: CompanyProfile) -> None:
        with self._lock:
            self._company_profiles[profile.site_id] = profile

    def list_pages(self, site_id: str) -> list[ContentPage]:
        with self._lock:
            return sorted(
                [page for page in self._pages.values() if page.site_id == site_id],
                key=lambda page: (page.sort_order, page.created_at),
            )

    def add_page(self, page: ContentPage) -> None:
        with self._lock:
            self._pages[page.id] = page

    def get_page(self, page_id: str) -> ContentPage | None:
        with self._lock:
            return self._pages.get(page_id)

    def get_page_by_slug(self, site_id: str, slug: str) -> ContentPage | None:
        with self._lock:
            for page in self._pages.values():
                if page.site_id == site_id and page.slug == slug:
                    return page
            return None

    def save_page(self, page: ContentPage) -> None:
        with self._lock:
            self._pages[page.id] = page

    def delete_page(self, page_id: str) -> None:
        with self._lock:
            self._pages.pop(page_id, None)

    def list_articles(self, site_id: str) -> list[Article]:
        with self._lock:
            return sorted(
                [article for article in self._articles.values() if article.site_id == site_id],
                key=lambda article: article.created_at,
                reverse=True,
            )

    def add_article(self, article: Article) -> None:
        with self._lock:
            self._articles[article.id] = article

    def get_article(self, article_id: str) -> Article | None:
        with self._lock:
            return self._articles.get(article_id)

    def save_article(self, article: Article) -> None:
        with self._lock:
            self._articles[article.id] = article

    def delete_article(self, article_id: str) -> None:
        with self._lock:
            self._articles.pop(article_id, None)

    def list_products(self, site_id: str) -> list[Product]:
        with self._lock:
            return sorted(
                [product for product in self._products.values() if product.site_id == site_id],
                key=lambda product: product.created_at,
                reverse=True,
            )

    def add_product(self, product: Product) -> None:
        with self._lock:
            self._products[product.id] = product

    def get_product(self, product_id: str) -> Product | None:
        with self._lock:
            return self._products.get(product_id)

    def save_product(self, product: Product) -> None:
        with self._lock:
            self._products[product.id] = product

    def delete_product(self, product_id: str) -> None:
        with self._lock:
            self._products.pop(product_id, None)

    def list_faqs(self, site_id: str) -> list[FAQItem]:
        with self._lock:
            return sorted(
                [faq for faq in self._faqs.values() if faq.site_id == site_id],
                key=lambda faq: (faq.sort_order, faq.created_at),
            )

    def add_faq(self, faq: FAQItem) -> None:
        with self._lock:
            self._faqs[faq.id] = faq

    def get_faq(self, faq_id: str) -> FAQItem | None:
        with self._lock:
            return self._faqs.get(faq_id)

    def save_faq(self, faq: FAQItem) -> None:
        with self._lock:
            self._faqs[faq.id] = faq

    def delete_faq(self, faq_id: str) -> None:
        with self._lock:
            self._faqs.pop(faq_id, None)

    def list_cases(self, site_id: str) -> list[CaseStudy]:
        with self._lock:
            return sorted(
                [case for case in self._cases.values() if case.site_id == site_id],
                key=lambda case: case.created_at,
                reverse=True,
            )

    def add_case(self, case: CaseStudy) -> None:
        with self._lock:
            self._cases[case.id] = case

    def get_case(self, case_id: str) -> CaseStudy | None:
        with self._lock:
            return self._cases.get(case_id)

    def save_case(self, case: CaseStudy) -> None:
        with self._lock:
            self._cases[case.id] = case

    def delete_case(self, case_id: str) -> None:
        with self._lock:
            self._cases.pop(case_id, None)

    def list_services(self, site_id: str) -> list[ServiceItem]:
        with self._lock:
            return sorted(
                [service for service in self._services.values() if service.site_id == site_id],
                key=lambda service: service.created_at,
                reverse=True,
            )

    def add_service(self, service: ServiceItem) -> None:
        with self._lock:
            self._services[service.id] = service

    def get_service(self, service_id: str) -> ServiceItem | None:
        with self._lock:
            return self._services.get(service_id)

    def save_service(self, service: ServiceItem) -> None:
        with self._lock:
            self._services[service.id] = service

    def delete_service(self, service_id: str) -> None:
        with self._lock:
            self._services.pop(service_id, None)

    def add_publish_record(self, record: PublishRecord) -> None:
        with self._lock:
            self._publish_records[record.id] = record

    def list_publish_records(self, site_id: str) -> list[PublishRecord]:
        with self._lock:
            return sorted(
                [record for record in self._publish_records.values() if record.site_id == site_id],
                key=lambda record: record.created_at,
                reverse=True,
            )

    def list_assets(self, site_id: str) -> list[MediaAsset]:
        with self._lock:
            return sorted(
                [asset for asset in self._assets.values() if asset.site_id == site_id],
                key=lambda asset: asset.created_at,
                reverse=True,
            )

    def add_asset(self, asset: MediaAsset) -> None:
        with self._lock:
            self._assets[asset.id] = asset

    def get_asset(self, asset_id: str) -> MediaAsset | None:
        with self._lock:
            return self._assets.get(asset_id)

    def save_asset(self, asset: MediaAsset) -> None:
        with self._lock:
            self._assets[asset.id] = asset

    def delete_asset(self, asset_id: str) -> None:
        with self._lock:
            self._assets.pop(asset_id, None)
