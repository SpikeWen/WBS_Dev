type PreviewPanelProps = {
  siteId: string;
  previewVersion: number;
  target: {
    title: string;
    description: string;
    path: string;
  } | null;
};

export function PreviewPanel({
  siteId,
  previewVersion,
  target
}: PreviewPanelProps) {
  const preview = target ?? {
    title: "总体预览",
    description: "查看当前官网首页和整体内容。",
    path: `/api/sites/${siteId}/preview`
  };
  const separator = preview.path.includes("?") ? "&" : "?";

  return (
    <section className="panel previewPanel">
      <div className="panelHeader">
        <div>
          <h2>{preview.title}</h2>
          <p>{preview.description}</p>
        </div>
      </div>
      <iframe title={preview.title} src={`${preview.path}${separator}v=${previewVersion}`} />
    </section>
  );
}
