# WBS Dev Backend

Minimal FastAPI scaffold for the WBS site management system.

## Run

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/backend
../.venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If `web/dist` exists, the backend also serves the built admin UI at `/`.

## First endpoints

- `GET /health`
- `POST /api/sites`
- `GET /api/sites`
- `GET /api/sites/{site_id}`
- `PATCH /api/sites/{site_id}`
- `GET /api/sites/{site_id}/status`
- `GET/PUT /api/sites/{site_id}/profile`
- `GET/PUT /api/sites/{site_id}/company-profile`
- `GET/POST /api/sites/{site_id}/pages`
- `PATCH/DELETE /api/pages/{page_id}`
- `GET/POST /api/sites/{site_id}/articles`
- `PATCH/DELETE /api/articles/{article_id}`
- `GET/POST /api/sites/{site_id}/products`
- `PATCH/DELETE /api/products/{product_id}`
- `GET/POST /api/sites/{site_id}/faqs`
- `PATCH/DELETE /api/faqs/{faq_id}`
- `GET/POST /api/sites/{site_id}/cases`
- `PATCH/DELETE /api/cases/{case_id}`
- `GET/POST /api/sites/{site_id}/services`
- `PATCH/DELETE /api/services/{service_id}`
- `GET/POST /api/sites/{site_id}/assets`
- `PATCH/DELETE /api/assets/{asset_id}`
- `POST /api/sites/{site_id}/publish`
- `GET /api/sites/{site_id}/publishes`
- `GET /api/sites/{site_id}/preview`
- `GET /api/sites/{site_id}/preview/pages/{slug}`
- `GET /api/sites/{site_id}/preview/articles/{slug}`
- `GET /api/sites/{site_id}/preview/products/{slug}`
- `GET /api/sites/{site_id}/preview/cases/{slug}`
- `GET /api/sites/{site_id}/preview/services/{slug}`

## Test

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/backend
../.venv/bin/python -m unittest discover -s tests
```
