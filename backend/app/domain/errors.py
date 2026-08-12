class DuplicateSlugError(Exception):
    def __init__(self, slug: str | None = None) -> None:
        message = f"slug 已存在：{slug}" if slug else "slug 已存在"
        super().__init__(message)
