import { FormEvent } from "react";
import { FileText, Plus } from "lucide-react";

import { ContentPage, PagePayload } from "../api";
import { toSlug } from "../utils/slug";
import { ContentWorkbenchPanel } from "./ContentWorkbenchPanel";
import { Field } from "./Field";

type PagePanelProps = {
  pages: ContentPage[];
  selectedId: string;
  draft: ContentPage | null;
  newPage: PagePayload;
  onNewChange: (value: PagePayload) => void;
  onDraftChange: (value: ContentPage) => void;
  onCreate: (event: FormEvent<HTMLFormElement>) => void;
  onSelect: (page: ContentPage) => void;
  onSave: () => void;
  onRemove: () => void;
  onPreview: (page: ContentPage) => void;
};

export function PagePanel({
  pages,
  selectedId,
  draft,
  newPage,
  onNewChange,
  onDraftChange,
  onCreate,
  onSelect,
  onSave,
  onRemove,
  onPreview
}: PagePanelProps) {
  return (
    <ContentWorkbenchPanel
      title="页面树与固定页面"
      description="先维护官网基础页面，正文会同步进入空壳官网预览。"
      hasDraft={Boolean(draft)}
      saveLabel="保存页面"
      previewLabel="页面预览"
      onPreview={draft ? () => onPreview(draft) : undefined}
      onSave={onSave}
      onRemove={onRemove}
      createForm={
        <form className="pageCreate" onSubmit={onCreate}>
          <Field label="新页面标题" tone="required">
            <input
              value={newPage.title}
              onChange={(event) =>
                onNewChange({
                  ...newPage,
                  title: event.target.value,
                  slug: newPage.slug || toSlug(event.target.value)
                })
              }
              placeholder="关于我们"
            />
          </Field>
          <Field label="页面短链接" tone="required" hint="系统会按标题自动生成，通常不用改。">
            <input
              value={newPage.slug}
              onChange={(event) => onNewChange({ ...newPage, slug: event.target.value })}
              placeholder="about"
            />
          </Field>
          <button className="secondaryButton" type="submit">
            <Plus size={16} />
            添加页面
          </button>
        </form>
      }
      list={
        <>
          {pages.map((page) => (
            <button
              key={page.id}
              className={page.id === selectedId ? "pageItem active" : "pageItem"}
              onClick={() => onSelect(page)}
            >
              <FileText size={16} />
              <span>{page.title}</span>
              <small>{page.slug}</small>
            </button>
          ))}
          {pages.length === 0 && <div className="emptyState">还没有固定页面</div>}
        </>
      }
      editor={
        !draft ? (
          <div className="blankPanel slim">新增或选择一个固定页面。</div>
        ) : (
          <div className="formSections">
            <section className="formSection">
              <div className="formSectionIntro">
                <h3>页面基础设置</h3>
                <p>决定这个页面叫什么、在哪里访问、是否出现在前台导航。</p>
              </div>
              <div className="sectionGrid">
                <Field label="标题" tone="required">
                  <input value={draft.title} onChange={(event) => onDraftChange({ ...draft, title: event.target.value })} />
                </Field>
                <Field label="页面短链接" tone="required" hint="系统会按标题自动生成，通常不用改。">
                  <input value={draft.slug} onChange={(event) => onDraftChange({ ...draft, slug: event.target.value })} />
                </Field>
                <Field label="状态" hint="草稿不对外展示；发布会进入预览和发布；隐藏会从前台移除。">
                  <select
                    value={draft.status}
                    onChange={(event) => onDraftChange({ ...draft, status: event.target.value as ContentPage["status"] })}
                  >
                    <option value="draft">草稿</option>
                    <option value="published">发布</option>
                    <option value="hidden">隐藏</option>
                  </select>
                </Field>
                <Field label="排序" hint="数字越小越靠前。">
                  <input
                    type="number"
                    value={draft.sort_order}
                    onChange={(event) => onDraftChange({ ...draft, sort_order: Number(event.target.value) })}
                  />
                </Field>
                <Field label="导航显示" hint="控制这个页面是否出现在前台顶部导航。">
                  <label className="toggleField">
                    <input
                      type="checkbox"
                      checked={draft.show_in_nav}
                      onChange={(event) => onDraftChange({ ...draft, show_in_nav: event.target.checked })}
                    />
                    <span>显示在前台导航</span>
                  </label>
                </Field>
              </div>
            </section>
            <section className="formSection">
              <div className="formSectionIntro">
                <h3>页面正文</h3>
                <p>这部分会直接展示在前台页面里，是访客真正会阅读的内容。</p>
              </div>
              <div className="sectionGrid">
                <Field label="页面主标题" hint="对应前台页面正文顶部的大标题。">
                  <input value={draft.h1} onChange={(event) => onDraftChange({ ...draft, h1: event.target.value })} />
                </Field>
                <Field label="正文" wide>
                  <textarea
                    className="bodyEditor"
                    value={draft.body}
                    onChange={(event) => onDraftChange({ ...draft, body: event.target.value })}
                  />
                </Field>
              </div>
            </section>
            <section className="formSection">
              <div className="formSectionIntro">
                <h3>搜索展示</h3>
                <p>用于搜索引擎和浏览器标题，不会改变正文内容。</p>
              </div>
              <div className="sectionGrid">
                <Field label="SEO 标题">
                  <input
                    value={draft.meta_title}
                    onChange={(event) => onDraftChange({ ...draft, meta_title: event.target.value })}
                  />
                </Field>
                <Field label="SEO 描述" wide>
                  <textarea
                    value={draft.meta_description}
                    onChange={(event) => onDraftChange({ ...draft, meta_description: event.target.value })}
                  />
                </Field>
              </div>
            </section>
          </div>
        )
      }
    />
  );
}
