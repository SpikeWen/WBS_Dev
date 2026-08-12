import { ArrowRight, ExternalLink, Gauge, Info } from "lucide-react";

import {
  Article,
  CaseStudy,
  CompanyProfile,
  ContentPage,
  FAQItem,
  MediaAsset,
  Product,
  PublishReadiness,
  PublishRecord,
  ServiceItem,
  Site,
  SiteProfile
} from "../api";

type WorkspaceSection =
  | "dashboard"
  | "identity"
  | "company"
  | "pages"
  | "articles"
  | "products"
  | "cases"
  | "services"
  | "faqs"
  | "media"
  | "publish"
  | "preview";

type SiteDashboardPanelProps = {
  site: Site;
  profile: SiteProfile;
  companyProfile: CompanyProfile;
  pages: ContentPage[];
  articles: Article[];
  products: Product[];
  faqs: FAQItem[];
  cases: CaseStudy[];
  services: ServiceItem[];
  assets: MediaAsset[];
  publishes: PublishRecord[];
  readiness: PublishReadiness | null;
  onNavigate: (section: WorkspaceSection) => void;
};

export function SiteDashboardPanel({
  site,
  profile,
  companyProfile,
  pages,
  articles,
  products,
  faqs,
  cases,
  services,
  assets,
  publishes,
  readiness,
  onNavigate
}: SiteDashboardPanelProps) {
  const moduleStats = [
    countStat("固定页面", pages),
    countStat("文章", articles),
    countStat("产品", products),
    countStat("案例", cases),
    countStat("服务", services),
    countStat("FAQ", faqs),
    { label: "媒体素材", total: assets.length, published: assets.length }
  ];
  const latestPublish = publishes[0] ?? null;
  const workflowSteps = getWorkflowSteps(profile, companyProfile, pages, services, readiness);

  return (
    <section className="panel dashboardPanel">
      <div className="panelHeader">
        <div>
          <h2>站点驾驶舱</h2>
          <p>汇总站点状态、内容数量和发布前基础检查。</p>
        </div>
        <a className="secondaryButton compact" href={`/api/sites/${site.id}/preview`} target="_blank" rel="noreferrer">
          <ExternalLink size={16} />
          前台预览
        </a>
      </div>

      <div className="dashboardGrid">
        <div className="dashboardSummary">
          <div className="summaryIcon">
            <Gauge size={22} />
          </div>
          <div>
            <strong>{site.name}</strong>
            <span>{site.status} / {site.template_id}</span>
          </div>
        </div>

        <div className="dashboardSummary">
          <div className="summaryIcon">
            <Info size={22} />
          </div>
          <div>
            <strong>{readinessLabel(readiness)}</strong>
            <span>{readiness?.issue_count ? `${readiness.issue_count} 条提示` : "基础资料检查通过"}</span>
          </div>
        </div>

        <div className="dashboardSummary">
          <div className="summaryIcon">
            <ExternalLink size={22} />
          </div>
          <div>
            <strong>{latestPublish ? latestPublish.version : "尚未发布"}</strong>
            <span>{latestPublish ? new Date(latestPublish.created_at).toLocaleString() : "发布后会生成静态版本"}</span>
          </div>
        </div>
      </div>

      <div className="moduleStatGrid">
        {moduleStats.map((item) => (
          <div className="moduleStat" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.total}</strong>
            <small>{item.published} 已发布/可用</small>
          </div>
        ))}
      </div>

      <div className="workflowStrip">
        {workflowSteps.map((step) => (
          <button className="workflowStep" key={step.section} onClick={() => onNavigate(step.section)}>
            <span>{step.label}</span>
            <strong>{step.title}</strong>
            <small>{step.detail}</small>
            <ArrowRight size={15} />
          </button>
        ))}
      </div>
    </section>
  );
}

function countStat<T extends { status: string }>(label: string, items: T[]) {
  return {
    label,
    total: items.length,
    published: items.filter((item) => item.status === "published").length
  };
}

function readinessLabel(readiness: PublishReadiness | null) {
  if (!readiness) {
    return "检查未加载";
  }
  if (!readiness.issue_count) {
    return "基础内容就绪";
  }
  return readiness.can_publish ? "可发布，有建议" : "存在发布风险";
}

function getWorkflowSteps(
  profile: SiteProfile,
  companyProfile: CompanyProfile,
  pages: ContentPage[],
  services: ServiceItem[],
  readiness: PublishReadiness | null
) {
  const steps: { label: string; title: string; detail: string; section: WorkspaceSection }[] = [];
  if (!profile.site_name.trim() || !profile.default_title.trim()) {
    steps.push({
      label: "第 1 步",
      title: "完善站点身份",
      detail: "对应官网顶部品牌和默认 SEO",
      section: "identity"
    });
  }
  if (!companyProfile.company_name.trim() || !companyProfile.description.trim()) {
    steps.push({
      label: "第 2 步",
      title: "填写企业档案",
      detail: "对应官网企业介绍和联系方式",
      section: "company"
    });
  }
  if (!pages.some((page) => page.status === "published")) {
    steps.push({
      label: "第 3 步",
      title: "创建固定页面",
      detail: "对应官网导航和基础页面",
      section: "pages"
    });
  }
  if (!services.some((service) => service.status === "published")) {
    steps.push({
      label: "第 4 步",
      title: "补充服务内容",
      detail: "对应官网服务展示区",
      section: "services"
    });
  }
  steps.push({
    label: readiness?.issue_count ? "检查" : "完成",
    title: readiness?.issue_count ? "查看发布提示" : "预览并发布",
    detail: readiness?.issue_count ? `${readiness.issue_count} 条提示可处理` : "基础内容已形成闭环",
    section: readiness?.issue_count ? "publish" : "preview"
  });
  return steps.slice(0, 4);
}
