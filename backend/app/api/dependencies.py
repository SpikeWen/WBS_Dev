from fastapi import Request

from app.application.site_service import SiteApplicationService


def get_site_service(request: Request) -> SiteApplicationService:
    return request.app.state.site_service
