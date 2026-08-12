from dataclasses import dataclass, field
from enum import StrEnum


class ReadinessLevel(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(slots=True)
class ReadinessIssue:
    level: ReadinessLevel
    module: str
    message: str


@dataclass(slots=True)
class SitePublishReadiness:
    site_id: str
    can_publish: bool
    issue_count: int
    issues: list[ReadinessIssue] = field(default_factory=list)
