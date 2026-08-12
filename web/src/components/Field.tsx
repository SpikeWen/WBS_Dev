import { ReactNode } from "react";

export function Field({
  label,
  hint,
  tone = "optional",
  wide = false,
  children
}: {
  label: string;
  hint?: string;
  tone?: "required" | "optional" | "readonly" | "system";
  wide?: boolean;
  children: ReactNode;
}) {
  return (
    <label className={`${wide ? "field wide" : "field"} ${tone === "readonly" || tone === "system" ? "staticField" : ""}`}>
      <span className="fieldLabel">
        <span>{label}</span>
        <em className={`fieldBadge ${tone}`}>{toneLabel(tone)}</em>
      </span>
      {hint && <small>{hint}</small>}
      {children}
    </label>
  );
}

function toneLabel(tone: "required" | "optional" | "readonly" | "system") {
  if (tone === "required") return "必填";
  if (tone === "readonly") return "只读";
  if (tone === "system") return "系统";
  return "选填";
}
