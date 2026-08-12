import { FormEvent } from "react";
import { FileText, Plus } from "lucide-react";

import { CasePayload, CaseStudy, MediaAsset } from "../api";
import { toSlug } from "../utils/slug";
import { AssetUrlInput } from "./AssetUrlInput";
import { ContentWorkbenchPanel } from "./ContentWorkbenchPanel";
import { Field } from "./Field";

type CasePanelProps = {
  cases: CaseStudy[];
  selectedId: string;
  draft: CaseStudy | null;
  newCase: CasePayload;
  assets: MediaAsset[];
  onNewChange: (value: CasePayload) => void;
  onDraftChange: (value: CaseStudy) => void;
  onCreate: (event: FormEvent<HTMLFormElement>) => void;
  onSelect: (caseItem: CaseStudy) => void;
  onSave: () => void;
  onRemove: () => void;
  onPreview: (caseItem: CaseStudy) => void;
};

export function CasePanel({
  cases,
  selectedId,
  draft,
  newCase,
  assets,
  onNewChange,
  onDraftChange,
  onCreate,
  onSelect,
  onSave,
  onRemove,
  onPreview
}: CasePanelProps) {
  return (
    <ContentWorkbenchPanel
      title="项目案例"
      description="维护客户案例、行业、挑战、方案和结果，预览页会同步展示项目证明。"
      hasDraft={Boolean(draft)}
      saveLabel="保存案例"
      previewLabel="案例预览"
      onPreview={draft ? () => onPreview(draft) : undefined}
      onSave={onSave}
      onRemove={onRemove}
      createForm={
        <form className="pageCreate" onSubmit={onCreate}>
          <Field label="新案例标题" tone="required">
            <input
              value={newCase.title}
              onChange={(event) =>
                onNewChange({
                  ...newCase,
                  title: event.target.value,
                  slug: newCase.slug || toSlug(event.target.value)
                })
              }
              placeholder="客户项目案例"
            />
          </Field>
          <Field label="页面短链接" tone="required" hint="系统会按标题自动生成，通常不用改。">
            <input value={newCase.slug} onChange={(event) => onNewChange({ ...newCase, slug: event.target.value })} placeholder="customer-case" />
          </Field>
          <button className="secondaryButton" type="submit">
            <Plus size={16} />
            添加案例
          </button>
        </form>
      }
      list={
        <>
          {cases.map((caseItem) => (
            <button
              key={caseItem.id}
              className={caseItem.id === selectedId ? "pageItem active" : "pageItem"}
              onClick={() => onSelect(caseItem)}
            >
              <FileText size={16} />
              <span>{caseItem.title}</span>
              <small>{caseItem.status} / {caseItem.industry || "未分类"}</small>
            </button>
          ))}
          {cases.length === 0 && <div className="emptyState">还没有案例</div>}
        </>
      }
      editor={
        !draft ? (
          <div className="blankPanel slim">新增或选择一个案例。</div>
        ) : (
          <div className="formGrid">
            <Field label="标题" tone="required">
              <input value={draft.title} onChange={(event) => onDraftChange({ ...draft, title: event.target.value })} />
            </Field>
            <Field label="页面短链接" tone="required" hint="系统会按标题自动生成，通常不用改。">
              <input value={draft.slug} onChange={(event) => onDraftChange({ ...draft, slug: event.target.value })} />
            </Field>
            <Field label="状态" hint="草稿不对外展示；发布会进入预览和发布；隐藏会从前台移除。">
              <select
                value={draft.status}
                onChange={(event) => onDraftChange({ ...draft, status: event.target.value as CaseStudy["status"] })}
              >
                <option value="draft">草稿</option>
                <option value="published">发布</option>
                <option value="hidden">隐藏</option>
              </select>
            </Field>
            <Field label="客户名称">
              <input value={draft.client_name} onChange={(event) => onDraftChange({ ...draft, client_name: event.target.value })} />
            </Field>
            <Field label="行业">
              <input value={draft.industry} onChange={(event) => onDraftChange({ ...draft, industry: event.target.value })} />
            </Field>
            <Field label="项目时间">
              <input value={draft.project_date} onChange={(event) => onDraftChange({ ...draft, project_date: event.target.value })} />
            </Field>
            <Field label="封面图" hint="从媒体素材中选择；不需要图片也可以留空。">
              <AssetUrlInput
                value={draft.cover_image}
                assets={assets}
                onChange={(value) => onDraftChange({ ...draft, cover_image: value })}
              />
            </Field>
            <Field label="摘要" wide>
              <textarea value={draft.summary} onChange={(event) => onDraftChange({ ...draft, summary: event.target.value })} />
            </Field>
            <Field label="挑战" wide>
              <textarea value={draft.challenge} onChange={(event) => onDraftChange({ ...draft, challenge: event.target.value })} />
            </Field>
            <Field label="方案" wide>
              <textarea className="bodyEditor" value={draft.solution} onChange={(event) => onDraftChange({ ...draft, solution: event.target.value })} />
            </Field>
            <Field label="结果" wide>
              <textarea value={draft.result} onChange={(event) => onDraftChange({ ...draft, result: event.target.value })} />
            </Field>
          </div>
        )
      }
    />
  );
}
