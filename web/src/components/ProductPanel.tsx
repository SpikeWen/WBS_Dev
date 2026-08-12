import { FormEvent } from "react";
import { FileText, Plus } from "lucide-react";

import { MediaAsset, Product, ProductPayload } from "../api";
import { toSlug } from "../utils/slug";
import { AssetUrlInput } from "./AssetUrlInput";
import { ContentWorkbenchPanel } from "./ContentWorkbenchPanel";
import { Field } from "./Field";

type ProductPanelProps = {
  products: Product[];
  selectedId: string;
  draft: Product | null;
  newProduct: ProductPayload;
  assets: MediaAsset[];
  onNewChange: (value: ProductPayload) => void;
  onDraftChange: (value: Product) => void;
  onCreate: (event: FormEvent<HTMLFormElement>) => void;
  onSelect: (product: Product) => void;
  onSave: () => void;
  onRemove: () => void;
  onPreview: (product: Product) => void;
};

export function ProductPanel({
  products,
  selectedId,
  draft,
  newProduct,
  assets,
  onNewChange,
  onDraftChange,
  onCreate,
  onSelect,
  onSave,
  onRemove,
  onPreview
}: ProductPanelProps) {
  return (
    <ContentWorkbenchPanel
      title="产品资料"
      description="维护产品名称、型号、卖点、参数和价格说明，预览页会同步展示产品资料。"
      hasDraft={Boolean(draft)}
      saveLabel="保存产品"
      previewLabel="产品预览"
      onPreview={draft ? () => onPreview(draft) : undefined}
      onSave={onSave}
      onRemove={onRemove}
      createForm={
        <form className="pageCreate" onSubmit={onCreate}>
          <Field label="新产品名称" tone="required">
            <input
              value={newProduct.name}
              onChange={(event) =>
                onNewChange({
                  ...newProduct,
                  name: event.target.value,
                  slug: newProduct.slug || toSlug(event.target.value)
                })
              }
              placeholder="产品名称"
            />
          </Field>
          <Field label="页面短链接" tone="required" hint="系统会按名称自动生成，通常不用改。">
            <input
              value={newProduct.slug}
              onChange={(event) => onNewChange({ ...newProduct, slug: event.target.value })}
              placeholder="product-name"
            />
          </Field>
          <button className="secondaryButton" type="submit">
            <Plus size={16} />
            添加产品
          </button>
        </form>
      }
      list={
        <>
          {products.map((product) => (
            <button
              key={product.id}
              className={product.id === selectedId ? "pageItem active" : "pageItem"}
              onClick={() => onSelect(product)}
            >
              <FileText size={16} />
              <span>{product.name}</span>
              <small>{product.status} / {product.category || "未分类"}</small>
            </button>
          ))}
          {products.length === 0 && <div className="emptyState">还没有产品</div>}
        </>
      }
      editor={
        !draft ? (
          <div className="blankPanel slim">新增或选择一个产品。</div>
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
                onChange={(event) => onDraftChange({ ...draft, status: event.target.value as Product["status"] })}
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
            <Field label="型号">
              <input value={draft.model} onChange={(event) => onDraftChange({ ...draft, model: event.target.value })} />
            </Field>
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
            <Field label="产品介绍" wide>
              <textarea
                className="bodyEditor"
                value={draft.description}
                onChange={(event) => onDraftChange({ ...draft, description: event.target.value })}
              />
            </Field>
            <Field label="规格参数" wide>
              <textarea
                value={draft.specifications}
                onChange={(event) => onDraftChange({ ...draft, specifications: event.target.value })}
              />
            </Field>
            <Field label="价格说明" wide>
              <input
                value={draft.price_note}
                onChange={(event) => onDraftChange({ ...draft, price_note: event.target.value })}
              />
            </Field>
          </div>
        )
      }
    />
  );
}
