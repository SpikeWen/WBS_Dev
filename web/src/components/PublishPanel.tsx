import { AlertCircle, CheckCircle2, ExternalLink, Info, Rocket } from "lucide-react";

import { PublishReadiness, PublishRecord, ReadinessIssue } from "../api";

export function PublishPanel({
  publishes,
  readiness,
  onPublish
}: {
  publishes: PublishRecord[];
  readiness: PublishReadiness | null;
  onPublish: () => void;
}) {
  const hasIssues = Boolean(readiness?.issue_count);

  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>发布</h2>
          <p>将当前预览输出为静态 HTML，并保留发布历史。</p>
        </div>
        <button className="primaryButton compact" onClick={onPublish}>
          <Rocket size={16} />
          发布
        </button>
      </div>
      <div className={hasIssues ? "readinessBox" : "readinessBox ready"}>
        <div className="readinessTitle">
          {hasIssues ? <AlertCircle size={16} /> : <CheckCircle2 size={16} />}
          <span>{hasIssues ? `发布前检查：${readiness?.issue_count ?? 0} 条提示` : "发布前检查：基础内容已就绪"}</span>
        </div>
        {readiness?.issues.length ? (
          <div className="readinessList">
            {readiness.issues.map((issue) => (
              <div className={`readinessItem ${issue.level}`} key={`${issue.module}-${issue.message}`}>
                {issueIcon(issue)}
                <span>{issue.message}</span>
              </div>
            ))}
          </div>
        ) : (
          <p>当前没有阻碍预览发布的基础问题。</p>
        )}
      </div>
      <div className="publishList">
        {publishes.map((record) => (
          <div className="publishItem" key={record.id}>
            <div>
              <strong>{record.version}</strong>
              <small>{record.status} / {new Date(record.created_at).toLocaleString()}</small>
            </div>
            <a className="secondaryButton compact" href={record.publish_url} target="_blank" rel="noreferrer">
              <ExternalLink size={16} />
              查看
            </a>
          </div>
        ))}
        {publishes.length === 0 && <div className="emptyState">还没有发布记录</div>}
      </div>
    </section>
  );
}

function issueIcon(issue: ReadinessIssue) {
  if (issue.level === "error") {
    return <AlertCircle size={14} />;
  }
  if (issue.level === "warning") {
    return <AlertCircle size={14} />;
  }
  return <Info size={14} />;
}
