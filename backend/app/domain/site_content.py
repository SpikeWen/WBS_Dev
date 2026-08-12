from dataclasses import dataclass

from app.domain.article import Article
from app.domain.case import CaseStudy
from app.domain.faq import FAQItem
from app.domain.page import ContentPage
from app.domain.product import Product
from app.domain.profile import CompanyProfile, SiteProfile
from app.domain.service_item import ServiceItem
from app.domain.site import Site


@dataclass(frozen=True)
class SiteContent:
    site: Site
    site_profile: SiteProfile
    company_profile: CompanyProfile
    pages: list[ContentPage]
    articles: list[Article]
    products: list[Product]
    faqs: list[FAQItem]
    cases: list[CaseStudy]
    services: list[ServiceItem]
