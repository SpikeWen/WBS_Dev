from html import escape

from app.domain.site_content import SiteContent
from app.infrastructure.site_preview_theme import render_preview_document


def render_site_preview(
    content: SiteContent,
    active_slug: str | None = None,
    active_content: tuple[str, str] | None = None,
    static_links: bool = False,
) -> str:
    visible_pages = _visible(content.pages)
    visible_articles = _visible(content.articles)
    visible_products = _visible(content.products)
    visible_faqs = _visible(content.faqs)
    visible_cases = _visible(content.cases)
    visible_services = _visible(content.services)
    site = content.site
    site_profile = content.site_profile
    company_profile = content.company_profile
    title = _html(site_profile.default_title or site.name)
    display_name = _html(site_profile.site_name or site.name)
    subtitle = _html(site_profile.subtitle)
    logo = site_profile.logo
    default_description = _html(site_profile.default_description)
    company_description = _html(company_profile.description)
    company_name = _html(company_profile.company_name)
    phone = _html(company_profile.phone)
    email = _html(company_profile.email)
    address = _html(company_profile.address)
    active_page = None
    detail_html = ""
    if active_slug is not None:
        active_page = next((page for page in visible_pages if page.slug == active_slug), None)
        if active_page is None:
            return ""
    if active_content is not None:
        detail_html = _detail_html(active_content, visible_articles, visible_products, visible_cases, visible_services)
        if not detail_html:
            return ""
    static_prefix = "../../" if static_links and active_content is not None else "../" if static_links and active_slug is not None else "./"
    home_href = f"{static_prefix}index.html" if static_links else f"/api/sites/{site.id}/preview"
    home_active = active_slug is None and active_content is None
    nav_pages = [page for page in visible_pages if page.show_in_nav]
    page_links = _render_page_links(site.id, nav_pages, active_slug, static_links, static_prefix)
    module_links = _render_module_links(visible_services, visible_products, visible_cases, visible_articles, visible_faqs)
    active_page_html = _render_active_page(active_page)
    page_cards = _render_page_cards(site.id, visible_pages, static_links, static_prefix)
    article_cards = _render_article_cards(site.id, visible_articles, static_links, static_prefix)
    product_cards = _render_product_cards(site.id, visible_products, static_links, static_prefix)
    faq_cards = _render_faq_cards(visible_faqs)
    case_cards = _render_case_cards(site.id, visible_cases, static_links, static_prefix)
    service_cards = _render_service_cards(site.id, visible_services, static_links, static_prefix)
    body_html = f"""<header class="siteHeader">
    <div class="navShell">
      <a class="brand" href="{home_href}">
        {_image(logo, display_name, 'logo')}
        <span>{display_name}</span>
      </a>
      <div class="navLinks">
        <a class="navLink homeLink{' active' if home_active else ''}" href="{home_href}">首页</a>
        {page_links}
        {module_links}
        <a class="navLink" href="#contact">联系</a>
      </div>
    </div>
  </header>
  <main>
    <section class="heroBand">
      <div class="heroShell heroSingle">
        <div class="heroCopy">
          <div class="label">企业官网</div>
          <h1>{display_name}</h1>
          <p class="lead">{subtitle or default_description}</p>
          <div class="heroActions">
            <a class="primaryCta" href="#services">查看服务</a>
            <a class="ghostCta" href="#contact">联系我们</a>
          </div>
        </div>
      </div>
    </section>
    <div class="wrap">
    <section class="aboutBand">
      <div>
        <div class="label">企业简介</div>
        <h2>{company_name or display_name}</h2>
      </div>
      <div class="aboutText">{_paragraphs(company_profile.description or site_profile.default_description)}</div>
    </section>
    {active_page_html}
    {detail_html}
    {_section_block('pages', '关于与栏目', '固定页面会出现在这里，适合放关于我们、资质、流程等长期内容。', page_cards, '<article class="panel"><div class="label">页面</div><h2>还没有固定页面</h2><div class="value">在后台新增页面后，这里会显示正文内容。</div></article>')}
    {_section_block('services', '服务项目', '把客户最关心的服务范围、流程和交付物集中展示。', service_cards, '<article class="panel"><div class="label">服务</div><h2>还没有服务项目</h2><div class="value">在后台新增服务后，这里会显示交付能力。</div></article>')}
    {_section_block('products', '产品资料', '产品模块用于展示产品名称、型号、卖点和基础参数。', product_cards, '<article class="panel"><div class="label">产品</div><h2>还没有产品</h2><div class="value">在后台新增产品后，这里会显示产品资料。</div></article>')}
    {_section_block('cases', '项目案例', '案例模块帮助访客快速判断企业经验和可信度。', case_cards, '<article class="panel"><div class="label">案例</div><h2>还没有案例</h2><div class="value">在后台新增案例后，这里会显示项目证明。</div></article>')}
    {_section_block('articles', '资讯文章', '文章模块承载新闻、知识内容和 SEO 长尾信息。', article_cards, '<article class="panel"><div class="label">文章</div><h2>还没有文章</h2><div class="value">在后台新增文章后，这里会显示资讯内容。</div></article>')}
    {_section_block('faq', '常见问题', 'FAQ 用来提前回答客户反复询问的问题。', faq_cards, '<article class="panel"><div class="label">FAQ</div><h2>还没有问答</h2><div class="value">在后台新增 FAQ 后，这里会显示常见问题。</div></article>')}
    </div>
  </main>
  <footer class="siteFooter" id="contact">
    <div class="footerShell">
      <div>
        <div class="label">联系我们</div>
        <h2>{company_name or display_name}</h2>
      </div>
      <div class="footerContact">
        <span>{phone}</span>
        <span>{email}</span>
        <span>{address}</span>
      </div>
    </div>
  </footer>"""
    return render_preview_document(body_html, title)


def render_focused_preview(
    content: SiteContent,
    section: str,
    slug: str | None = None,
) -> str:
    visible_pages = _visible(content.pages)
    visible_articles = _visible(content.articles)
    visible_products = _visible(content.products)
    visible_cases = _visible(content.cases)
    visible_services = _visible(content.services)
    site = content.site
    site_profile = content.site_profile
    company_profile = content.company_profile
    title = _html(site_profile.default_title or site.name)
    display_name = _html(site_profile.site_name or site.name)
    subtitle = _html(site_profile.subtitle)

    if section == "identity":
        body_html = f"""<div class="wrap">
    <nav class="siteNav">
      <a class="brand" href="/api/sites/{site.id}/preview">
        {_image(site_profile.logo, display_name, 'logo')}
        <span>{display_name}</span>
      </a>
    </nav>
    <section class="hero">
      <div class="muted">官网顶部</div>
      <h1>{display_name}</h1>
      <p class="muted">{subtitle}</p>
      <p class="muted">{_html(site_profile.default_description)}</p>
    </section>
  </div>"""
        return render_preview_document(body_html, title)

    if section == "company":
        body_html = f"""<div class="wrap">
    <h2 class="sectionTitle">企业档案</h2>
    <div class="grid">
      <section class="panel">
        <div class="label">企业介绍</div>
        <h2>{_html(company_profile.company_name)}</h2>
        <div class="value">{_paragraphs(company_profile.description)}</div>
      </section>
      <section class="panel">
        <div class="label">联系信息</div>
        <div class="value">{_html(company_profile.phone)}<br>{_html(company_profile.email)}<br>{_html(company_profile.address)}</div>
      </section>
      <section class="panel">
        <div class="label">行业</div>
        <div class="value">{_html(company_profile.industry)}</div>
      </section>
      <section class="panel">
        <div class="label">服务区域</div>
        <div class="value">{_html(company_profile.service_area)}</div>
      </section>
    </div>
  </div>"""
        return render_preview_document(body_html, title)

    if section == "pages" and slug is not None:
        page = next((item for item in visible_pages if item.slug == slug), None)
        return render_preview_document(f"""<div class="wrap">{_render_active_page(page)}</div>""", title) if page else ""

    if section in {"articles", "products", "cases", "services"} and slug is not None:
        detail_html = _detail_html((section, slug), visible_articles, visible_products, visible_cases, visible_services)
        return render_preview_document(f"""<div class="wrap">{detail_html}</div>""", title) if detail_html else ""

    return ""



def _html(value: str | None) -> str:
    return escape(value or "", quote=True)


def _paragraphs(value: str | None) -> str:
    escaped = _html(value)
    return escaped.replace("\n", "<br>")


def _visible(items):
    return [item for item in items if item.status != "hidden"]


def _image(url: str | None, alt: str | None, class_name: str = "cover") -> str:
    if not url:
        return ""
    return f"""<img class="{_html(class_name)}" src="{_html(url)}" alt="{_html(alt)}">"""


def _page_href(site_id: str, slug: str, static_links: bool, static_prefix: str = "./") -> str:
    if not static_links:
        return f"/api/sites/{site_id}/preview/pages/{_html(slug)}"
    return f"{static_prefix}{_html(slug)}/index.html"


def _detail_href(site_id: str, section: str, slug: str, static_links: bool, static_prefix: str = "./") -> str:
    if not static_links:
        return f"/api/sites/{site_id}/preview/{section}/{_html(slug)}"
    return f"{static_prefix}{section}/{_html(slug)}/index.html"


def _render_page_links(site_id: str, pages, active_slug: str | None, static_links: bool, static_prefix: str) -> str:
    return "\n".join(
        f"""<a class="navLink{' active' if page.slug == active_slug else ''}" href="{_page_href(site_id, page.slug, static_links, static_prefix)}">{_html(page.title)}</a>"""
        for page in pages
    )


def _render_module_links(services, products, cases, articles, faqs) -> str:
    links = [
        ("services", "服务", services),
        ("products", "产品", products),
        ("cases", "案例", cases),
        ("articles", "资讯", articles),
        ("faq", "FAQ", faqs),
    ]
    return "\n".join(
        f"""<a class="navLink" href="#{anchor}">{label}</a>"""
        for anchor, label, items in links
        if items
    )


def _section_block(anchor: str, title: str, intro: str, cards: str, empty_html: str) -> str:
    return f"""
    <section class="contentSection" id="{_html(anchor)}">
      <div class="sectionHeader">
        <div>
          <div class="label">内容模块</div>
          <h2 class="sectionTitle">{_html(title)}</h2>
          <p>{_html(intro)}</p>
        </div>
      </div>
      <div class="pageList">
        {cards or empty_html}
      </div>
    </section>"""


def _render_active_page(active_page) -> str:
    if active_page is None:
        return ""
    return f"""
    <section class="pageList">
      <article class="panel feature">
        <div class="label">{_html(active_page.slug)}</div>
        <h2>{_html(active_page.h1 or active_page.title)}</h2>
        <div class="value">{_paragraphs(active_page.body)}</div>
      </article>
    </section>"""


def _render_page_cards(site_id: str, pages, static_links: bool, static_prefix: str) -> str:
    return "\n".join(
        f"""
      <article class="panel">
        <div class="label">{_html(page.slug)}</div>
        <h2><a href="{_page_href(site_id, page.slug, static_links, static_prefix)}">{_html(page.h1 or page.title)}</a></h2>
        <div class="value">{_paragraphs(page.body)}</div>
      </article>"""
        for page in pages
    )


def _render_article_cards(site_id: str, articles, static_links: bool, static_prefix: str) -> str:
    return "\n".join(
        f"""
      <article class="panel">
        {_image(article.cover_image, article.title)}
        <div class="label">{_html(article.category or 'article')} / {_html(article.slug)}</div>
        <h2><a href="{_detail_href(site_id, 'articles', article.slug, static_links, static_prefix)}">{_html(article.title)}</a></h2>
        <div class="value">{_html(article.summary)}</div>
      </article>"""
        for article in articles
    )


def _render_product_cards(site_id: str, products, static_links: bool, static_prefix: str) -> str:
    return "\n".join(
        f"""
      <article class="panel">
        {_image(product.cover_image, product.name)}
        <div class="label">{_html(product.category or 'product')} / {_html(product.slug)}</div>
        <h2><a href="{_detail_href(site_id, 'products', product.slug, static_links, static_prefix)}">{_html(product.name)}</a></h2>
        <div class="value"><strong>型号:</strong> {_html(product.model)}</div>
        <div class="value">{_html(product.summary)}</div>
        <div class="value"><strong>价格说明:</strong> {_html(product.price_note)}</div>
      </article>"""
        for product in products
    )


def _render_faq_cards(faqs) -> str:
    return "\n".join(
        f"""
      <article class="panel">
        <div class="label">{_html(faq.category or 'faq')}</div>
        <h2>{_html(faq.question)}</h2>
        <div class="value">{_paragraphs(faq.answer)}</div>
      </article>"""
        for faq in faqs
    )


def _render_case_cards(site_id: str, cases, static_links: bool, static_prefix: str) -> str:
    return "\n".join(
        f"""
      <article class="panel">
        {_image(case.cover_image, case.title)}
        <div class="label">{_html(case.industry or 'case')} / {_html(case.slug)}</div>
        <h2><a href="{_detail_href(site_id, 'cases', case.slug, static_links, static_prefix)}">{_html(case.title)}</a></h2>
        <div class="value"><strong>客户:</strong> {_html(case.client_name)}</div>
        <div class="value"><strong>时间:</strong> {_html(case.project_date)}</div>
        <div class="value">{_html(case.summary)}</div>
      </article>"""
        for case in cases
    )


def _render_service_cards(site_id: str, services, static_links: bool, static_prefix: str) -> str:
    return "\n".join(
        f"""
      <article class="panel">
        <div class="label">{_html(item.category or 'service')} / {_html(item.slug)}</div>
        <h2><a href="{_detail_href(site_id, 'services', item.slug, static_links, static_prefix)}">{_html(item.name)}</a></h2>
        <div class="value">{_html(item.summary)}</div>
        <div class="value"><strong>价格说明:</strong> {_html(item.price_note)}</div>
      </article>"""
        for item in services
    )


def _detail_html(active_content, articles, products, cases, services) -> str:
    section, slug = active_content
    if section == "articles":
        item = next((article for article in articles if article.slug == slug), None)
        return _render_article_detail(item)
    if section == "products":
        item = next((product for product in products if product.slug == slug), None)
        return _render_product_detail(item)
    if section == "cases":
        item = next((case for case in cases if case.slug == slug), None)
        return _render_case_detail(item)
    if section == "services":
        item = next((service for service in services if service.slug == slug), None)
        return _render_service_detail(item)
    return ""


def _render_article_detail(item) -> str:
    if item is None:
        return ""
    return f"""
    <section class="pageList">
      <article class="panel feature">
        {_image(item.cover_image, item.title)}
        <div class="label">{_html(item.category or 'article')} / {_html(item.slug)}</div>
        <h2>{_html(item.title)}</h2>
        <div class="value">{_html(item.summary)}</div>
        <div class="value">{_paragraphs(item.body)}</div>
      </article>
    </section>"""


def _render_product_detail(item) -> str:
    if item is None:
        return ""
    return f"""
    <section class="pageList">
      <article class="panel feature">
        {_image(item.cover_image, item.name)}
        <div class="label">{_html(item.category or 'product')} / {_html(item.slug)}</div>
        <h2>{_html(item.name)}</h2>
        <div class="value"><strong>型号:</strong> {_html(item.model)}</div>
        <div class="value">{_html(item.summary)}</div>
        <div class="value">{_paragraphs(item.description)}</div>
        <div class="value"><strong>参数:</strong><br>{_paragraphs(item.specifications)}</div>
        <div class="value"><strong>价格说明:</strong> {_html(item.price_note)}</div>
      </article>
    </section>"""


def _render_case_detail(item) -> str:
    if item is None:
        return ""
    return f"""
    <section class="pageList">
      <article class="panel feature">
        {_image(item.cover_image, item.title)}
        <div class="label">{_html(item.industry or 'case')} / {_html(item.slug)}</div>
        <h2>{_html(item.title)}</h2>
        <div class="value"><strong>客户:</strong> {_html(item.client_name)}</div>
        <div class="value"><strong>时间:</strong> {_html(item.project_date)}</div>
        <div class="value">{_html(item.summary)}</div>
        <div class="value"><strong>挑战:</strong><br>{_paragraphs(item.challenge)}</div>
        <div class="value"><strong>方案:</strong><br>{_paragraphs(item.solution)}</div>
        <div class="value"><strong>结果:</strong><br>{_paragraphs(item.result)}</div>
      </article>
    </section>"""


def _render_service_detail(item) -> str:
    if item is None:
        return ""
    return f"""
    <section class="pageList">
      <article class="panel feature">
        <div class="label">{_html(item.category or 'service')} / {_html(item.slug)}</div>
        <h2>{_html(item.name)}</h2>
        <div class="value">{_html(item.summary)}</div>
        <div class="value"><strong>服务范围:</strong><br>{_paragraphs(item.scope)}</div>
        <div class="value"><strong>服务流程:</strong><br>{_paragraphs(item.process)}</div>
        <div class="value"><strong>交付物:</strong><br>{_paragraphs(item.deliverables)}</div>
        <div class="value"><strong>价格说明:</strong> {_html(item.price_note)}</div>
      </article>
    </section>"""
