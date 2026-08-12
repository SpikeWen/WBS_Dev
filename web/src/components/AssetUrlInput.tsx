import { ImageIcon, Link2, X } from "lucide-react";

import { MediaAsset } from "../api";

type AssetUrlInputProps = {
  value: string;
  assets: MediaAsset[];
  onChange: (value: string) => void;
};

export function AssetUrlInput({ value, assets, onChange }: AssetUrlInputProps) {
  const imageAssets = assets.filter((asset) => asset.file_type.startsWith("image/"));
  const recentAssets = imageAssets.slice(0, 6);
  const selectedAsset = imageAssets.find((asset) => asset.url === value);

  return (
    <div className="assetUrlInput">
      <div className="assetPickerCurrent">
        <div className={value ? "assetPickerPreview" : "assetPickerPreview empty"}>
          {value ? <img src={value} alt={selectedAsset?.alt_text || selectedAsset?.filename || "已选择图片"} /> : <ImageIcon size={24} />}
        </div>
        <div className="assetPickerText">
          <strong>{selectedAsset?.filename || (value ? "已选择图片" : "尚未选择图片")}</strong>
          <span>{value ? "图片会用于当前字段对应的官网位置" : "从下方素材中点选一张图片"}</span>
        </div>
        {value && (
          <button className="iconButton" type="button" onClick={() => onChange("")} title="清除图片">
            <X size={15} />
          </button>
        )}
      </div>
      {recentAssets.length > 0 && (
        <div className="assetChoices">
          {recentAssets.map((asset) => (
            <button
              key={asset.id}
              type="button"
              className={asset.url === value ? "assetChoice active" : "assetChoice"}
              onClick={() => onChange(asset.url)}
              title={asset.alt_text || asset.filename}
            >
              <span className="assetThumb">
                <img src={asset.url} alt={asset.alt_text || asset.filename} />
              </span>
              <span>{asset.filename}</span>
            </button>
          ))}
        </div>
      )}
      {assets.length > 0 && recentAssets.length === 0 && (
        <div className="assetHint">
          <ImageIcon size={14} />
          当前素材库没有可选图片
        </div>
      )}
      {assets.length === 0 && (
        <div className="assetHint">
          <ImageIcon size={14} />
          还没有图片素材，请先到“媒体”模块上传
        </div>
      )}
      <details className="manualAssetUrl">
        <summary>
          <Link2 size={14} />
          手动填写图片地址
        </summary>
        <input value={value} onChange={(event) => onChange(event.target.value)} placeholder="/storage/..." />
      </details>
    </div>
  );
}
