# WBS_Dev 企业官网后台管理系统

WBS_Dev 是一个面向企业官网的后台管理系统 / 模板建站系统 MVP。

它不是一次性自动生成器。系统的核心目标是让客户先创建一个空壳官网，再在后台持续维护站点身份、企业档案、页面、文章、产品、案例、服务、FAQ 和媒体素材。前台官网预览和发布结果会根据后台内容实时更新。

AWA 诊断能力在本项目中只作为后续可选插件，不是建站、预览、发布的强制门禁。

## 当前状态

当前版本已经跑通 MVP 主链路：

- 创建和选择站点。
- 维护站点身份：站点名称、模板、域名、官网显示名、Logo、Favicon、默认 SEO。
- 维护企业档案：企业名称、法定名称、行业、简介、电话、邮箱、地址、服务区域。
- 维护固定页面，并控制状态、排序和是否显示在前台导航。
- 维护文章、产品、案例、服务、FAQ。
- 上传媒体素材，并在 Logo、Favicon、文章/产品/案例封面等字段中直接选择图片。
- 保存内容后刷新前台预览。
- 预览首页、固定页面、文章详情、产品详情、案例详情、服务详情。
- 在后台当前窗口查看模块聚焦预览。
- 发布静态 HTML，并保留发布记录。
- 发布前内容检查给出非强制提示，不阻止发布。

## 技术栈

- 后端：FastAPI
- 前端：React + TypeScript + Vite
- 数据库：SQLite
- 前台预览渲染：Python HTML 渲染器，后续可替换为 Jinja2 或模板引擎
- 文件存储：本地 `storage/`
- 发布输出：本地 `exports/`

## 目录结构

```text
WBS_Dev/
  backend/
    app/
      api/              # FastAPI 路由，请求响应编排
      application/      # 应用服务，组织站点、内容、发布等用例
      domain/           # 领域实体、状态、错误、仓储接口
      infrastructure/   # SQLite、本地文件、预览渲染等基础设施实现
      schemas/          # API 请求和响应模型
    tests/              # 后端 MVP 流程测试
    README.md
  web/
    src/
      components/       # 后台管理界面组件
      api.ts            # 前端 API 类型和请求封装
      App.tsx           # 前端应用编排
      styles.css        # 后台 UI 样式
    README.md
  docs/
    README.md
    01_开发原则与代码规范.md
    02_系统分层与模块边界.md
    03_数据模型与接口契约.md
    04_实施阶段与验收标准.md
    05_实施总纲与开发顺序.md
    06_开发进度记录.md
    07_MVP验收清单.md
  storage/              # 上传素材保存目录，本地运行时生成
  exports/              # 发布后的静态 HTML 输出目录，本地运行时生成
  企业官网后台管理系统技术设计报告.md
```

## 分层原则

项目遵循低耦合、高内聚、单向依赖：

- UI 只调用应用层暴露的接口。
- 应用层只依赖领域模型和仓储抽象。
- 基础设施层负责 SQLite、本地文件、模板渲染和外部能力适配。
- 页面组件不写业务规则。
- API 路由不直接写复杂业务判断。
- AWA 不进入主流程强依赖。

## 本地运行

### 1. 安装后端依赖

项目当前使用根目录下的 `.venv`。

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev
./.venv/bin/python -m pip install fastapi "uvicorn[standard]" python-multipart
```

### 2. 安装前端依赖

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/web
npm install
```

### 3. 构建前端

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/web
npm run build
```

构建结果会输出到 `web/dist/`。后端检测到 `web/dist/` 后，会在 `/` 托管后台管理界面。

### 4. 启动后端

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/backend
../.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

打开：

```text
http://127.0.0.1:8000/
```

健康检查：

```text
http://127.0.0.1:8000/health
```

### 5. 前端开发模式

如果本地环境允许 Vite 绑定端口，可以单独启动前端开发服务：

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/web
npm run dev
```

后端 CORS 当前允许：

- `http://localhost:5173`
- `http://127.0.0.1:5173`

在端口受限环境中，推荐使用“先 `npm run build`，再由后端托管 `web/dist`”的方式。

## 测试与验证

后端测试：

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/backend
../.venv/bin/python -m unittest discover -s tests
```

前端构建：

```bash
cd /home/shaochen/Intern_Dev/WBS_Dev/web
npm run build
```

推荐每次提交前至少跑这两条命令。

## 后台使用流程

建议按以下顺序录入内容：

1. 创建站点。
2. 进入站点驾驶舱，查看下一步提示。
3. 填写站点身份，优先维护官网显示名称、首页副标题、Logo、默认 SEO。
4. 填写企业档案，维护企业介绍和联系方式。
5. 创建固定页面，例如关于我们、资质、流程。
6. 创建服务、产品、案例、文章、FAQ。
7. 在媒体模块上传图片素材。
8. 在 Logo、Favicon、封面图等字段中选择已上传素材。
9. 使用模块内预览查看当前内容对应的前台片段。
10. 使用总体预览查看完整官网。
11. 进入发布模块，查看发布前检查并执行发布。

## 数据和文件

### SQLite 数据库

当前使用 SQLite 起步，仓储实现在：

```text
backend/app/infrastructure/sqlite_site_repository.py
```

### 上传素材

素材上传后保存在：

```text
storage/sites/{site_id}/assets/
```

素材会通过后端静态路径访问：

```text
/storage/sites/{site_id}/assets/{filename}
```

### 发布结果

执行发布后，静态 HTML 输出到：

```text
exports/{site_id}/{version}/
```

后端会挂载为：

```text
/published/{site_id}/{version}/index.html
```

## API 总览

后端所有业务接口统一挂在 `/api` 下。

### 基础

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/health` | 服务健康检查 |

### 站点

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/sites` | 创建站点 |
| GET | `/api/sites` | 获取站点列表 |
| GET | `/api/sites/{site_id}` | 获取站点详情 |
| PATCH | `/api/sites/{site_id}` | 更新站点基础信息 |
| GET | `/api/sites/{site_id}/status` | 获取站点状态摘要 |

创建站点示例：

```bash
curl -X POST http://127.0.0.1:8000/api/sites \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "default",
    "name": "示例企业官网",
    "template_id": "template_basic",
    "domain": ""
  }'
```

### 站点身份

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/profile` | 获取站点身份 |
| PUT | `/api/sites/{site_id}/profile` | 更新站点身份 |

字段：

- `site_name`：官网顶部品牌名和首页主标题。
- `subtitle`：首页主标题下方一句话介绍。
- `logo`：Logo 图片 URL，通常来自媒体素材。
- `favicon`：浏览器标签图标 URL，通常来自媒体素材。
- `default_title`：默认 SEO 标题。
- `default_description`：默认 SEO 描述。

### 企业档案

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/company-profile` | 获取企业档案 |
| PUT | `/api/sites/{site_id}/company-profile` | 更新企业档案 |

字段：

- `company_name`
- `legal_name`
- `industry`
- `description`
- `phone`
- `email`
- `address`
- `service_area`

联系方式会在前台官网底部页脚展示。

### 固定页面

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/pages` | 获取固定页面列表 |
| POST | `/api/sites/{site_id}/pages` | 创建固定页面 |
| PATCH | `/api/pages/{page_id}` | 更新固定页面 |
| DELETE | `/api/pages/{page_id}` | 删除固定页面 |

核心字段：

- `title`：后台和导航中的页面标题。
- `slug`：页面短链接，例如 `about`。
- `h1`：前台页面正文主标题。
- `body`：正文。
- `meta_title`
- `meta_description`
- `sort_order`：排序，数字越小越靠前。
- `show_in_nav`：是否显示在前台顶部导航。
- `status`：`draft`、`published`、`hidden`。

说明：

- `hidden` 不进入前台展示。
- `show_in_nav=false` 时，页面仍可预览和发布，但不会显示在顶部导航。

### 文章

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/articles` | 获取文章列表 |
| POST | `/api/sites/{site_id}/articles` | 创建文章 |
| PATCH | `/api/articles/{article_id}` | 更新文章 |
| DELETE | `/api/articles/{article_id}` | 删除文章 |

核心字段：

- `title`
- `slug`
- `category`
- `summary`
- `body`
- `cover_image`
- `status`

### 产品

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/products` | 获取产品列表 |
| POST | `/api/sites/{site_id}/products` | 创建产品 |
| PATCH | `/api/products/{product_id}` | 更新产品 |
| DELETE | `/api/products/{product_id}` | 删除产品 |

核心字段：

- `name`
- `slug`
- `category`
- `model`
- `summary`
- `description`
- `specifications`
- `cover_image`
- `price_note`
- `status`

### FAQ

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/faqs` | 获取 FAQ 列表 |
| POST | `/api/sites/{site_id}/faqs` | 创建 FAQ |
| PATCH | `/api/faqs/{faq_id}` | 更新 FAQ |
| DELETE | `/api/faqs/{faq_id}` | 删除 FAQ |

核心字段：

- `question`
- `answer`
- `category`
- `sort_order`
- `status`

### 案例

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/cases` | 获取案例列表 |
| POST | `/api/sites/{site_id}/cases` | 创建案例 |
| PATCH | `/api/cases/{case_id}` | 更新案例 |
| DELETE | `/api/cases/{case_id}` | 删除案例 |

核心字段：

- `title`
- `slug`
- `client_name`
- `industry`
- `summary`
- `challenge`
- `solution`
- `result`
- `cover_image`
- `project_date`
- `status`

### 服务

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/services` | 获取服务列表 |
| POST | `/api/sites/{site_id}/services` | 创建服务 |
| PATCH | `/api/services/{service_id}` | 更新服务 |
| DELETE | `/api/services/{service_id}` | 删除服务 |

核心字段：

- `name`
- `slug`
- `category`
- `summary`
- `scope`
- `process`
- `deliverables`
- `price_note`
- `status`

### 媒体素材

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/assets` | 获取素材列表 |
| POST | `/api/sites/{site_id}/assets` | 上传素材 |
| PATCH | `/api/assets/{asset_id}` | 更新素材说明 |
| DELETE | `/api/assets/{asset_id}` | 删除素材 |

上传素材示例：

```bash
curl -X POST http://127.0.0.1:8000/api/sites/{site_id}/assets \
  -F "file=@/path/to/logo.png" \
  -F "alt_text=企业 Logo"
```

返回字段：

- `filename`
- `url`
- `alt_text`
- `file_type`
- `size`
- `created_at`
- `updated_at`

### 预览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/preview` | 完整官网首页预览 |
| GET | `/api/sites/{site_id}/preview/pages/{slug}` | 固定页面预览 |
| GET | `/api/sites/{site_id}/preview/articles/{slug}` | 文章详情预览 |
| GET | `/api/sites/{site_id}/preview/products/{slug}` | 产品详情预览 |
| GET | `/api/sites/{site_id}/preview/cases/{slug}` | 案例详情预览 |
| GET | `/api/sites/{site_id}/preview/services/{slug}` | 服务详情预览 |
| GET | `/api/sites/{site_id}/preview/focus/{section}` | 模块聚焦预览 |
| GET | `/api/sites/{site_id}/preview/focus/{section}/{slug}` | 单条内容聚焦预览 |

聚焦预览当前用于后台内嵌预览。支持的 `section` 包括：

- `identity`
- `company`
- `pages`
- `articles`
- `products`
- `cases`
- `services`

### 发布

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/sites/{site_id}/publish-readiness` | 获取发布前检查 |
| POST | `/api/sites/{site_id}/publish` | 发布静态 HTML |
| GET | `/api/sites/{site_id}/publishes` | 获取发布历史 |

说明：

- 发布前检查只提示缺项，不阻止发布。
- 发布会输出首页、固定页面、文章详情、产品详情、案例详情和服务详情。
- 发布记录会保存 `version`、`publish_url`、`output_path`、`status` 和 `message`。

## 状态约定

站点状态：

- `draft`
- `active`
- `archived`

内容状态：

- `draft`：草稿，不作为正式内容展示。
- `published`：已发布，进入预览和发布结果。
- `hidden`：隐藏，从前台移除。

当前 MVP 中，预览层会过滤 `hidden` 内容。发布前检查不会作为强制门禁。

## 错误处理

当前已处理的主要错误：

- 站点或内容不存在：`404`
- 重复 `slug`：`409`
- FastAPI 字段校验失败：`422`

重复短链接会通过领域错误 `DuplicateSlugError` 转换为友好提示，避免把数据库原始错误暴露给前端。

## 后续功能接口规划

以下能力不属于当前 MVP，但可以按现有分层继续补。

### 用户、权限和操作审计

建议新增：

```text
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me

GET  /api/sites/{site_id}/members
POST /api/sites/{site_id}/members
PATCH /api/site-members/{member_id}
DELETE /api/site-members/{member_id}

GET  /api/sites/{site_id}/audit-logs
```

建议模型：

- `User`
- `Role`
- `SiteMember`
- `AuditLog`

注意：

- 第一阶段不要做复杂组织架构。
- 先支持站点级管理员和编辑员即可。
- 所有删除、发布、回滚动作应记录审计日志。

### 模板和主题配置

建议新增：

```text
GET   /api/templates
GET   /api/templates/{template_id}
GET   /api/sites/{site_id}/theme
PUT   /api/sites/{site_id}/theme
POST  /api/sites/{site_id}/theme/preview
```

建议字段：

- 主色
- 辅助色
- 字体方案
- 首页模块显示顺序
- 导航样式
- 页脚样式

注意：

- 不要一开始做复杂拖拽。
- 先做有限配置项，让模板保持稳定。
- 模板渲染仍放在基础设施层。

### 首页区块编排

建议新增：

```text
GET   /api/sites/{site_id}/home-sections
POST  /api/sites/{site_id}/home-sections
PATCH /api/home-sections/{section_id}
DELETE /api/home-sections/{section_id}
POST  /api/sites/{site_id}/home-sections/reorder
```

建议区块类型：

- `hero`
- `company_intro`
- `services`
- `products`
- `cases`
- `articles`
- `faq`
- `contact`

注意：

- 首页区块只做排序、显示隐藏和基础文案。
- 不要上来做任意组件拖拽。

### 导航树

建议新增：

```text
GET   /api/sites/{site_id}/navigation
PUT   /api/sites/{site_id}/navigation
POST  /api/sites/{site_id}/navigation/items
PATCH /api/navigation-items/{item_id}
DELETE /api/navigation-items/{item_id}
POST  /api/sites/{site_id}/navigation/reorder
```

建议支持：

- 顶部导航
- 页脚导航
- 一级导航
- 简单二级导航
- 外部链接

注意：

- 当前 `pages.show_in_nav` 是 MVP 简化方案。
- 后续导航树应独立建模，不要把所有导航逻辑继续塞进页面表。

### 内容检索、分页和批量操作

建议新增查询参数：

```text
GET /api/sites/{site_id}/articles?q=&status=&category=&page=&page_size=
GET /api/sites/{site_id}/products?q=&status=&category=&page=&page_size=
GET /api/sites/{site_id}/cases?q=&status=&industry=&page=&page_size=
GET /api/sites/{site_id}/services?q=&status=&category=&page=&page_size=
```

建议新增批量接口：

```text
POST /api/articles/bulk-status
POST /api/products/bulk-status
POST /api/cases/bulk-status
POST /api/services/bulk-status
POST /api/faqs/bulk-status
```

注意：

- 先统一分页响应格式。
- 再做前端列表筛选。

### 媒体增强

建议新增：

```text
GET   /api/sites/{site_id}/asset-folders
POST  /api/sites/{site_id}/asset-folders
PATCH /api/asset-folders/{folder_id}
DELETE /api/asset-folders/{folder_id}

GET   /api/assets/{asset_id}/usages
POST  /api/assets/{asset_id}/replace
POST  /api/assets/{asset_id}/variants
```

可补能力：

- 素材分类
- 图片裁剪
- 图片压缩
- WebP 转换
- 素材引用关系
- 删除前风险提示

### 发布增强

建议新增：

```text
GET  /api/sites/{site_id}/publishes/{publish_id}
POST /api/sites/{site_id}/publishes/{publish_id}/rollback
GET  /api/sites/{site_id}/publishes/{publish_id}/diff
POST /api/sites/{site_id}/sitemap
POST /api/sites/{site_id}/robots
```

可补能力：

- 发布回滚
- 发布差异对比
- sitemap 输出
- robots 输出
- 发布前完整链接检查
- 发布任务异步化

### 可选 AWA 诊断

建议作为插件式能力接入：

```text
POST /api/sites/{site_id}/diagnostics/awa/run
GET  /api/sites/{site_id}/diagnostics/awa/latest
GET  /api/sites/{site_id}/diagnostics/awa/runs
GET  /api/diagnostics/awa/runs/{run_id}
```

原则：

- 不阻塞建站。
- 不阻塞保存。
- 不强制阻塞发布。
- 诊断结果只作为优化建议。
- 诊断模块不要反向依赖内容编辑模块。

建议模型：

- `DiagnosticRun`
- `DiagnosticIssue`
- `DiagnosticSuggestion`

### LLM 文案助手

建议新增：

```text
POST /api/sites/{site_id}/assist/copy/rewrite
POST /api/sites/{site_id}/assist/copy/summarize
POST /api/sites/{site_id}/assist/seo/title
POST /api/sites/{site_id}/assist/seo/description
```

原则：

- 只做辅助生成和润色。
- 用户必须确认后才写入正式内容。
- 不允许自动覆盖用户已有内容。

## 开发注意事项

- 新功能优先挂在现有主线：站点 -> 档案 -> 内容 -> 素材 -> 预览 -> 发布。
- 不要绕过应用层直接在 API 里操作数据库。
- 不要在 React 页面组件里写最终前台模板逻辑。
- 不要把素材 URL 填写作为普通用户主流程，优先做选择和上传。
- 不要把发布前检查做成强制阻断，除非后续明确有审核工作流。
- 不要让 AWA、LLM 或外部服务成为 MVP 主流程依赖。

## 文档索引

详细设计和阶段记录见：

- `企业官网后台管理系统技术设计报告.md`
- `docs/README.md`
- `docs/01_开发原则与代码规范.md`
- `docs/02_系统分层与模块边界.md`
- `docs/03_数据模型与接口契约.md`
- `docs/04_实施阶段与验收标准.md`
- `docs/05_实施总纲与开发顺序.md`
- `docs/06_开发进度记录.md`
- `docs/07_MVP验收清单.md`
