import { FormEvent } from "react";
import { FileText, Plus } from "lucide-react";

import { Article, ArticlePayload, MediaAsset } from "../api";
import { toSlug } from "../utils/slug";
import { AssetUrlInput } from "./AssetUrlInput";
import { ContentWorkbenchPanel } from "./ContentWorkbenchPanel";
import { Field } from "./Field";

type ArticlePanelProps = {
  articles: Article[];
  selectedId: string;
  draft: Article | null;
  newArticle: ArticlePayload;
  assets: MediaAsset[];
  onNewChange: (value: ArticlePayload) => void;
  onDraftChange: (value: Article) => void;
  onCreate: (event: FormEvent<HTMLFormElement>) => void;
  onSelect: (article: Article) => void;
  onSave: () => void;
  onRemove: () => void;
  onPreview: (article: Article) => void;
};

export function ArticlePanel({
  articles,
  selectedId,
  draft,
  newArticle,
  assets,
  onNewChange,
  onDraftChange,
  onCreate,
  onSelect,
  onSave,
  onRemove,
  onPreview
}: ArticlePanelProps) {
  return (
    <ContentWorkbenchPanel
      title="资讯文章"
      description="维护新闻、动态和知识内容，预览页会同步展示文章列表。"
      hasDraft={Boolean(draft)}
      saveLabel="保存文章"
      previewLabel="文章预览"
      onPreview={draft ? () => onPreview(draft) : undefined}
      onSave={onSave}
      onRemove={onRemove}
      createForm={
        <form className="pageCreate" onSubmit={onCreate}>
          <Field label="新文章标题" tone="required">
            <input
              value={newArticle.title}
              onChange={(event) =>
                onNewChange({
                  ...newArticle,
                  title: event.target.value,
                  slug: newArticle.slug || toSlug(event.target.value)
                })
              }
              placeholder="企业动态标题"
            />
          </Field>
          <Field label="页面短链接" tone="required" hint="系统会按标题自动生成，通常不用改。">
            <input
              value={newArticle.slug}
              onChange={(event) => onNewChange({ ...newArticle, slug: event.target.value })}
              placeholder="news-title"
            />
          </Field>
          <button className="secondaryButton" type="submit">
            <Plus size={16} />
            添加文章
          </button>
        </form>
      }
      list={
        <>
          {articles.map((article) => (
            <button
              key={article.id}
              className={article.id === selectedId ? "pageItem active" : "pageItem"}
              onClick={() => onSelect(article)}
            >
              <FileText size={16} />
              <span>{article.title}</span>
              <small>{article.status} / {article.category || "未分类"}</small>
            </button>
          ))}
          {articles.length === 0 && <div className="emptyState">还没有文章</div>}
        </>
      }
      editor={
        !draft ? (
          <div className="blankPanel slim">新增或选择一篇文章。</div>
        ) : (
          <div className="formSections">
            <section className="formSection">
              <div className="formSectionIntro">
                <h3>文章基础信息</h3>
                <p>决定文章标题、访问地址、分类和发布状态。</p>
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
                    onChange={(event) => onDraftChange({ ...draft, status: event.target.value as Article["status"] })}
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
              </div>
            </section>
            <section className="formSection">
              <div className="formSectionIntro">
                <h3>前台展示内容</h3>
                <p>摘要用于文章列表，正文用于详情页；封面图可以先不填。</p>
              </div>
              <div className="sectionGrid">
                <Field label="封面图" hint="从媒体素材中选择；不需要图片也可以留空。">
                  <AssetUrlInput
                    value={draft.cover_image}
                    assets={assets}
                    onChange={(value) => onDraftChange({ ...draft, cover_image: value })}
                  />
                </Field>
                <Field label="摘要" wide>
                  <textarea
                    value={draft.summary}
                    onChange={(event) => onDraftChange({ ...draft, summary: event.target.value })}
                  />
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
          </div>
        )
      }
    />
  );
}
