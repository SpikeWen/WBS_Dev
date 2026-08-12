import { Eye, Save } from "lucide-react";

import { MediaAsset, Site, SiteProfile } from "../api";
import { AssetUrlInput } from "./AssetUrlInput";
import { Field } from "./Field";

type SiteIdentityPanelProps = {
  site: Site;
  profile: SiteProfile;
  assets: MediaAsset[];
  onSiteChange: (value: Site) => void;
  onProfileChange: (value: SiteProfile) => void;
  onSave: () => void;
  onPreview: () => void;
};

export function SiteIdentityPanel({
  site,
  profile,
  assets,
  onSiteChange,
  onProfileChange,
  onSave,
  onPreview
}: SiteIdentityPanelProps) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>站点身份</h2>
          <p>维护官网名称、模板、域名和默认 SEO。</p>
        </div>
        <div className="panelActions">
          <button className="secondaryButton compact" onClick={onPreview}>
            <Eye size={16} />
            顶部预览
          </button>
          <button className="primaryButton compact" onClick={onSave}>
            <Save size={16} />
            保存身份
          </button>
        </div>
      </div>
      <div className="formSections">
        <section className="formSection">
          <div className="formSectionIntro">
            <h3>项目基础信息</h3>
            <p>这些字段主要给后台和发布流程使用，用户通常只需要改站点名称和域名。</p>
          </div>
          <div className="sectionGrid">
            <Field label="站点名称" tone="required" hint="后台中识别这个官网项目的名称。">
              <input value={site.name} onChange={(event) => onSiteChange({ ...site, name: event.target.value })} />
            </Field>
            <Field label="模板" tone="required" hint="当前先使用 template_basic，后续可扩展更多官网模板。">
              <input
                value={site.template_id}
                onChange={(event) => onSiteChange({ ...site, template_id: event.target.value })}
              />
            </Field>
            <Field label="绑定域名" hint="没有正式域名可以先留空。">
              <input
                value={site.domain ?? ""}
                onChange={(event) => onSiteChange({ ...site, domain: event.target.value })}
              />
            </Field>
          </div>
        </section>
        <section className="formSection">
          <div className="formSectionIntro">
            <h3>官网顶部展示</h3>
            <p>这些内容会直接显示在官网顶部和首页首屏，优先填这里。</p>
          </div>
          <div className="sectionGrid">
            <Field label="官网显示名称" tone="required" hint="对应官网顶部品牌名和首页主标题。">
              <input
                value={profile.site_name}
                onChange={(event) => onProfileChange({ ...profile, site_name: event.target.value })}
              />
            </Field>
            <Field label="首页副标题" hint="对应官网首页主标题下方的一句话介绍。">
              <input
                value={profile.subtitle}
                onChange={(event) => onProfileChange({ ...profile, subtitle: event.target.value })}
              />
            </Field>
            <Field label="Logo 图片" hint="从媒体素材中选择，显示在官网顶部品牌旁边。">
              <AssetUrlInput
                value={profile.logo}
                assets={assets}
                onChange={(value) => onProfileChange({ ...profile, logo: value })}
              />
            </Field>
            <Field label="浏览器图标" hint="从媒体素材中选择，显示在浏览器标签页，可暂时留空。">
              <AssetUrlInput
                value={profile.favicon}
                assets={assets}
                onChange={(value) => onProfileChange({ ...profile, favicon: value })}
              />
            </Field>
          </div>
        </section>
        <section className="formSection">
          <div className="formSectionIntro">
            <h3>搜索展示</h3>
            <p>用于浏览器标题和搜索摘要，不会作为正文直接显示。</p>
          </div>
          <div className="sectionGrid">
            <Field label="SEO 默认标题" tone="required" hint="没有单独页面标题时使用。">
              <input
                value={profile.default_title}
                onChange={(event) => onProfileChange({ ...profile, default_title: event.target.value })}
              />
            </Field>
            <Field label="SEO 默认描述" hint="搜索结果和页面摘要使用的一段说明。" wide>
              <textarea
                value={profile.default_description}
                onChange={(event) => onProfileChange({ ...profile, default_description: event.target.value })}
              />
            </Field>
          </div>
        </section>
      </div>
    </section>
  );
}
