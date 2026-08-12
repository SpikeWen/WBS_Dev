import { FormEvent } from "react";
import { FileText, Plus } from "lucide-react";

import { ServiceItem, ServicePayload } from "../api";
import { toSlug } from "../utils/slug";
import { ContentWorkbenchPanel } from "./ContentWorkbenchPanel";
import { Field } from "./Field";

type ServicePanelProps = {
  services: ServiceItem[];
  selectedId: string;
  draft: ServiceItem | null;
  newService: ServicePayload;
  onNewChange: (value: ServicePayload) => void;
  onDraftChange: (value: ServiceItem) => void;
  onCreate: (event: FormEvent<HTMLFormElement>) => void;
  onSelect: (service: ServiceItem) => void;
  onSave: () => void;
  onRemove: () => void;
  onPreview: (service: ServiceItem) => void;
};

export function ServicePanel({
  services,
  selectedId,
  draft,
  newService,
  onNewChange,
  onDraftChange,
  onCreate,
  onSelect,
  onSave,
  onRemove,
  onPreview
}: ServicePanelProps) {
  return (
    <ContentWorkbenchPanel
      title="服务项目"
      description="维护服务名称、范围、流程、交付物和价格说明，预览页会同步展示服务能力。"
      hasDraft={Boolean(draft)}
      saveLabel="保存服务"
      previewLabel="服务预览"
      onPreview={draft ? () => onPreview(draft) : undefined}
      onSave={onSave}
      onRemove={onRemove}
      createForm={
        <form className="pageCreate" onSubmit={onCreate}>
          <Field label="新服务名称" tone="required">
            <input
              value={newService.name}
              onChange={(event) =>
                onNewChange({
                  ...newService,
                  name: event.target.value,
                  slug: newService.slug || toSlug(event.target.value)
                })
              }
              placeholder="官网后台实施服务"
            />
          </Field>
          <Field label="页面短链接" tone="required" hint="系统会按名称自动生成，通常不用改。">
            <input
              value={newService.slug}
              onChange={(event) => onNewChange({ ...newService, slug: event.target.value })}
              placeholder="website-cms-service"
            />
          </Field>
          <button className="secondaryButton" type="submit">
            <Plus size={16} />
            添加服务
          </button>
        </form>
      }
      list={
        <>
          {services.map((item) => (
            <button
              key={item.id}
              className={item.id === selectedId ? "pageItem active" : "pageItem"}
              onClick={() => onSelect(item)}
            >
              <FileText size={16} />
              <span>{item.name}</span>
              <small>{item.status} / {item.category || "未分类"}</small>
            </button>
          ))}
          {services.length === 0 && <div className="emptyState">还没有服务项目</div>}
        </>
      }
      editor={
        !draft ? (
          <div className="blankPanel slim">新增或选择一个服务项目。</div>
        ) : (
          <div className="formGrid">
            <Field label="名称" tone="required">
              <input value={draft.name} onChange={(event) => onDraftChange({ ...draft, name: event.target.value })} />
            </Field>
            <Field label="页面短链接" tone="required" hint="系统会按名称自动生成，通常不用改。">
              <input value={draft.slug} onChange={(event) => onDraftChange({ ...draft, slug: event.target.value })} />
            </Field>
            <Field label="状态" hint="草稿不对外展示；发布会进入预览和发布；隐藏会从前台移除。">
              <select
                value={draft.status}
                onChange={(event) => onDraftChange({ ...draft, status: event.target.value as ServiceItem["status"] })}
              >
                <option value="draft">草稿</option>
                <option value="published">发布</option>
                <option value="hidden">隐藏</option>
              </select>
            </Field>
            <Field label="分类">
              <input value={draft.category} onChange={(event) => onDraftChange({ ...draft, category: event.target.value })} />
            </Field>
            <Field label="价格说明">
              <input
                value={draft.price_note}
                onChange={(event) => onDraftChange({ ...draft, price_note: event.target.value })}
              />
            </Field>
            <Field label="摘要" wide>
              <textarea value={draft.summary} onChange={(event) => onDraftChange({ ...draft, summary: event.target.value })} />
            </Field>
            <Field label="服务范围" wide>
              <textarea value={draft.scope} onChange={(event) => onDraftChange({ ...draft, scope: event.target.value })} />
            </Field>
            <Field label="服务流程" wide>
              <textarea
                className="bodyEditor"
                value={draft.process}
                onChange={(event) => onDraftChange({ ...draft, process: event.target.value })}
              />
            </Field>
            <Field label="交付物" wide>
              <textarea value={draft.deliverables} onChange={(event) => onDraftChange({ ...draft, deliverables: event.target.value })} />
            </Field>
          </div>
        )
      }
    />
  );
}
