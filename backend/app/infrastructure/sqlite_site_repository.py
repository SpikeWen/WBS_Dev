from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import RLock

from app.domain.article import Article, ArticleStatus
from app.domain.case import CaseStatus, CaseStudy
from app.domain.errors import DuplicateSlugError
from app.domain.faq import FAQItem, FAQStatus
from app.domain.media import MediaAsset
from app.domain.page import ContentPage, PageStatus
from app.domain.product import Product, ProductStatus
from app.domain.profile import CompanyProfile, SiteProfile
from app.domain.publish import PublishRecord, PublishStatus
from app.domain.repositories import SiteRepository
from app.domain.service_item import ServiceItem, ServiceStatus
from app.domain.site import Site, SiteStatus


class SQLiteSiteRepository(SiteRepository):
    def __init__(self, db_path: Path | None = None) -> None:
        base_dir = Path(__file__).resolve().parents[2] / "data"
        base_dir.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path or (base_dir / "wbs.db")
        self._lock = RLock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._lock, self._connect() as conn:
            conn.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS sites (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    template_id TEXT NOT NULL,
                    domain TEXT,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS site_profiles (
                    site_id TEXT PRIMARY KEY,
                    site_name TEXT NOT NULL,
                    subtitle TEXT NOT NULL,
                    logo TEXT NOT NULL,
                    favicon TEXT NOT NULL,
                    default_title TEXT NOT NULL,
                    default_description TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS company_profiles (
                    site_id TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    legal_name TEXT NOT NULL,
                    industry TEXT NOT NULL,
                    description TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    service_area TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS pages (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    h1 TEXT NOT NULL,
                    body TEXT NOT NULL,
                    meta_title TEXT NOT NULL,
                    meta_description TEXT NOT NULL,
                    sort_order INTEGER NOT NULL,
                    show_in_nav INTEGER NOT NULL DEFAULT 1,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(site_id, slug)
                );
                CREATE TABLE IF NOT EXISTS articles (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    category TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    body TEXT NOT NULL,
                    cover_image TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(site_id, slug)
                );
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    category TEXT NOT NULL,
                    model TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    description TEXT NOT NULL,
                    specifications TEXT NOT NULL,
                    cover_image TEXT NOT NULL,
                    price_note TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(site_id, slug)
                );
                CREATE TABLE IF NOT EXISTS faqs (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    category TEXT NOT NULL,
                    sort_order INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS cases (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    client_name TEXT NOT NULL,
                    industry TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    challenge TEXT NOT NULL,
                    solution TEXT NOT NULL,
                    result TEXT NOT NULL,
                    cover_image TEXT NOT NULL,
                    project_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(site_id, slug)
                );
                CREATE TABLE IF NOT EXISTS services (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    category TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    process TEXT NOT NULL,
                    deliverables TEXT NOT NULL,
                    price_note TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(site_id, slug)
                );
                CREATE TABLE IF NOT EXISTS publish_records (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    version TEXT NOT NULL,
                    status TEXT NOT NULL,
                    preview_url TEXT NOT NULL,
                    publish_url TEXT NOT NULL,
                    output_path TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS media_assets (
                    id TEXT PRIMARY KEY,
                    site_id TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    url TEXT NOT NULL,
                    alt_text TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )
            self._ensure_column(conn, "pages", "show_in_nav", "INTEGER NOT NULL DEFAULT 1")

    def _ensure_column(self, conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def _handle_integrity_error(self, error: sqlite3.IntegrityError, slug: str | None = None) -> None:
        if "UNIQUE constraint failed" in str(error) and ".slug" in str(error):
            raise DuplicateSlugError(slug) from error
        raise error

    def add(self, site: Site) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sites (id, tenant_id, name, template_id, domain, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._site_params(site),
            )
            self._ensure_default_profiles(conn, site.id)

    def get(self, site_id: str) -> Site | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM sites WHERE id = ?", (site_id,)).fetchone()
            if row is None:
                return None
            return self._site_from_row(row)

    def list_sites(self) -> list[Site]:
        with self._lock, self._connect() as conn:
            rows = conn.execute("SELECT * FROM sites ORDER BY created_at DESC").fetchall()
            return [self._site_from_row(row) for row in rows]

    def save(self, site: Site) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE sites
                SET tenant_id = ?, name = ?, template_id = ?, domain = ?, status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    site.tenant_id,
                    site.name,
                    site.template_id,
                    site.domain,
                    site.status.value,
                    site.updated_at.isoformat(),
                    site.id,
                ),
            )

    def get_site_profile(self, site_id: str) -> SiteProfile:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM site_profiles WHERE site_id = ?", (site_id,)).fetchone()
            if row is None:
                profile = SiteProfile(site_id=site_id)
                self.save_site_profile(profile)
                return profile
            return self._site_profile_from_row(row)

    def save_site_profile(self, profile: SiteProfile) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO site_profiles (
                    site_id, site_name, subtitle, logo, favicon, default_title, default_description, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(site_id) DO UPDATE SET
                    site_name = excluded.site_name,
                    subtitle = excluded.subtitle,
                    logo = excluded.logo,
                    favicon = excluded.favicon,
                    default_title = excluded.default_title,
                    default_description = excluded.default_description,
                    updated_at = excluded.updated_at
                """,
                (
                    profile.site_id,
                    profile.site_name,
                    profile.subtitle,
                    profile.logo,
                    profile.favicon,
                    profile.default_title,
                    profile.default_description,
                    profile.created_at.isoformat(),
                    profile.updated_at.isoformat(),
                ),
            )

    def get_company_profile(self, site_id: str) -> CompanyProfile:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM company_profiles WHERE site_id = ?", (site_id,)).fetchone()
            if row is None:
                profile = CompanyProfile(site_id=site_id)
                self.save_company_profile(profile)
                return profile
            return self._company_profile_from_row(row)

    def save_company_profile(self, profile: CompanyProfile) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO company_profiles (
                    site_id, company_name, legal_name, industry, description, phone, email, address, service_area, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(site_id) DO UPDATE SET
                    company_name = excluded.company_name,
                    legal_name = excluded.legal_name,
                    industry = excluded.industry,
                    description = excluded.description,
                    phone = excluded.phone,
                    email = excluded.email,
                    address = excluded.address,
                    service_area = excluded.service_area,
                    updated_at = excluded.updated_at
                """,
                (
                    profile.site_id,
                    profile.company_name,
                    profile.legal_name,
                    profile.industry,
                    profile.description,
                    profile.phone,
                    profile.email,
                    profile.address,
                    profile.service_area,
                    profile.created_at.isoformat(),
                    profile.updated_at.isoformat(),
                ),
            )

    def list_pages(self, site_id: str) -> list[ContentPage]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM pages WHERE site_id = ? ORDER BY sort_order ASC, created_at ASC",
                (site_id,),
            ).fetchall()
            return [self._page_from_row(row) for row in rows]

    def add_page(self, page: ContentPage) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO pages (
                        id, site_id, title, slug, h1, body, meta_title, meta_description, sort_order, show_in_nav, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._page_params(page),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, page.slug)

    def get_page(self, page_id: str) -> ContentPage | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM pages WHERE id = ?", (page_id,)).fetchone()
            if row is None:
                return None
            return self._page_from_row(row)

    def get_page_by_slug(self, site_id: str, slug: str) -> ContentPage | None:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM pages WHERE site_id = ? AND slug = ?",
                (site_id, slug),
            ).fetchone()
            if row is None:
                return None
            return self._page_from_row(row)

    def save_page(self, page: ContentPage) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    UPDATE pages
                    SET title = ?,
                        slug = ?,
                        h1 = ?,
                        body = ?,
                        meta_title = ?,
                        meta_description = ?,
                        sort_order = ?,
                        show_in_nav = ?,
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        page.title,
                        page.slug,
                        page.h1,
                        page.body,
                        page.meta_title,
                        page.meta_description,
                        page.sort_order,
                        1 if page.show_in_nav else 0,
                        page.status.value,
                        page.updated_at.isoformat(),
                        page.id,
                    ),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, page.slug)

    def delete_page(self, page_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM pages WHERE id = ?", (page_id,))

    def list_articles(self, site_id: str) -> list[Article]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE site_id = ? ORDER BY created_at DESC",
                (site_id,),
            ).fetchall()
            return [self._article_from_row(row) for row in rows]

    def add_article(self, article: Article) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO articles (
                        id, site_id, title, slug, category, summary, body, cover_image, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._article_params(article),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, article.slug)

    def get_article(self, article_id: str) -> Article | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
            if row is None:
                return None
            return self._article_from_row(row)

    def save_article(self, article: Article) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    UPDATE articles
                    SET title = ?,
                        slug = ?,
                        category = ?,
                        summary = ?,
                        body = ?,
                        cover_image = ?,
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        article.title,
                        article.slug,
                        article.category,
                        article.summary,
                        article.body,
                        article.cover_image,
                        article.status.value,
                        article.updated_at.isoformat(),
                        article.id,
                    ),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, article.slug)

    def delete_article(self, article_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))

    def list_products(self, site_id: str) -> list[Product]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM products WHERE site_id = ? ORDER BY created_at DESC",
                (site_id,),
            ).fetchall()
            return [self._product_from_row(row) for row in rows]

    def add_product(self, product: Product) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO products (
                        id, site_id, name, slug, category, model, summary, description, specifications,
                        cover_image, price_note, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._product_params(product),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, product.slug)

    def get_product(self, product_id: str) -> Product | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if row is None:
                return None
            return self._product_from_row(row)

    def save_product(self, product: Product) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    UPDATE products
                    SET name = ?,
                        slug = ?,
                        category = ?,
                        model = ?,
                        summary = ?,
                        description = ?,
                        specifications = ?,
                        cover_image = ?,
                        price_note = ?,
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        product.name,
                        product.slug,
                        product.category,
                        product.model,
                        product.summary,
                        product.description,
                        product.specifications,
                        product.cover_image,
                        product.price_note,
                        product.status.value,
                        product.updated_at.isoformat(),
                        product.id,
                    ),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, product.slug)

    def delete_product(self, product_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))

    def list_faqs(self, site_id: str) -> list[FAQItem]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM faqs WHERE site_id = ? ORDER BY sort_order ASC, created_at ASC",
                (site_id,),
            ).fetchall()
            return [self._faq_from_row(row) for row in rows]

    def add_faq(self, faq: FAQItem) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO faqs (
                    id, site_id, question, answer, category, sort_order, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._faq_params(faq),
            )

    def get_faq(self, faq_id: str) -> FAQItem | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM faqs WHERE id = ?", (faq_id,)).fetchone()
            if row is None:
                return None
            return self._faq_from_row(row)

    def save_faq(self, faq: FAQItem) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE faqs
                SET question = ?,
                    answer = ?,
                    category = ?,
                    sort_order = ?,
                    status = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    faq.question,
                    faq.answer,
                    faq.category,
                    faq.sort_order,
                    faq.status.value,
                    faq.updated_at.isoformat(),
                    faq.id,
                ),
            )

    def delete_faq(self, faq_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))

    def list_cases(self, site_id: str) -> list[CaseStudy]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM cases WHERE site_id = ? ORDER BY created_at DESC",
                (site_id,),
            ).fetchall()
            return [self._case_from_row(row) for row in rows]

    def add_case(self, case: CaseStudy) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO cases (
                        id, site_id, title, slug, client_name, industry, summary, challenge, solution,
                        result, cover_image, project_date, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._case_params(case),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, case.slug)

    def get_case(self, case_id: str) -> CaseStudy | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
            if row is None:
                return None
            return self._case_from_row(row)

    def save_case(self, case: CaseStudy) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    UPDATE cases
                    SET title = ?,
                        slug = ?,
                        client_name = ?,
                        industry = ?,
                        summary = ?,
                        challenge = ?,
                        solution = ?,
                        result = ?,
                        cover_image = ?,
                        project_date = ?,
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        case.title,
                        case.slug,
                        case.client_name,
                        case.industry,
                        case.summary,
                        case.challenge,
                        case.solution,
                        case.result,
                        case.cover_image,
                        case.project_date,
                        case.status.value,
                        case.updated_at.isoformat(),
                        case.id,
                    ),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, case.slug)

    def delete_case(self, case_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM cases WHERE id = ?", (case_id,))

    def list_services(self, site_id: str) -> list[ServiceItem]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM services WHERE site_id = ? ORDER BY created_at DESC",
                (site_id,),
            ).fetchall()
            return [self._service_from_row(row) for row in rows]

    def add_service(self, service: ServiceItem) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO services (
                        id, site_id, name, slug, category, summary, scope, process, deliverables,
                        price_note, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._service_params(service),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, service.slug)

    def get_service(self, service_id: str) -> ServiceItem | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM services WHERE id = ?", (service_id,)).fetchone()
            if row is None:
                return None
            return self._service_from_row(row)

    def save_service(self, service: ServiceItem) -> None:
        with self._lock, self._connect() as conn:
            try:
                conn.execute(
                    """
                    UPDATE services
                    SET name = ?,
                        slug = ?,
                        category = ?,
                        summary = ?,
                        scope = ?,
                        process = ?,
                        deliverables = ?,
                        price_note = ?,
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        service.name,
                        service.slug,
                        service.category,
                        service.summary,
                        service.scope,
                        service.process,
                        service.deliverables,
                        service.price_note,
                        service.status.value,
                        service.updated_at.isoformat(),
                        service.id,
                    ),
                )
            except sqlite3.IntegrityError as error:
                self._handle_integrity_error(error, service.slug)

    def delete_service(self, service_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM services WHERE id = ?", (service_id,))

    def add_publish_record(self, record: PublishRecord) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO publish_records (
                    id, site_id, version, status, preview_url, publish_url, output_path, message, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.site_id,
                    record.version,
                    record.status.value,
                    record.preview_url,
                    record.publish_url,
                    record.output_path,
                    record.message,
                    record.created_at.isoformat(),
                ),
            )

    def list_publish_records(self, site_id: str) -> list[PublishRecord]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM publish_records WHERE site_id = ? ORDER BY created_at DESC",
                (site_id,),
            ).fetchall()
            return [self._publish_record_from_row(row) for row in rows]

    def list_assets(self, site_id: str) -> list[MediaAsset]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM media_assets WHERE site_id = ? ORDER BY created_at DESC",
                (site_id,),
            ).fetchall()
            return [self._asset_from_row(row) for row in rows]

    def add_asset(self, asset: MediaAsset) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO media_assets (
                    id, site_id, filename, url, alt_text, file_type, size, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    asset.id,
                    asset.site_id,
                    asset.filename,
                    asset.url,
                    asset.alt_text,
                    asset.file_type,
                    asset.size,
                    asset.created_at.isoformat(),
                    asset.updated_at.isoformat(),
                ),
            )

    def get_asset(self, asset_id: str) -> MediaAsset | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM media_assets WHERE id = ?", (asset_id,)).fetchone()
            if row is None:
                return None
            return self._asset_from_row(row)

    def save_asset(self, asset: MediaAsset) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE media_assets
                SET alt_text = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    asset.alt_text,
                    asset.updated_at.isoformat(),
                    asset.id,
                ),
            )

    def delete_asset(self, asset_id: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM media_assets WHERE id = ?", (asset_id,))

    def _ensure_default_profiles(self, conn: sqlite3.Connection, site_id: str) -> None:
        conn.execute(
            """
            INSERT OR IGNORE INTO site_profiles (
                site_id, site_name, subtitle, logo, favicon, default_title, default_description, created_at, updated_at
            ) VALUES (?, '', '', '', '', '', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (site_id,),
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO company_profiles (
                site_id, company_name, legal_name, industry, description, phone, email, address, service_area, created_at, updated_at
            ) VALUES (?, '', '', '', '', '', '', '', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (site_id,),
        )

    def _site_params(self, site: Site) -> tuple[object, ...]:
        return (
            site.id,
            site.tenant_id,
            site.name,
            site.template_id,
            site.domain,
            site.status.value,
            site.created_at.isoformat(),
            site.updated_at.isoformat(),
        )

    def _site_from_row(self, row: sqlite3.Row) -> Site:
        return Site(
            id=row["id"],
            tenant_id=row["tenant_id"],
            name=row["name"],
            template_id=row["template_id"],
            domain=row["domain"],
            status=SiteStatus(row["status"]),
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _site_profile_from_row(self, row: sqlite3.Row) -> SiteProfile:
        return SiteProfile(
            site_id=row["site_id"],
            site_name=row["site_name"],
            subtitle=row["subtitle"],
            logo=row["logo"],
            favicon=row["favicon"],
            default_title=row["default_title"],
            default_description=row["default_description"],
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _company_profile_from_row(self, row: sqlite3.Row) -> CompanyProfile:
        return CompanyProfile(
            site_id=row["site_id"],
            company_name=row["company_name"],
            legal_name=row["legal_name"],
            industry=row["industry"],
            description=row["description"],
            phone=row["phone"],
            email=row["email"],
            address=row["address"],
            service_area=row["service_area"],
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _page_params(self, page: ContentPage) -> tuple[object, ...]:
        return (
            page.id,
            page.site_id,
            page.title,
            page.slug,
            page.h1,
            page.body,
            page.meta_title,
            page.meta_description,
            page.sort_order,
            1 if page.show_in_nav else 0,
            page.status.value,
            page.created_at.isoformat(),
            page.updated_at.isoformat(),
        )

    def _page_from_row(self, row: sqlite3.Row) -> ContentPage:
        return ContentPage(
            id=row["id"],
            site_id=row["site_id"],
            title=row["title"],
            slug=row["slug"],
            h1=row["h1"],
            body=row["body"],
            meta_title=row["meta_title"],
            meta_description=row["meta_description"],
            sort_order=row["sort_order"],
            show_in_nav=bool(row["show_in_nav"]),
            status=PageStatus(row["status"]),
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _article_params(self, article: Article) -> tuple[object, ...]:
        return (
            article.id,
            article.site_id,
            article.title,
            article.slug,
            article.category,
            article.summary,
            article.body,
            article.cover_image,
            article.status.value,
            article.created_at.isoformat(),
            article.updated_at.isoformat(),
        )

    def _article_from_row(self, row: sqlite3.Row) -> Article:
        return Article(
            id=row["id"],
            site_id=row["site_id"],
            title=row["title"],
            slug=row["slug"],
            category=row["category"],
            summary=row["summary"],
            body=row["body"],
            cover_image=row["cover_image"],
            status=ArticleStatus(row["status"]),
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _product_params(self, product: Product) -> tuple[object, ...]:
        return (
            product.id,
            product.site_id,
            product.name,
            product.slug,
            product.category,
            product.model,
            product.summary,
            product.description,
            product.specifications,
            product.cover_image,
            product.price_note,
            product.status.value,
            product.created_at.isoformat(),
            product.updated_at.isoformat(),
        )

    def _product_from_row(self, row: sqlite3.Row) -> Product:
        return Product(
            id=row["id"],
            site_id=row["site_id"],
            name=row["name"],
            slug=row["slug"],
            category=row["category"],
            model=row["model"],
            summary=row["summary"],
            description=row["description"],
            specifications=row["specifications"],
            cover_image=row["cover_image"],
            price_note=row["price_note"],
            status=ProductStatus(row["status"]),
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _faq_params(self, faq: FAQItem) -> tuple[object, ...]:
        return (
            faq.id,
            faq.site_id,
            faq.question,
            faq.answer,
            faq.category,
            faq.sort_order,
            faq.status.value,
            faq.created_at.isoformat(),
            faq.updated_at.isoformat(),
        )

    def _faq_from_row(self, row: sqlite3.Row) -> FAQItem:
        return FAQItem(
            id=row["id"],
            site_id=row["site_id"],
            question=row["question"],
            answer=row["answer"],
            category=row["category"],
            sort_order=row["sort_order"],
            status=FAQStatus(row["status"]),
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _case_params(self, case: CaseStudy) -> tuple[object, ...]:
        return (
            case.id,
            case.site_id,
            case.title,
            case.slug,
            case.client_name,
            case.industry,
            case.summary,
            case.challenge,
            case.solution,
            case.result,
            case.cover_image,
            case.project_date,
            case.status.value,
            case.created_at.isoformat(),
            case.updated_at.isoformat(),
        )

    def _case_from_row(self, row: sqlite3.Row) -> CaseStudy:
        return CaseStudy(
            id=row["id"],
            site_id=row["site_id"],
            title=row["title"],
            slug=row["slug"],
            client_name=row["client_name"],
            industry=row["industry"],
            summary=row["summary"],
            challenge=row["challenge"],
            solution=row["solution"],
            result=row["result"],
            cover_image=row["cover_image"],
            project_date=row["project_date"],
            status=CaseStatus(row["status"]),
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _service_params(self, service: ServiceItem) -> tuple[object, ...]:
        return (
            service.id,
            service.site_id,
            service.name,
            service.slug,
            service.category,
            service.summary,
            service.scope,
            service.process,
            service.deliverables,
            service.price_note,
            service.status.value,
            service.created_at.isoformat(),
            service.updated_at.isoformat(),
        )

    def _service_from_row(self, row: sqlite3.Row) -> ServiceItem:
        return ServiceItem(
            id=row["id"],
            site_id=row["site_id"],
            name=row["name"],
            slug=row["slug"],
            category=row["category"],
            summary=row["summary"],
            scope=row["scope"],
            process=row["process"],
            deliverables=row["deliverables"],
            price_note=row["price_note"],
            status=ServiceStatus(row["status"]),
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _publish_record_from_row(self, row: sqlite3.Row) -> PublishRecord:
        return PublishRecord(
            id=row["id"],
            site_id=row["site_id"],
            version=row["version"],
            status=PublishStatus(row["status"]),
            preview_url=row["preview_url"],
            publish_url=row["publish_url"],
            output_path=row["output_path"],
            message=row["message"],
            created_at=self._parse_datetime(row["created_at"]),
        )

    def _asset_from_row(self, row: sqlite3.Row) -> MediaAsset:
        return MediaAsset(
            id=row["id"],
            site_id=row["site_id"],
            filename=row["filename"],
            url=row["url"],
            alt_text=row["alt_text"],
            file_type=row["file_type"],
            size=row["size"],
            created_at=self._parse_datetime(row["created_at"]),
            updated_at=self._parse_datetime(row["updated_at"]),
        )

    def _parse_datetime(self, value: str):
        from datetime import datetime

        normalized = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            return datetime.now()
