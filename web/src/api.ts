export type Site = {
  id: string;
  tenant_id: string;
  name: string;
  template_id: string;
  domain: string | null;
  status: "draft" | "active" | "archived";
  created_at: string;
  updated_at: string;
};

export type SitePayload = {
  tenant_id: string;
  name: string;
  template_id: string;
  domain?: string | null;
};

export type SiteProfile = {
  site_id: string;
  site_name: string;
  subtitle: string;
  logo: string;
  favicon: string;
  default_title: string;
  default_description: string;
  created_at: string;
  updated_at: string;
};

export type CompanyProfile = {
  site_id: string;
  company_name: string;
  legal_name: string;
  industry: string;
  description: string;
  phone: string;
  email: string;
  address: string;
  service_area: string;
  created_at: string;
  updated_at: string;
};

export type PageStatus = "draft" | "published" | "hidden";

export type ContentPage = {
  id: string;
  site_id: string;
  title: string;
  slug: string;
  h1: string;
  body: string;
  meta_title: string;
  meta_description: string;
  sort_order: number;
  show_in_nav: boolean;
  status: PageStatus;
  created_at: string;
  updated_at: string;
};

export type PagePayload = {
  title: string;
  slug: string;
  h1?: string | null;
  body?: string | null;
  meta_title?: string | null;
  meta_description?: string | null;
  sort_order?: number;
};

export type ArticleStatus = "draft" | "published" | "hidden";

export type Article = {
  id: string;
  site_id: string;
  title: string;
  slug: string;
  category: string;
  summary: string;
  body: string;
  cover_image: string;
  status: ArticleStatus;
  created_at: string;
  updated_at: string;
};

export type ArticlePayload = {
  title: string;
  slug: string;
  category?: string | null;
  summary?: string | null;
  body?: string | null;
  cover_image?: string | null;
};

export type ProductStatus = "draft" | "published" | "hidden";

export type Product = {
  id: string;
  site_id: string;
  name: string;
  slug: string;
  category: string;
  model: string;
  summary: string;
  description: string;
  specifications: string;
  cover_image: string;
  price_note: string;
  status: ProductStatus;
  created_at: string;
  updated_at: string;
};

export type ProductPayload = {
  name: string;
  slug: string;
  category?: string | null;
  model?: string | null;
  summary?: string | null;
  description?: string | null;
  specifications?: string | null;
  cover_image?: string | null;
  price_note?: string | null;
};

export type FAQStatus = "draft" | "published" | "hidden";

export type FAQItem = {
  id: string;
  site_id: string;
  question: string;
  answer: string;
  category: string;
  sort_order: number;
  status: FAQStatus;
  created_at: string;
  updated_at: string;
};

export type FAQPayload = {
  question: string;
  answer?: string | null;
  category?: string | null;
  sort_order?: number;
};

export type CaseStatus = "draft" | "published" | "hidden";

export type CaseStudy = {
  id: string;
  site_id: string;
  title: string;
  slug: string;
  client_name: string;
  industry: string;
  summary: string;
  challenge: string;
  solution: string;
  result: string;
  cover_image: string;
  project_date: string;
  status: CaseStatus;
  created_at: string;
  updated_at: string;
};

export type CasePayload = {
  title: string;
  slug: string;
  client_name?: string | null;
  industry?: string | null;
  summary?: string | null;
  challenge?: string | null;
  solution?: string | null;
  result?: string | null;
  cover_image?: string | null;
  project_date?: string | null;
};

export type ServiceStatus = "draft" | "published" | "hidden";

export type ServiceItem = {
  id: string;
  site_id: string;
  name: string;
  slug: string;
  category: string;
  summary: string;
  scope: string;
  process: string;
  deliverables: string;
  price_note: string;
  status: ServiceStatus;
  created_at: string;
  updated_at: string;
};

export type ServicePayload = {
  name: string;
  slug: string;
  category?: string | null;
  summary?: string | null;
  scope?: string | null;
  process?: string | null;
  deliverables?: string | null;
  price_note?: string | null;
};

export type PublishRecord = {
  id: string;
  site_id: string;
  version: string;
  status: "success" | "failed";
  preview_url: string;
  publish_url: string;
  output_path: string;
  message: string;
  created_at: string;
};

export type ReadinessIssue = {
  level: "error" | "warning" | "info";
  module: string;
  message: string;
};

export type PublishReadiness = {
  site_id: string;
  can_publish: boolean;
  issue_count: number;
  issues: ReadinessIssue[];
};

export type MediaAsset = {
  id: string;
  site_id: string;
  filename: string;
  url: string;
  alt_text: string;
  file_type: string;
  size: number;
  created_at: string;
  updated_at: string;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {})
    },
    ...options
  });
  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return response.json() as Promise<T>;
}

export function listSites(): Promise<Site[]> {
  return request<Site[]>("/api/sites");
}

export function createSite(payload: SitePayload): Promise<Site> {
  return request<Site>("/api/sites", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

async function uploadRequest<T>(path: string, formData: FormData): Promise<T> {
  const response = await fetch(path, {
    method: "POST",
    body: formData
  });
  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return response.json() as Promise<T>;
}

async function requestNoContent(path: string, options?: RequestInit): Promise<void> {
  const response = await fetch(path, options);
  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
}

async function readErrorMessage(response: Response): Promise<string> {
  const text = await response.text();
  if (!text) {
    return `Request failed: ${response.status}`;
  }
  try {
    const body = JSON.parse(text) as { detail?: unknown };
    if (Array.isArray(body.detail)) {
      return body.detail
        .map((item) => {
          if (!item || typeof item !== "object") return "请求参数错误";
          const detail = item as { loc?: unknown[]; msg?: string };
          const field = Array.isArray(detail.loc) ? detail.loc.slice(1).join(".") : "";
          return field ? `${field}: ${detail.msg ?? "请求参数错误"}` : detail.msg ?? "请求参数错误";
        })
        .join("；");
    }
    if (typeof body.detail === "string") {
      return body.detail;
    }
  } catch {
    return text;
  }
  return text;
}

export function updateSite(siteId: string, payload: Partial<SitePayload>): Promise<Site> {
  return request<Site>(`/api/sites/${siteId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function getSiteProfile(siteId: string): Promise<SiteProfile> {
  return request<SiteProfile>(`/api/sites/${siteId}/profile`);
}

export function saveSiteProfile(siteId: string, payload: Partial<SiteProfile>): Promise<SiteProfile> {
  return request<SiteProfile>(`/api/sites/${siteId}/profile`, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export function getCompanyProfile(siteId: string): Promise<CompanyProfile> {
  return request<CompanyProfile>(`/api/sites/${siteId}/company-profile`);
}

export function saveCompanyProfile(siteId: string, payload: Partial<CompanyProfile>): Promise<CompanyProfile> {
  return request<CompanyProfile>(`/api/sites/${siteId}/company-profile`, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export function listPages(siteId: string): Promise<ContentPage[]> {
  return request<ContentPage[]>(`/api/sites/${siteId}/pages`);
}

export function createPage(siteId: string, payload: PagePayload): Promise<ContentPage> {
  return request<ContentPage>(`/api/sites/${siteId}/pages`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updatePage(pageId: string, payload: Partial<ContentPage>): Promise<ContentPage> {
  return request<ContentPage>(`/api/pages/${pageId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function deletePage(pageId: string): Promise<void> {
  return requestNoContent(`/api/pages/${pageId}`, { method: "DELETE" });
}

export function listArticles(siteId: string): Promise<Article[]> {
  return request<Article[]>(`/api/sites/${siteId}/articles`);
}

export function createArticle(siteId: string, payload: ArticlePayload): Promise<Article> {
  return request<Article>(`/api/sites/${siteId}/articles`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateArticle(articleId: string, payload: Partial<Article>): Promise<Article> {
  return request<Article>(`/api/articles/${articleId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function deleteArticle(articleId: string): Promise<void> {
  return requestNoContent(`/api/articles/${articleId}`, { method: "DELETE" });
}

export function listProducts(siteId: string): Promise<Product[]> {
  return request<Product[]>(`/api/sites/${siteId}/products`);
}

export function createProduct(siteId: string, payload: ProductPayload): Promise<Product> {
  return request<Product>(`/api/sites/${siteId}/products`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateProduct(productId: string, payload: Partial<Product>): Promise<Product> {
  return request<Product>(`/api/products/${productId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function deleteProduct(productId: string): Promise<void> {
  return requestNoContent(`/api/products/${productId}`, { method: "DELETE" });
}

export function listFaqs(siteId: string): Promise<FAQItem[]> {
  return request<FAQItem[]>(`/api/sites/${siteId}/faqs`);
}

export function createFaq(siteId: string, payload: FAQPayload): Promise<FAQItem> {
  return request<FAQItem>(`/api/sites/${siteId}/faqs`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateFaq(faqId: string, payload: Partial<FAQItem>): Promise<FAQItem> {
  return request<FAQItem>(`/api/faqs/${faqId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function deleteFaq(faqId: string): Promise<void> {
  return requestNoContent(`/api/faqs/${faqId}`, { method: "DELETE" });
}

export function listCases(siteId: string): Promise<CaseStudy[]> {
  return request<CaseStudy[]>(`/api/sites/${siteId}/cases`);
}

export function createCase(siteId: string, payload: CasePayload): Promise<CaseStudy> {
  return request<CaseStudy>(`/api/sites/${siteId}/cases`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateCase(caseId: string, payload: Partial<CaseStudy>): Promise<CaseStudy> {
  return request<CaseStudy>(`/api/cases/${caseId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function deleteCase(caseId: string): Promise<void> {
  return requestNoContent(`/api/cases/${caseId}`, { method: "DELETE" });
}

export function listServices(siteId: string): Promise<ServiceItem[]> {
  return request<ServiceItem[]>(`/api/sites/${siteId}/services`);
}

export function createService(siteId: string, payload: ServicePayload): Promise<ServiceItem> {
  return request<ServiceItem>(`/api/sites/${siteId}/services`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateService(serviceId: string, payload: Partial<ServiceItem>): Promise<ServiceItem> {
  return request<ServiceItem>(`/api/services/${serviceId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function deleteService(serviceId: string): Promise<void> {
  return requestNoContent(`/api/services/${serviceId}`, { method: "DELETE" });
}

export function publishSite(siteId: string): Promise<PublishRecord> {
  return request<PublishRecord>(`/api/sites/${siteId}/publish`, {
    method: "POST"
  });
}

export function getPublishReadiness(siteId: string): Promise<PublishReadiness> {
  return request<PublishReadiness>(`/api/sites/${siteId}/publish-readiness`);
}

export function listPublishes(siteId: string): Promise<PublishRecord[]> {
  return request<PublishRecord[]>(`/api/sites/${siteId}/publishes`);
}

export function listAssets(siteId: string): Promise<MediaAsset[]> {
  return request<MediaAsset[]>(`/api/sites/${siteId}/assets`);
}

export function uploadAsset(siteId: string, file: File, altText: string): Promise<MediaAsset> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("alt_text", altText);
  return uploadRequest<MediaAsset>(`/api/sites/${siteId}/assets`, formData);
}

export function updateAsset(assetId: string, payload: Pick<MediaAsset, "alt_text">): Promise<MediaAsset> {
  return request<MediaAsset>(`/api/assets/${assetId}`, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}

export function deleteAsset(assetId: string): Promise<void> {
  return requestNoContent(`/api/assets/${assetId}`, { method: "DELETE" });
}
