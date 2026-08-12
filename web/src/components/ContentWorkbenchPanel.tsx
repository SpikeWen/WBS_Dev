import { ReactNode } from "react";
import { Eye, Save, Trash2 } from "lucide-react";

export function ContentWorkbenchPanel({
  title,
  description,
  hasDraft,
  saveLabel,
  previewLabel = "对应预览",
  onPreview,
  onSave,
  onRemove,
  createForm,
  list,
  editor
}: {
  title: string;
  description: string;
  hasDraft: boolean;
  saveLabel: string;
  previewLabel?: string;
  onPreview?: () => void;
  onSave: () => void;
  onRemove: () => void;
  createForm: ReactNode;
  list: ReactNode;
  editor: ReactNode;
}) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
        <div className="panelActions">
          {onPreview && (
            <button className="secondaryButton compact" onClick={onPreview}>
              <Eye size={16} />
              {previewLabel}
            </button>
          )}
          <button className="dangerButton compact" onClick={onRemove} disabled={!hasDraft}>
            <Trash2 size={16} />
            删除
          </button>
          <button className="primaryButton compact" onClick={onSave} disabled={!hasDraft}>
            <Save size={16} />
            {saveLabel}
          </button>
        </div>
      </div>

      <div className="pageWorkbench">
        <div className="pageRail">
          {createForm}
          <div className="pageList">{list}</div>
        </div>
        <div className="pageEditor">{editor}</div>
      </div>
    </section>
  );
}
