import { Eye, Save } from "lucide-react";

import { CompanyProfile } from "../api";
import { Field } from "./Field";

type CompanyProfilePanelProps = {
  profile: CompanyProfile;
  onChange: (value: CompanyProfile) => void;
  onSave: () => void;
  onPreview: () => void;
};

export function CompanyProfilePanel({ profile, onChange, onSave, onPreview }: CompanyProfilePanelProps) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>企业档案</h2>
          <p>先沉淀企业基本事实，后续内容模块会复用这些资料。</p>
        </div>
        <div className="panelActions">
          <button className="secondaryButton compact" onClick={onPreview}>
            <Eye size={16} />
            档案预览
          </button>
          <button className="primaryButton compact" onClick={onSave}>
            <Save size={16} />
            保存档案
          </button>
        </div>
      </div>
      <div className="formGrid">
        <Field label="企业对外名称" tone="required" hint="官网上展示给访客看的公司名称。">
          <input
            value={profile.company_name}
            onChange={(event) => onChange({ ...profile, company_name: event.target.value })}
          />
        </Field>
        <Field label="工商/法定名称" hint="需要展示正式主体时填写，可留空。">
          <input
            value={profile.legal_name}
            onChange={(event) => onChange({ ...profile, legal_name: event.target.value })}
          />
        </Field>
        <Field label="所属行业" hint="例如智能制造、软件服务、教育培训。">
          <input value={profile.industry} onChange={(event) => onChange({ ...profile, industry: event.target.value })} />
        </Field>
        <Field label="联系电话" hint="会出现在官网联系信息中。">
          <input value={profile.phone} onChange={(event) => onChange({ ...profile, phone: event.target.value })} />
        </Field>
        <Field label="联系邮箱" hint="会出现在官网联系信息中。">
          <input value={profile.email} onChange={(event) => onChange({ ...profile, email: event.target.value })} />
        </Field>
        <Field label="服务区域" hint="例如全国、华东地区、上海及周边。">
          <input
            value={profile.service_area}
            onChange={(event) => onChange({ ...profile, service_area: event.target.value })}
          />
        </Field>
        <Field label="办公/联系地址" hint="会出现在官网联系信息中。" wide>
          <input value={profile.address} onChange={(event) => onChange({ ...profile, address: event.target.value })} />
        </Field>
        <Field label="企业介绍" tone="required" hint="对应官网企业档案区域，建议写 1-3 句话。" wide>
          <textarea
            value={profile.description}
            onChange={(event) => onChange({ ...profile, description: event.target.value })}
          />
        </Field>
      </div>
    </section>
  );
}
