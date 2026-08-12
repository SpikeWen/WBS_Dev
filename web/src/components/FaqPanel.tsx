import { FormEvent } from "react";
import { FileText, Plus } from "lucide-react";

import { FAQItem, FAQPayload } from "../api";
import { ContentWorkbenchPanel } from "./ContentWorkbenchPanel";
import { Field } from "./Field";

type FaqPanelProps = {
  faqs: FAQItem[];
  selectedId: string;
  draft: FAQItem | null;
  newFaq: FAQPayload;
  onNewChange: (value: FAQPayload) => void;
  onDraftChange: (value: FAQItem) => void;
  onCreate: (event: FormEvent<HTMLFormElement>) => void;
  onSelect: (faq: FAQItem) => void;
  onSave: () => void;
  onRemove: () => void;
};

export function FaqPanel({
  faqs,
  selectedId,
  draft,
  newFaq,
  onNewChange,
  onDraftChange,
  onCreate,
  onSelect,
  onSave,
  onRemove
}: FaqPanelProps) {
  return (
    <ContentWorkbenchPanel
      title="FAQ"
      description="维护客户常见问题，预览页会同步展示问答内容。"
      hasDraft={Boolean(draft)}
      saveLabel="保存 FAQ"
      onSave={onSave}
      onRemove={onRemove}
      createForm={
        <form className="pageCreate" onSubmit={onCreate}>
          <Field label="新问题" tone="required">
            <input
              value={newFaq.question}
              onChange={(event) => onNewChange({ ...newFaq, question: event.target.value })}
              placeholder="交付周期是多久？"
            />
          </Field>
          <Field label="分类">
            <input
              value={newFaq.category ?? ""}
              onChange={(event) => onNewChange({ ...newFaq, category: event.target.value })}
              placeholder="交付"
            />
          </Field>
          <button className="secondaryButton" type="submit">
            <Plus size={16} />
            添加 FAQ
          </button>
        </form>
      }
      list={
        <>
          {faqs.map((faq) => (
            <button
              key={faq.id}
              className={faq.id === selectedId ? "pageItem active" : "pageItem"}
              onClick={() => onSelect(faq)}
            >
              <FileText size={16} />
              <span>{faq.question}</span>
              <small>{faq.status} / {faq.category || "未分类"}</small>
            </button>
          ))}
          {faqs.length === 0 && <div className="emptyState">还没有 FAQ</div>}
        </>
      }
      editor={
        !draft ? (
          <div className="blankPanel slim">新增或选择一条 FAQ。</div>
        ) : (
          <div className="formGrid">
            <Field label="问题" tone="required" wide>
              <input
                value={draft.question}
                onChange={(event) => onDraftChange({ ...draft, question: event.target.value })}
              />
            </Field>
            <Field label="状态" hint="草稿不对外展示；发布会进入预览和发布；隐藏会从前台移除。">
              <select
                value={draft.status}
                onChange={(event) => onDraftChange({ ...draft, status: event.target.value as FAQItem["status"] })}
              >
                <option value="draft">草稿</option>
                <option value="published">发布</option>
                <option value="hidden">隐藏</option>
              </select>
            </Field>
            <Field label="分类">
              <input
                value={draft.category}
                onChange={(event) => onDraftChange({ ...draft, category: event.target.value })}
              />
            </Field>
            <Field label="排序">
              <input
                type="number"
                value={draft.sort_order}
                onChange={(event) => onDraftChange({ ...draft, sort_order: Number(event.target.value) })}
              />
            </Field>
            <Field label="回答" wide>
              <textarea className="bodyEditor" value={draft.answer} onChange={(event) => onDraftChange({ ...draft, answer: event.target.value })} />
            </Field>
          </div>
        )
      }
    />
  );
}
