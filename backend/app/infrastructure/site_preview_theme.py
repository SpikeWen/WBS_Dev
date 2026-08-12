PREVIEW_CSS = """
    :root { color: #172033; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #eef3f7; scroll-behavior: smooth; }
    * { box-sizing: border-box; }
    body { margin: 0; background: #eef3f7; color: #172033; }
    .siteHeader { position: sticky; top: 0; z-index: 5; background: rgba(255, 255, 255, 0.96); border-bottom: 1px solid #d8e0ea; backdrop-filter: blur(10px); }
    .navShell, .heroShell, .wrap, .footerShell { width: min(1680px, calc(100% - 40px)); margin: 0 auto; }
    .navShell { min-height: 72px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
    .brand { display: inline-flex; align-items: center; gap: 10px; color: #101828; font-weight: 800; text-decoration: none; }
    .logo { width: 38px; height: 38px; border-radius: 8px; object-fit: contain; border: 1px solid #d7dee8; background: #fff; }
    .navLinks { display: flex; align-items: center; justify-content: flex-end; gap: 6px; flex-wrap: wrap; }
    .navLink { color: #315a92; text-decoration: none; border: 1px solid transparent; border-radius: 999px; padding: 8px 11px; font-size: 13px; background: transparent; }
    .navLink:hover { background: #eef5ff; border-color: #c7d8f2; }
    .navLink.active { color: #fff; background: #214f8f; border-color: #214f8f; }
    .navLink:focus-visible { outline: 2px solid #88aee8; outline-offset: 2px; }
    body:has(#pages:target) .navLink.homeLink.active,
    body:has(#services:target) .navLink.homeLink.active,
    body:has(#products:target) .navLink.homeLink.active,
    body:has(#cases:target) .navLink.homeLink.active,
    body:has(#articles:target) .navLink.homeLink.active,
    body:has(#faq:target) .navLink.homeLink.active,
    body:has(#contact:target) .navLink.homeLink.active { color: #315a92; background: transparent; border-color: transparent; }
    body:has(#pages:target) .navLink[href="#pages"],
    body:has(#services:target) .navLink[href="#services"],
    body:has(#products:target) .navLink[href="#products"],
    body:has(#cases:target) .navLink[href="#cases"],
    body:has(#articles:target) .navLink[href="#articles"],
    body:has(#faq:target) .navLink[href="#faq"],
    body:has(#contact:target) .navLink[href="#contact"] { color: #fff; background: #214f8f; border-color: #214f8f; }
    .heroBand { background: linear-gradient(135deg, #f8fbff 0%, #ffffff 46%, #e8f3ef 100%); border-bottom: 1px solid #d8e0ea; }
    .heroShell { min-height: 500px; display: grid; align-items: center; padding: 72px 0; }
    .heroSingle { grid-template-columns: minmax(0, 1fr); }
    .heroCopy { max-width: 1160px; }
    h1 { margin: 0 0 16px; max-width: 1080px; font-size: clamp(44px, 5.4vw, 92px); line-height: 1; letter-spacing: 0; }
    a { color: #315eaa; }
    .lead, .muted { color: #526075; font-size: 20px; line-height: 1.65; max-width: 820px; }
    .heroActions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
    .primaryCta, .ghostCta { display: inline-flex; min-height: 44px; align-items: center; justify-content: center; border-radius: 6px; padding: 0 18px; font-weight: 800; text-decoration: none; }
    .primaryCta { background: #214f8f; color: #fff; }
    .ghostCta { border: 1px solid #b8c8dc; color: #214f8f; background: #fff; }
    .wrap { padding: 42px 0 72px; }
    .aboutBand { display: grid; grid-template-columns: minmax(240px, .38fr) minmax(0, .62fr); gap: 32px; align-items: start; border: 1px solid #d8e0ea; border-radius: 8px; background: #fff; padding: 30px; box-shadow: 0 14px 34px rgba(23, 32, 51, 0.05); }
    .aboutBand h2 { margin: 8px 0 0; font-size: 32px; line-height: 1.18; }
    .aboutText { color: #334155; font-size: 17px; line-height: 1.75; white-space: pre-wrap; }
    .contentSection { scroll-margin-top: 94px; padding: 42px 0 18px; }
    .sectionHeader { max-width: 820px; margin-bottom: 18px; }
    .sectionHeader p { margin: 10px 0 0; color: #607086; font-size: 15px; line-height: 1.6; }
    .panel { min-width: 0; background: #fff; border: 1px solid #d8e0ea; border-radius: 8px; padding: 22px; box-shadow: 0 10px 28px rgba(23, 32, 51, 0.04); }
    .panel.feature { padding: 30px; }
    .panel h2 { margin: 8px 0 10px; font-size: 23px; line-height: 1.2; }
    .cover { display: block; width: 100%; max-height: 340px; object-fit: cover; border-radius: 6px; border: 1px solid #d7dee8; margin-bottom: 14px; background: #fff; }
    .label { font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: .04em; font-weight: 800; }
    .value { margin-top: 7px; color: #334155; font-size: 15px; line-height: 1.65; white-space: pre-wrap; }
    .pageList { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 16px; }
    .sectionTitle { margin: 0; font-size: 34px; letter-spacing: 0; }
    .pageList .panel.feature { grid-column: 1 / -1; }
    .siteFooter { scroll-margin-top: 94px; background: #101828; color: #fff; }
    .footerShell { min-height: 230px; display: flex; align-items: center; justify-content: space-between; gap: 36px; padding: 44px 0; }
    .siteFooter .label, .siteFooter .value { color: #b9c3d1; }
    .siteFooter h2 { margin: 8px 0 0; font-size: 30px; }
    .footerContact { display: grid; gap: 9px; color: #e6edf6; text-align: right; }
    .footerContact span:empty { display: none; }
    @media (max-width: 1180px) {
      .heroShell { grid-template-columns: 1fr; min-height: auto; }
      .pageList { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .aboutBand { grid-template-columns: 1fr; }
    }
    @media (max-width: 760px) {
      .navShell, .heroShell, .wrap, .footerShell { width: min(100% - 28px, 1680px); }
      .navShell { align-items: flex-start; flex-direction: column; padding: 14px 0; }
      .heroShell { padding: 42px 0; gap: 24px; }
      .pageList { grid-template-columns: 1fr; }
      .footerShell { align-items: flex-start; flex-direction: column; }
      .footerContact { text-align: left; }
    }
"""


def render_preview_document(body_html: str, title: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
{PREVIEW_CSS}
  </style>
</head>
<body>
{body_html}
</body>
</html>"""
