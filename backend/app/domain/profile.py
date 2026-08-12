from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class SiteProfile:
    site_id: str
    site_name: str = ""
    subtitle: str = ""
    logo: str = ""
    favicon: str = ""
    default_title: str = ""
    default_description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def update(
        self,
        site_name: str | None = None,
        subtitle: str | None = None,
        logo: str | None = None,
        favicon: str | None = None,
        default_title: str | None = None,
        default_description: str | None = None,
    ) -> None:
        if site_name is not None:
            self.site_name = site_name
        if subtitle is not None:
            self.subtitle = subtitle
        if logo is not None:
            self.logo = logo
        if favicon is not None:
            self.favicon = favicon
        if default_title is not None:
            self.default_title = default_title
        if default_description is not None:
            self.default_description = default_description
        self.updated_at = datetime.now(UTC)


@dataclass(slots=True)
class CompanyProfile:
    site_id: str
    company_name: str = ""
    legal_name: str = ""
    industry: str = ""
    description: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    service_area: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def update(
        self,
        company_name: str | None = None,
        legal_name: str | None = None,
        industry: str | None = None,
        description: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        service_area: str | None = None,
    ) -> None:
        if company_name is not None:
            self.company_name = company_name
        if legal_name is not None:
            self.legal_name = legal_name
        if industry is not None:
            self.industry = industry
        if description is not None:
            self.description = description
        if phone is not None:
            self.phone = phone
        if email is not None:
            self.email = email
        if address is not None:
            self.address = address
        if service_area is not None:
            self.service_area = service_area
        self.updated_at = datetime.now(UTC)

