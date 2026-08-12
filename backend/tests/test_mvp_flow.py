from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.api import routes
from app.api.routes import (
    preview_article,
    preview_case,
    preview_focused_item,
    preview_focused_section,
    preview_page,
    preview_product,
    preview_service,
    preview_site,
    publish_site,
)
from app.application.site_service import SiteApplicationService
from app.domain.article import ArticleStatus
from app.domain.case import CaseStatus
from app.domain.errors import DuplicateSlugError
from app.domain.faq import FAQStatus
from app.domain.page import PageStatus
from app.domain.product import ProductStatus
from app.domain.service_item import ServiceStatus
from app.infrastructure.sqlite_site_repository import SQLiteSiteRepository
from app.schemas.site import (
    ArticleCreateRequest,
    ArticleUpdateRequest,
    CaseCreateRequest,
    CaseUpdateRequest,
    CompanyProfileRequest,
    PageCreateRequest,
    PageUpdateRequest,
    FAQCreateRequest,
    FAQUpdateRequest,
    MediaAssetUpdateRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
    ServiceCreateRequest,
    ServiceUpdateRequest,
    SiteCreateRequest,
    SiteProfileRequest,
)


class MvpFlowTest(unittest.TestCase):
    def test_site_profiles_pages_and_preview_are_persisted(self) -> None:
        with TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "wbs.db"
            service = SiteApplicationService(SQLiteSiteRepository(db_path))

            site = service.create_site(
                SiteCreateRequest(
                    tenant_id="tenant_001",
                    name="示例官网",
                    template_id="template_basic",
                    domain="example.com",
                )
            )
            service.update_site_profile(
                site.id,
                SiteProfileRequest(
                    site_name="WBS 企业官网",
                    subtitle="官网后台继续长肉",
                    default_title="WBS 企业官网",
                    logo=f"/storage/sites/{site.id}/assets/logo.png",
                ),
            )
            service.update_company_profile(
                site.id,
                CompanyProfileRequest(
                    company_name="WBS Tech",
                    description="企业档案文本",
                ),
            )
            page = service.create_page(
                site.id,
                PageCreateRequest(
                    title="关于我们",
                    slug="about",
                    h1="关于 WBS Tech",
                    body="第一段正文",
                    sort_order=1,
                ),
            )

            self.assertIsNotNone(page)
            assert page is not None
            self.assertTrue(page.show_in_nav)
            service.update_page(
                page.id,
                PageUpdateRequest(
                    status=PageStatus.PUBLISHED,
                    body="已发布的关于我们正文",
                ),
            )
            article = service.create_article(
                site.id,
                ArticleCreateRequest(
                    title="第一篇资讯",
                    slug="first-news",
                    category="新闻",
                    summary="文章摘要",
                    body="文章正文",
                    cover_image=f"/storage/sites/{site.id}/assets/news.png",
                ),
            )

            self.assertIsNotNone(article)
            assert article is not None
            service.update_article(
                article.id,
                ArticleUpdateRequest(status=ArticleStatus.PUBLISHED),
            )
            product = service.create_product(
                site.id,
                ProductCreateRequest(
                    name="WBS CMS 套件",
                    slug="wbs-cms-suite",
                    category="软件产品",
                    model="MVP-1",
                    summary="官网后台管理系统",
                    description="产品介绍正文",
                    specifications="SQLite 起步\nFastAPI 后端",
                    price_note="按项目报价",
                ),
            )

            self.assertIsNotNone(product)
            assert product is not None
            service.update_product(
                product.id,
                ProductUpdateRequest(status=ProductStatus.PUBLISHED),
            )
            faq = service.create_faq(
                site.id,
                FAQCreateRequest(
                    question="交付周期是多久？",
                    answer="MVP 阶段按模块逐步验收。",
                    category="交付",
                    sort_order=1,
                ),
            )

            self.assertIsNotNone(faq)
            assert faq is not None
            service.update_faq(
                faq.id,
                FAQUpdateRequest(status=FAQStatus.PUBLISHED),
            )
            case = service.create_case(
                site.id,
                CaseCreateRequest(
                    title="制造业官网升级案例",
                    slug="manufacturing-website-case",
                    client_name="某制造企业",
                    industry="制造业",
                    summary="官网内容后台化改造",
                    challenge="旧站内容更新依赖开发。",
                    solution="用 WBS 管理站点资料和内容模块。",
                    result="资料保存后前台预览同步更新。",
                    project_date="2026-08",
                ),
            )

            self.assertIsNotNone(case)
            assert case is not None
            service.update_case(
                case.id,
                CaseUpdateRequest(status=CaseStatus.PUBLISHED),
            )
            service_item = service.create_service(
                site.id,
                ServiceCreateRequest(
                    name="官网后台实施服务",
                    slug="website-cms-service",
                    category="官网建设",
                    summary="从资料沉淀到预览发布的实施服务",
                    scope="站点资料\n内容模块\n预览发布",
                    process="建站点\n填资料\n发布预览",
                    deliverables="后台系统\n前台官网预览",
                    price_note="按范围报价",
                ),
            )

            self.assertIsNotNone(service_item)
            assert service_item is not None
            service.update_service(
                service_item.id,
                ServiceUpdateRequest(status=ServiceStatus.PUBLISHED),
            )
            asset = service.create_asset(
                site_id=site.id,
                filename="logo.png",
                url=f"/storage/sites/{site.id}/assets/logo.png",
                alt_text="企业 Logo",
                file_type="image/png",
                size=2048,
            )

            self.assertIsNotNone(asset)
            assert asset is not None
            service.update_asset(
                asset.id,
                MediaAssetUpdateRequest(alt_text="更新后的 Logo 说明"),
            )
            readiness = service.get_publish_readiness(site.id)
            self.assertIsNotNone(readiness)
            assert readiness is not None
            self.assertTrue(readiness.can_publish)
            self.assertFalse(any(issue.level.value == "error" for issue in readiness.issues))

            reopened = SQLiteSiteRepository(db_path)
            self.assertEqual(len(reopened.list_sites()), 1)
            self.assertEqual(reopened.get_site_profile(site.id).site_name, "WBS 企业官网")
            self.assertEqual(reopened.get_company_profile(site.id).company_name, "WBS Tech")
            self.assertEqual(len(reopened.list_pages(site.id)), 1)
            self.assertEqual(len(reopened.list_articles(site.id)), 1)
            self.assertEqual(len(reopened.list_products(site.id)), 1)
            self.assertEqual(len(reopened.list_faqs(site.id)), 1)
            self.assertEqual(len(reopened.list_cases(site.id)), 1)
            self.assertEqual(len(reopened.list_services(site.id)), 1)
            self.assertEqual(len(reopened.list_assets(site.id)), 1)
            self.assertEqual(reopened.list_assets(site.id)[0].alt_text, "更新后的 Logo 说明")

            html = preview_site(site.id, service).body.decode("utf-8")
            self.assertIn("WBS 企业官网", html)
            self.assertIn("/api/sites/", html)
            self.assertIn("/preview/pages/about", html)
            self.assertIn("/storage/sites/", html)
            self.assertIn("关于 WBS Tech", html)
            self.assertIn("已发布的关于我们正文", html)
            self.assertIn("第一篇资讯", html)
            self.assertIn("/preview/articles/first-news", html)
            self.assertIn("WBS CMS 套件", html)
            self.assertIn("/preview/products/wbs-cms-suite", html)
            self.assertIn("交付周期是多久？", html)
            self.assertIn("MVP 阶段按模块逐步验收。", html)
            self.assertIn("制造业官网升级案例", html)
            self.assertIn("/preview/cases/manufacturing-website-case", html)
            self.assertIn("官网后台实施服务", html)
            self.assertIn("/preview/services/website-cms-service", html)
            page_html = preview_page(site.id, "about", service).body.decode("utf-8")
            self.assertIn("navLink active", page_html)
            self.assertIn("已发布的关于我们正文", page_html)
            service.update_page(page.id, PageUpdateRequest(show_in_nav=False))
            html_without_nav_page = preview_site(site.id, service).body.decode("utf-8")
            self.assertNotIn("preview/pages/about", html_without_nav_page.split('<section class="heroBand">')[0])
            self.assertIn("已发布的关于我们正文", html_without_nav_page)
            service.update_page(page.id, PageUpdateRequest(show_in_nav=True))
            article_html = preview_article(site.id, "first-news", service).body.decode("utf-8")
            self.assertIn("文章正文", article_html)
            self.assertNotIn('class="navLink active" href="/api/sites/', article_html)
            product_html = preview_product(site.id, "wbs-cms-suite", service).body.decode("utf-8")
            self.assertIn("SQLite 起步", product_html)
            case_html = preview_case(site.id, "manufacturing-website-case", service).body.decode("utf-8")
            self.assertIn("旧站内容更新依赖开发。", case_html)
            service_html = preview_service(site.id, "website-cms-service", service).body.decode("utf-8")
            self.assertIn("站点资料", service_html)
            focused_identity_html = preview_focused_section(site.id, "identity", service).body.decode("utf-8")
            self.assertIn("WBS 企业官网", focused_identity_html)
            self.assertNotIn("资讯文章", focused_identity_html)
            focused_article_html = preview_focused_item(site.id, "articles", "first-news", service).body.decode("utf-8")
            self.assertIn("文章正文", focused_article_html)
            self.assertNotIn("产品资料", focused_article_html)

            routes.EXPORTS_DIR = Path(tmp) / "exports"
            publish = publish_site(site.id, service)
            self.assertEqual(publish.status.value, "success")
            self.assertTrue(Path(publish.output_path).exists())
            self.assertTrue((Path(publish.output_path).parent / "about" / "index.html").exists())
            self.assertTrue((Path(publish.output_path).parent / "articles" / "first-news" / "index.html").exists())
            self.assertTrue((Path(publish.output_path).parent / "products" / "wbs-cms-suite" / "index.html").exists())
            self.assertTrue(
                (Path(publish.output_path).parent / "cases" / "manufacturing-website-case" / "index.html").exists()
            )
            self.assertTrue((Path(publish.output_path).parent / "services" / "website-cms-service" / "index.html").exists())
            static_page_html = (Path(publish.output_path).parent / "about" / "index.html").read_text(encoding="utf-8")
            self.assertIn("../index.html", static_page_html)
            static_article_html = (
                Path(publish.output_path).parent / "articles" / "first-news" / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn("../../index.html", static_article_html)
            self.assertIn(site.id, publish.publish_url)
            self.assertEqual(len(reopened.list_publish_records(site.id)), 1)
            openapi_paths = {route.path for route in routes.router.routes}
            self.assertIn("/sites/{site_id}/assets", openapi_paths)
            self.assertIn("/assets/{asset_id}", openapi_paths)
            self.assertIn("/sites/{site_id}/publish-readiness", openapi_paths)

            self.assertTrue(service.delete_page(page.id))
            self.assertTrue(service.delete_article(article.id))
            self.assertTrue(service.delete_product(product.id))
            self.assertTrue(service.delete_faq(faq.id))
            self.assertTrue(service.delete_case(case.id))
            self.assertTrue(service.delete_service(service_item.id))
            self.assertTrue(service.delete_asset(asset.id))
            self.assertFalse(service.delete_page(page.id))
            self.assertEqual(len(reopened.list_pages(site.id)), 0)
            self.assertEqual(len(reopened.list_articles(site.id)), 0)
            self.assertEqual(len(reopened.list_products(site.id)), 0)
            self.assertEqual(len(reopened.list_faqs(site.id)), 0)
            self.assertEqual(len(reopened.list_cases(site.id)), 0)
            self.assertEqual(len(reopened.list_services(site.id)), 0)
            self.assertEqual(len(reopened.list_assets(site.id)), 0)

    def test_publish_readiness_reports_optional_content_gaps(self) -> None:
        with TemporaryDirectory() as tmp:
            service = SiteApplicationService(SQLiteSiteRepository(Path(tmp) / "wbs.db"))
            site = service.create_site(
                SiteCreateRequest(
                    tenant_id="tenant_001",
                    name="空壳官网",
                    template_id="template_basic",
                )
            )

            readiness = service.get_publish_readiness(site.id)

            self.assertIsNotNone(readiness)
            assert readiness is not None
            self.assertTrue(readiness.can_publish)
            self.assertGreater(readiness.issue_count, 0)
            self.assertIn("company_profile", {issue.module for issue in readiness.issues})
            self.assertIn("pages", {issue.module for issue in readiness.issues})

    def test_duplicate_page_slug_raises_domain_error(self) -> None:
        with TemporaryDirectory() as tmp:
            service = SiteApplicationService(SQLiteSiteRepository(Path(tmp) / "wbs.db"))
            site = service.create_site(
                SiteCreateRequest(
                    tenant_id="tenant_001",
                    name="示例官网",
                    template_id="template_basic",
                )
            )
            service.create_page(site.id, PageCreateRequest(title="关于我们", slug="about"))

            with self.assertRaises(DuplicateSlugError) as context:
                service.create_page(site.id, PageCreateRequest(title="另一个关于我们", slug="about"))

            self.assertIn("slug 已存在", str(context.exception))


if __name__ == "__main__":
    unittest.main()
