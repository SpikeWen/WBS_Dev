import { FormEvent } from "react";
import { ImageIcon, Save, Trash2, Upload } from "lucide-react";

import { MediaAsset } from "../api";
import { Field } from "./Field";

type MediaPanelProps = {
  assets: MediaAsset[];
  selectedAssetId: string;
  assetDraft: MediaAsset | null;
  assetFile: File | null;
  assetAltText: string;
  onUpload: (event: FormEvent<HTMLFormElement>) => void;
  onFileChange: (file: File | null) => void;
  onAltTextChange: (value: string) => void;
  onSelect: (asset: MediaAsset) => void;
  onDraftChange: (asset: MediaAsset) => void;
  onSave: () => void;
  onRemove: () => void;
};

export function MediaPanel({
  assets,
  selectedAssetId,
  assetDraft,
  assetFile,
  assetAltText,
  onUpload,
  onFileChange,
  onAltTextChange,
  onSelect,
  onDraftChange,
  onSave,
  onRemove
}: MediaPanelProps) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>媒体素材</h2>
          <p>上传图片或文件，之后可在 Logo、封面图等位置直接选择。</p>
        </div>
        <div className="panelActions">
          <button className="dangerButton compact" onClick={onRemove} disabled={!assetDraft}>
            <Trash2 size={16} />
            删除
          </button>
        </div>
      </div>

      <div className="mediaWorkbench">
        <form className="pageCreate" onSubmit={onUpload}>
          <Field label="选择文件" tone="required" hint="从本地选择要上传的图片或文件。">
            <input
              key={assetFile?.name ?? "empty-file"}
              type="file"
              onChange={(event) => onFileChange(event.target.files?.[0] ?? null)}
            />
          </Field>
          <Field label="Alt 文本" hint="图片无法显示时的说明，也有助于 SEO。">
            <input
              value={assetAltText}
              onChange={(event) => onAltTextChange(event.target.value)}
              placeholder="图片说明"
            />
          </Field>
          <button className="secondaryButton" type="submit">
            <Upload size={16} />
            上传素材
          </button>
        </form>

        <div className="assetGrid">
          <div className="assetList">
            {assets.map((asset) => (
              <button
                key={asset.id}
                className={asset.id === selectedAssetId ? "assetItem active" : "assetItem"}
                onClick={() => onSelect(asset)}
              >
                <ImageIcon size={16} />
                <span>{asset.filename}</span>
                <small>{formatBytes(asset.size)} / {asset.file_type}</small>
              </button>
            ))}
            {assets.length === 0 && <div className="emptyState">还没有媒体素材</div>}
          </div>

          <div className="pageEditor">
            {!assetDraft && <div className="blankPanel slim">上传或选择一个媒体素材。</div>}
            {assetDraft && (
              <div className="formGrid">
                <Field label="文件名" tone="readonly" hint="上传后由系统记录。">
                  <input value={assetDraft.filename} readOnly />
                </Field>
                <Field label="类型" tone="readonly" hint="系统识别的文件 MIME 类型。">
                  <input value={assetDraft.file_type} readOnly />
                </Field>
                <Field label="大小" tone="readonly" hint="系统计算的文件大小。">
                  <input value={formatBytes(assetDraft.size)} readOnly />
                </Field>
                <Field label="系统链接" tone="system" hint="系统自动生成，普通用户不需要手动修改。" wide>
                  <input value={assetDraft.url} readOnly />
                </Field>
                <Field label="图片说明" hint="上传时已经保存；后续改动说明时再点击更新。" wide>
                  <div className="inlineEdit">
                    <input
                      value={assetDraft.alt_text}
                      onChange={(event) => onDraftChange({ ...assetDraft, alt_text: event.target.value })}
                    />
                    <button className="secondaryButton compact" type="button" onClick={onSave}>
                      <Save size={16} />
                      更新说明
                    </button>
                  </div>
                </Field>
                {assetDraft.file_type.startsWith("image/") && (
                  <div className="assetPreview">
                    <img src={assetDraft.url} alt={assetDraft.alt_text || assetDraft.filename} />
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

function formatBytes(value: number) {
  if (value < 1024) {
    return `${value} B`;
  }
  if (value < 1024 * 1024) {
    return `${(value / 1024).toFixed(1)} KB`;
  }
  return `${(value / (1024 * 1024)).toFixed(1)} MB`;
}
