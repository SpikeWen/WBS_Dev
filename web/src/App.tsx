import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  BookOpen,
  BriefcaseBusiness,
  Building2,
  CircleHelp,
  Eye,
  FileText,
  Images,
  LayoutDashboard,
  Newspaper,
  Package,
  Plus,
  RefreshCw,
  Rocket,
  Settings
} from "lucide-react";
import {
  Article,
  ArticlePayload,
  CasePayload,
  CaseStudy,
  CompanyProfile,
  ContentPage,
  FAQItem,
  FAQPayload,
  MediaAsset,
  PagePayload,
  Product,
  ProductPayload,
  PublishReadiness,
  PublishRecord,
  ServiceItem,
  ServicePayload,
  Site,
  SitePayload,
  SiteProfile,
  createArticle,
  createService,
  createCase,
  createFaq,
  createProduct,
  createSite,
  createPage,
  deleteArticle,
  deleteAsset,
  deleteCase,
  deleteFaq,
  deletePage,
  deleteProduct,
  deleteService,
  getCompanyProfile,
  getPublishReadiness,
  getSiteProfile,
  listArticles,
  listAssets,
  listCases,
  listFaqs,
  listPages,
  listProducts,
  listPublishes,
  listServices,
  listSites,
  publishSite,
  saveCompanyProfile,
  saveSiteProfile,
  updateAsset,
  updatePage,
  updateArticle,
  updateCase,
  updateFaq,
  updateProduct,
  updateService,
  uploadAsset,
  updateSite
} from "./api";
import { ArticlePanel } from "./components/ArticlePanel";
import { CasePanel } from "./components/CasePanel";
import { CompanyProfilePanel } from "./components/CompanyProfilePanel";
import { Field } from "./components/Field";
import { FaqPanel } from "./components/FaqPanel";
import { MediaPanel } from "./components/MediaPanel";
import { PagePanel } from "./components/PagePanel";
import { PreviewPanel } from "./components/PreviewPanel";
import { ProductPanel } from "./components/ProductPanel";
import { PublishPanel } from "./components/PublishPanel";
import { ServicePanel } from "./components/ServicePanel";
import { SiteDashboardPanel } from "./components/SiteDashboardPanel";
import { SiteIdentityPanel } from "./components/SiteIdentityPanel";

const emptySiteForm: SitePayload = {
  tenant_id: "default",
  name: "",
  template_id: "template_basic",
  domain: ""
};

const emptySiteProfile: SiteProfile = {
  site_id: "",
  site_name: "",
  subtitle: "",
  logo: "",
  favicon: "",
  default_title: "",
  default_description: "",
  created_at: "",
  updated_at: ""
};

const emptyCompanyProfile: CompanyProfile = {
  site_id: "",
  company_name: "",
  legal_name: "",
  industry: "",
  description: "",
  phone: "",
  email: "",
  address: "",
  service_area: "",
  created_at: "",
  updated_at: ""
};

const emptyPageForm: PagePayload = {
  title: "",
  slug: "",
  h1: "",
  body: "",
  meta_title: "",
  meta_description: "",
  sort_order: 0
};

const emptyArticleForm: ArticlePayload = {
  title: "",
  slug: "",
  category: "",
  summary: "",
  body: "",
  cover_image: ""
};

const emptyProductForm: ProductPayload = {
  name: "",
  slug: "",
  category: "",
  model: "",
  summary: "",
  description: "",
  specifications: "",
  cover_image: "",
  price_note: ""
};

const emptyFaqForm: FAQPayload = {
  question: "",
  answer: "",
  category: "",
  sort_order: 0
};

const emptyCaseForm: CasePayload = {
  title: "",
  slug: "",
  client_name: "",
  industry: "",
  summary: "",
  challenge: "",
  solution: "",
  result: "",
  cover_image: "",
  project_date: ""
};

const emptyServiceForm: ServicePayload = {
  name: "",
  slug: "",
  category: "",
  summary: "",
  scope: "",
  process: "",
  deliverables: "",
  price_note: ""
};

type WorkspaceSection =
  | "dashboard"
  | "identity"
  | "company"
  | "pages"
  | "articles"
  | "products"
  | "cases"
  | "services"
  | "faqs"
  | "media"
  | "publish"
  | "preview";

type PreviewTarget = {
  title: string;
  description: string;
  path: string;
};

const workspaceSections: {
  id: WorkspaceSection;
  label: string;
  icon: typeof LayoutDashboard;
}[] = [
  { id: "dashboard", label: "驾驶舱", icon: LayoutDashboard },
  { id: "identity", label: "站点身份", icon: Settings },
  { id: "company", label: "企业档案", icon: Building2 },
  { id: "pages", label: "页面", icon: FileText },
  { id: "articles", label: "文章", icon: Newspaper },
  { id: "products", label: "产品", icon: Package },
  { id: "cases", label: "案例", icon: BriefcaseBusiness },
  { id: "services", label: "服务", icon: BookOpen },
  { id: "faqs", label: "FAQ", icon: CircleHelp },
  { id: "media", label: "媒体", icon: Images },
  { id: "publish", label: "发布", icon: Rocket },
  { id: "preview", label: "总体预览", icon: Eye }
];

export function App() {
  const [sites, setSites] = useState<Site[]>([]);
  const [selectedSiteId, setSelectedSiteId] = useState<string>("");
  const [newSite, setNewSite] = useState<SitePayload>(emptySiteForm);
  const [siteDraft, setSiteDraft] = useState<Site | null>(null);
  const [siteProfile, setSiteProfile] = useState<SiteProfile>(emptySiteProfile);
  const [companyProfile, setCompanyProfile] = useState<CompanyProfile>(emptyCompanyProfile);
  const [pages, setPages] = useState<ContentPage[]>([]);
  const [selectedPageId, setSelectedPageId] = useState<string>("");
  const [pageDraft, setPageDraft] = useState<ContentPage | null>(null);
  const [newPage, setNewPage] = useState<PagePayload>(emptyPageForm);
  const [articles, setArticles] = useState<Article[]>([]);
  const [selectedArticleId, setSelectedArticleId] = useState<string>("");
  const [articleDraft, setArticleDraft] = useState<Article | null>(null);
  const [newArticle, setNewArticle] = useState<ArticlePayload>(emptyArticleForm);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<string>("");
  const [productDraft, setProductDraft] = useState<Product | null>(null);
  const [newProduct, setNewProduct] = useState<ProductPayload>(emptyProductForm);
  const [faqs, setFaqs] = useState<FAQItem[]>([]);
  const [selectedFaqId, setSelectedFaqId] = useState<string>("");
  const [faqDraft, setFaqDraft] = useState<FAQItem | null>(null);
  const [newFaq, setNewFaq] = useState<FAQPayload>(emptyFaqForm);
  const [cases, setCases] = useState<CaseStudy[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>("");
  const [caseDraft, setCaseDraft] = useState<CaseStudy | null>(null);
  const [newCase, setNewCase] = useState<CasePayload>(emptyCaseForm);
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [selectedServiceId, setSelectedServiceId] = useState<string>("");
  const [serviceDraft, setServiceDraft] = useState<ServiceItem | null>(null);
  const [newService, setNewService] = useState<ServicePayload>(emptyServiceForm);
  const [assets, setAssets] = useState<MediaAsset[]>([]);
  const [selectedAssetId, setSelectedAssetId] = useState<string>("");
  const [assetDraft, setAssetDraft] = useState<MediaAsset | null>(null);
  const [assetFile, setAssetFile] = useState<File | null>(null);
  const [assetAltText, setAssetAltText] = useState("");
  const [publishes, setPublishes] = useState<PublishRecord[]>([]);
  const [publishReadiness, setPublishReadiness] = useState<PublishReadiness | null>(null);
  const [activeSection, setActiveSection] = useState<WorkspaceSection>("dashboard");
  const [previewTarget, setPreviewTarget] = useState<PreviewTarget | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [previewVersion, setPreviewVersion] = useState(0);

  const selectedSite = useMemo(
    () => sites.find((site) => site.id === selectedSiteId) ?? null,
    [selectedSiteId, sites]
  );

  useEffect(() => {
    void refreshSites();
  }, []);

  useEffect(() => {
    if (!selectedSiteId) {
      setSiteDraft(null);
      setSiteProfile(emptySiteProfile);
      setCompanyProfile(emptyCompanyProfile);
      setPages([]);
      setSelectedPageId("");
      setPageDraft(null);
      setArticles([]);
      setSelectedArticleId("");
      setArticleDraft(null);
      setProducts([]);
      setSelectedProductId("");
      setProductDraft(null);
      setFaqs([]);
      setSelectedFaqId("");
      setFaqDraft(null);
      setCases([]);
      setSelectedCaseId("");
      setCaseDraft(null);
      setServices([]);
      setSelectedServiceId("");
      setServiceDraft(null);
      setAssets([]);
      setSelectedAssetId("");
      setAssetDraft(null);
      setPublishes([]);
      setPublishReadiness(null);
      setPreviewTarget(null);
      return;
    }
    void loadSelectedSite(selectedSiteId);
  }, [selectedSiteId]);

  async function refreshSites() {
    setLoading(true);
    try {
      const items = await listSites();
      setSites(items);
      if (!selectedSiteId && items.length > 0) {
        setSelectedSiteId(items[0].id);
      }
      setMessage("站点列表已刷新");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "加载站点失败");
    } finally {
      setLoading(false);
    }
  }

  async function loadSelectedSite(siteId: string) {
    setLoading(true);
    try {
      const [
        profile,
        company,
        sitePages,
        siteArticles,
        siteProducts,
        siteFaqs,
        siteCases,
        siteServices,
        siteAssets,
        sitePublishes,
        siteReadiness
      ] = await Promise.all([
        getSiteProfile(siteId),
        getCompanyProfile(siteId),
        listPages(siteId),
        listArticles(siteId),
        listProducts(siteId),
        listFaqs(siteId),
        listCases(siteId),
        listServices(siteId),
        listAssets(siteId),
        listPublishes(siteId),
        getPublishReadiness(siteId)
      ]);
      const current = sites.find((site) => site.id === siteId) ?? null;
      setSiteDraft(current);
      setSiteProfile(profile);
      setCompanyProfile(company);
      setPages(sitePages);
      setArticles(siteArticles);
      setProducts(siteProducts);
      setFaqs(siteFaqs);
      setCases(siteCases);
      setServices(siteServices);
      setAssets(siteAssets);
      setPublishes(sitePublishes);
      setPublishReadiness(siteReadiness);
      if (sitePages.length > 0) {
        const nextSelected = sitePages.find((page) => page.id === selectedPageId) ?? sitePages[0];
        setSelectedPageId(nextSelected.id);
        setPageDraft(nextSelected);
      } else {
        setSelectedPageId("");
        setPageDraft(null);
      }
      if (siteArticles.length > 0) {
        const nextArticle =
          siteArticles.find((article) => article.id === selectedArticleId) ?? siteArticles[0];
        setSelectedArticleId(nextArticle.id);
        setArticleDraft(nextArticle);
      } else {
        setSelectedArticleId("");
        setArticleDraft(null);
      }
      if (siteProducts.length > 0) {
        const nextProduct =
          siteProducts.find((product) => product.id === selectedProductId) ?? siteProducts[0];
        setSelectedProductId(nextProduct.id);
        setProductDraft(nextProduct);
      } else {
        setSelectedProductId("");
        setProductDraft(null);
      }
      if (siteFaqs.length > 0) {
        const nextFaq = siteFaqs.find((faq) => faq.id === selectedFaqId) ?? siteFaqs[0];
        setSelectedFaqId(nextFaq.id);
        setFaqDraft(nextFaq);
      } else {
        setSelectedFaqId("");
        setFaqDraft(null);
      }
      if (siteCases.length > 0) {
        const nextCase = siteCases.find((item) => item.id === selectedCaseId) ?? siteCases[0];
        setSelectedCaseId(nextCase.id);
        setCaseDraft(nextCase);
      } else {
        setSelectedCaseId("");
        setCaseDraft(null);
      }
      if (siteServices.length > 0) {
        const nextService = siteServices.find((item) => item.id === selectedServiceId) ?? siteServices[0];
        setSelectedServiceId(nextService.id);
        setServiceDraft(nextService);
      } else {
        setSelectedServiceId("");
        setServiceDraft(null);
      }
      if (siteAssets.length > 0) {
        const nextAsset = siteAssets.find((item) => item.id === selectedAssetId) ?? siteAssets[0];
        setSelectedAssetId(nextAsset.id);
        setAssetDraft(nextAsset);
      } else {
        setSelectedAssetId("");
        setAssetDraft(null);
      }
      setPreviewVersion((value) => value + 1);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "加载站点详情失败");
    } finally {
      setLoading(false);
    }
  }

  async function refreshSiteDerivedState(siteId: string) {
    setPreviewVersion((value) => value + 1);
    try {
      setPublishReadiness(await getPublishReadiness(siteId));
    } catch {
      // 保存主流程已成功，发布检查刷新失败时不覆盖成功提示。
    }
  }

  async function handleCreateSite(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!newSite.name.trim()) {
      setMessage("站点名称不能为空");
      return;
    }
    setLoading(true);
    try {
      const created = await createSite({
        ...newSite,
        tenant_id: newSite.tenant_id.trim(),
        name: newSite.name.trim(),
        template_id: newSite.template_id.trim(),
        domain: newSite.domain?.trim() || null
      });
      setSites((items) => [created, ...items]);
      setSelectedSiteId(created.id);
      setActiveSection("dashboard");
      setNewSite(emptySiteForm);
      setMessage("站点已创建");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "创建站点失败");
    } finally {
      setLoading(false);
    }
  }

  async function saveSiteIdentity() {
    if (!siteDraft) return;
    if (!siteDraft.name.trim() || !siteDraft.template_id.trim()) {
      setMessage("站点名称和模板 ID 不能为空");
      return;
    }
    setLoading(true);
    try {
      const updated = await updateSite(siteDraft.id, {
        name: siteDraft.name.trim(),
        template_id: siteDraft.template_id.trim(),
        domain: siteDraft.domain?.trim() || null
      });
      const profile = await saveSiteProfile(siteDraft.id, siteProfile);
      setSites((items) => items.map((item) => (item.id === updated.id ? updated : item)));
      setSiteDraft(updated);
      setSiteProfile(profile);
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("站点身份已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存站点身份失败");
    } finally {
      setLoading(false);
    }
  }

  async function saveCompany() {
    if (!siteDraft) return;
    setLoading(true);
    try {
      const profile = await saveCompanyProfile(siteDraft.id, companyProfile);
      setCompanyProfile(profile);
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("企业档案已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存企业档案失败");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreatePage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!siteDraft) return;
    if (!newPage.title.trim() || !newPage.slug.trim()) {
      setMessage("页面标题和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const created = await createPage(siteDraft.id, {
        ...newPage,
        title: newPage.title.trim(),
        slug: newPage.slug.trim(),
        h1: newPage.h1 || newPage.title.trim(),
        meta_title: newPage.meta_title || newPage.title.trim(),
        sort_order: Number(newPage.sort_order ?? 0)
      });
      setPages((items) => [...items, created].sort(sortPages));
      setSelectedPageId(created.id);
      setPageDraft(created);
      setNewPage({ ...emptyPageForm, sort_order: pages.length + 1 });
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("固定页面已创建");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "创建页面失败");
    } finally {
      setLoading(false);
    }
  }

  function selectPage(page: ContentPage) {
    setSelectedPageId(page.id);
    setPageDraft(page);
  }

  async function savePage() {
    if (!pageDraft) return;
    if (!pageDraft.title.trim() || !pageDraft.slug.trim()) {
      setMessage("页面标题和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const updated = await updatePage(pageDraft.id, {
        title: pageDraft.title.trim(),
        slug: pageDraft.slug.trim(),
        h1: pageDraft.h1,
        body: pageDraft.body,
        meta_title: pageDraft.meta_title,
        meta_description: pageDraft.meta_description,
        sort_order: Number(pageDraft.sort_order),
        show_in_nav: pageDraft.show_in_nav,
        status: pageDraft.status
      });
      setPages((items) => items.map((item) => (item.id === updated.id ? updated : item)).sort(sortPages));
      setPageDraft(updated);
      await refreshSiteDerivedState(pageDraft.site_id);
      setMessage("页面内容已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存页面失败");
    } finally {
      setLoading(false);
    }
  }

  async function removePage() {
    if (!siteDraft || !pageDraft || !window.confirm(`删除页面「${pageDraft.title}」？`)) return;
    setLoading(true);
    try {
      await deletePage(pageDraft.id);
      await loadSelectedSite(siteDraft.id);
      setMessage("页面已删除");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "删除页面失败");
      setLoading(false);
    }
  }

  async function handleCreateArticle(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!siteDraft) return;
    if (!newArticle.title.trim() || !newArticle.slug.trim()) {
      setMessage("文章标题和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const created = await createArticle(siteDraft.id, {
        ...newArticle,
        title: newArticle.title.trim(),
        slug: newArticle.slug.trim(),
        category: newArticle.category || "新闻",
        summary: newArticle.summary || "",
        body: newArticle.body || ""
      });
      setArticles((items) => [created, ...items]);
      setSelectedArticleId(created.id);
      setArticleDraft(created);
      setNewArticle(emptyArticleForm);
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("文章已创建");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "创建文章失败");
    } finally {
      setLoading(false);
    }
  }

  function selectArticle(article: Article) {
    setSelectedArticleId(article.id);
    setArticleDraft(article);
  }

  async function saveArticle() {
    if (!articleDraft) return;
    if (!articleDraft.title.trim() || !articleDraft.slug.trim()) {
      setMessage("文章标题和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const updated = await updateArticle(articleDraft.id, {
        title: articleDraft.title.trim(),
        slug: articleDraft.slug.trim(),
        category: articleDraft.category,
        summary: articleDraft.summary,
        body: articleDraft.body,
        cover_image: articleDraft.cover_image,
        status: articleDraft.status
      });
      setArticles((items) => items.map((item) => (item.id === updated.id ? updated : item)));
      setArticleDraft(updated);
      await refreshSiteDerivedState(articleDraft.site_id);
      setMessage("文章已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存文章失败");
    } finally {
      setLoading(false);
    }
  }

  async function removeArticle() {
    if (!siteDraft || !articleDraft || !window.confirm(`删除文章「${articleDraft.title}」？`)) return;
    setLoading(true);
    try {
      await deleteArticle(articleDraft.id);
      await loadSelectedSite(siteDraft.id);
      setMessage("文章已删除");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "删除文章失败");
      setLoading(false);
    }
  }

  async function handleCreateProduct(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!siteDraft) return;
    if (!newProduct.name.trim() || !newProduct.slug.trim()) {
      setMessage("产品名称和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const created = await createProduct(siteDraft.id, {
        ...newProduct,
        name: newProduct.name.trim(),
        slug: newProduct.slug.trim(),
        category: newProduct.category || "产品",
        model: newProduct.model || "",
        summary: newProduct.summary || "",
        description: newProduct.description || "",
        specifications: newProduct.specifications || "",
        price_note: newProduct.price_note || ""
      });
      setProducts((items) => [created, ...items]);
      setSelectedProductId(created.id);
      setProductDraft(created);
      setNewProduct(emptyProductForm);
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("产品已创建");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "创建产品失败");
    } finally {
      setLoading(false);
    }
  }

  function selectProduct(product: Product) {
    setSelectedProductId(product.id);
    setProductDraft(product);
  }

  async function saveProduct() {
    if (!productDraft) return;
    if (!productDraft.name.trim() || !productDraft.slug.trim()) {
      setMessage("产品名称和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const updated = await updateProduct(productDraft.id, {
        name: productDraft.name.trim(),
        slug: productDraft.slug.trim(),
        category: productDraft.category,
        model: productDraft.model,
        summary: productDraft.summary,
        description: productDraft.description,
        specifications: productDraft.specifications,
        cover_image: productDraft.cover_image,
        price_note: productDraft.price_note,
        status: productDraft.status
      });
      setProducts((items) => items.map((item) => (item.id === updated.id ? updated : item)));
      setProductDraft(updated);
      await refreshSiteDerivedState(productDraft.site_id);
      setMessage("产品已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存产品失败");
    } finally {
      setLoading(false);
    }
  }

  async function removeProduct() {
    if (!siteDraft || !productDraft || !window.confirm(`删除产品「${productDraft.name}」？`)) return;
    setLoading(true);
    try {
      await deleteProduct(productDraft.id);
      await loadSelectedSite(siteDraft.id);
      setMessage("产品已删除");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "删除产品失败");
      setLoading(false);
    }
  }

  async function handleCreateFaq(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!siteDraft) return;
    if (!newFaq.question.trim()) {
      setMessage("FAQ 问题不能为空");
      return;
    }
    setLoading(true);
    try {
      const created = await createFaq(siteDraft.id, {
        ...newFaq,
        question: newFaq.question.trim(),
        answer: newFaq.answer || "",
        category: newFaq.category || "常见问题",
        sort_order: Number(newFaq.sort_order ?? faqs.length)
      });
      setFaqs((items) => [...items, created].sort(sortFaqs));
      setSelectedFaqId(created.id);
      setFaqDraft(created);
      setNewFaq({ ...emptyFaqForm, sort_order: faqs.length + 1 });
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("FAQ 已创建");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "创建 FAQ 失败");
    } finally {
      setLoading(false);
    }
  }

  function selectFaq(faq: FAQItem) {
    setSelectedFaqId(faq.id);
    setFaqDraft(faq);
  }

  async function saveFaq() {
    if (!faqDraft) return;
    if (!faqDraft.question.trim()) {
      setMessage("FAQ 问题不能为空");
      return;
    }
    setLoading(true);
    try {
      const updated = await updateFaq(faqDraft.id, {
        question: faqDraft.question.trim(),
        answer: faqDraft.answer,
        category: faqDraft.category,
        sort_order: Number(faqDraft.sort_order),
        status: faqDraft.status
      });
      setFaqs((items) => items.map((item) => (item.id === updated.id ? updated : item)).sort(sortFaqs));
      setFaqDraft(updated);
      await refreshSiteDerivedState(faqDraft.site_id);
      setMessage("FAQ 已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存 FAQ 失败");
    } finally {
      setLoading(false);
    }
  }

  async function removeFaq() {
    if (!siteDraft || !faqDraft || !window.confirm(`删除 FAQ「${faqDraft.question}」？`)) return;
    setLoading(true);
    try {
      await deleteFaq(faqDraft.id);
      await loadSelectedSite(siteDraft.id);
      setMessage("FAQ 已删除");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "删除 FAQ 失败");
      setLoading(false);
    }
  }

  async function handleCreateCase(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!siteDraft) return;
    if (!newCase.title.trim() || !newCase.slug.trim()) {
      setMessage("案例标题和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const created = await createCase(siteDraft.id, {
        ...newCase,
        title: newCase.title.trim(),
        slug: newCase.slug.trim(),
        client_name: newCase.client_name || "",
        industry: newCase.industry || "",
        summary: newCase.summary || "",
        challenge: newCase.challenge || "",
        solution: newCase.solution || "",
        result: newCase.result || "",
        cover_image: newCase.cover_image || "",
        project_date: newCase.project_date || ""
      });
      setCases((items) => [created, ...items]);
      setSelectedCaseId(created.id);
      setCaseDraft(created);
      setNewCase(emptyCaseForm);
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("案例已创建");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "创建案例失败");
    } finally {
      setLoading(false);
    }
  }

  function selectCase(caseItem: CaseStudy) {
    setSelectedCaseId(caseItem.id);
    setCaseDraft(caseItem);
  }

  async function saveCase() {
    if (!caseDraft) return;
    if (!caseDraft.title.trim() || !caseDraft.slug.trim()) {
      setMessage("案例标题和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const updated = await updateCase(caseDraft.id, {
        title: caseDraft.title.trim(),
        slug: caseDraft.slug.trim(),
        client_name: caseDraft.client_name,
        industry: caseDraft.industry,
        summary: caseDraft.summary,
        challenge: caseDraft.challenge,
        solution: caseDraft.solution,
        result: caseDraft.result,
        cover_image: caseDraft.cover_image,
        project_date: caseDraft.project_date,
        status: caseDraft.status
      });
      setCases((items) => items.map((item) => (item.id === updated.id ? updated : item)));
      setCaseDraft(updated);
      await refreshSiteDerivedState(caseDraft.site_id);
      setMessage("案例已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存案例失败");
    } finally {
      setLoading(false);
    }
  }

  async function removeCase() {
    if (!siteDraft || !caseDraft || !window.confirm(`删除案例「${caseDraft.title}」？`)) return;
    setLoading(true);
    try {
      await deleteCase(caseDraft.id);
      await loadSelectedSite(siteDraft.id);
      setMessage("案例已删除");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "删除案例失败");
      setLoading(false);
    }
  }

  async function handleCreateService(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!siteDraft) return;
    if (!newService.name.trim() || !newService.slug.trim()) {
      setMessage("服务名称和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const created = await createService(siteDraft.id, {
        ...newService,
        name: newService.name.trim(),
        slug: newService.slug.trim(),
        category: newService.category || "服务",
        summary: newService.summary || "",
        scope: newService.scope || "",
        process: newService.process || "",
        deliverables: newService.deliverables || "",
        price_note: newService.price_note || ""
      });
      setServices((items) => [created, ...items]);
      setSelectedServiceId(created.id);
      setServiceDraft(created);
      setNewService(emptyServiceForm);
      await refreshSiteDerivedState(siteDraft.id);
      setMessage("服务项目已创建");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "创建服务项目失败");
    } finally {
      setLoading(false);
    }
  }

  function selectService(item: ServiceItem) {
    setSelectedServiceId(item.id);
    setServiceDraft(item);
  }

  async function saveService() {
    if (!serviceDraft) return;
    if (!serviceDraft.name.trim() || !serviceDraft.slug.trim()) {
      setMessage("服务名称和 slug 不能为空");
      return;
    }
    setLoading(true);
    try {
      const updated = await updateService(serviceDraft.id, {
        name: serviceDraft.name.trim(),
        slug: serviceDraft.slug.trim(),
        category: serviceDraft.category,
        summary: serviceDraft.summary,
        scope: serviceDraft.scope,
        process: serviceDraft.process,
        deliverables: serviceDraft.deliverables,
        price_note: serviceDraft.price_note,
        status: serviceDraft.status
      });
      setServices((items) => items.map((item) => (item.id === updated.id ? updated : item)));
      setServiceDraft(updated);
      await refreshSiteDerivedState(serviceDraft.site_id);
      setMessage("服务项目已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存服务项目失败");
    } finally {
      setLoading(false);
    }
  }

  async function removeService() {
    if (!siteDraft || !serviceDraft || !window.confirm(`删除服务「${serviceDraft.name}」？`)) return;
    setLoading(true);
    try {
      await deleteService(serviceDraft.id);
      await loadSelectedSite(siteDraft.id);
      setMessage("服务项目已删除");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "删除服务项目失败");
      setLoading(false);
    }
  }

  async function handleUploadAsset(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!siteDraft || !assetFile) {
      setMessage("请选择要上传的文件");
      return;
    }
    setLoading(true);
    try {
      const uploaded = await uploadAsset(siteDraft.id, assetFile, assetAltText);
      setAssets((items) => [uploaded, ...items]);
      setSelectedAssetId(uploaded.id);
      setAssetDraft(uploaded);
      setAssetFile(null);
      setAssetAltText("");
      setMessage("媒体素材已上传");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "上传媒体素材失败");
    } finally {
      setLoading(false);
    }
  }

  function selectAsset(asset: MediaAsset) {
    setSelectedAssetId(asset.id);
    setAssetDraft(asset);
  }

  async function saveAsset() {
    if (!assetDraft) return;
    setLoading(true);
    try {
      const updated = await updateAsset(assetDraft.id, { alt_text: assetDraft.alt_text });
      setAssets((items) => items.map((item) => (item.id === updated.id ? updated : item)));
      setAssetDraft(updated);
      setMessage("媒体素材说明已保存");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "保存媒体素材失败");
    } finally {
      setLoading(false);
    }
  }

  async function removeAsset() {
    if (!siteDraft || !assetDraft || !window.confirm(`删除素材「${assetDraft.filename}」？`)) return;
    setLoading(true);
    try {
      await deleteAsset(assetDraft.id);
      await loadSelectedSite(siteDraft.id);
      setMessage("媒体素材已删除");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "删除媒体素材失败");
      setLoading(false);
    }
  }

  async function handlePublish() {
    if (!siteDraft) return;
    setLoading(true);
    try {
      setPublishReadiness(await getPublishReadiness(siteDraft.id));
      const record = await publishSite(siteDraft.id);
      setPublishes((items) => [record, ...items]);
      setMessage(`发布完成：${record.version}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "发布失败");
    } finally {
      setLoading(false);
    }
  }

  function openPreview(target: PreviewTarget) {
    setPreviewTarget(target);
    setActiveSection("preview");
  }

  function openFocusedSectionPreview(section: "identity" | "company", title: string, description: string) {
    if (!siteDraft) return;
    openPreview({
      title,
      description,
      path: `/api/sites/${siteDraft.id}/preview/focus/${section}`
    });
  }

  return (
    <div className="appShell">
      <header className="topbar">
        <div>
          <div className="productName">WBS 管理后台</div>
          <div className="subtle">企业官网后台管理系统 / 模板建站系统 MVP</div>
        </div>
        <div className="statusLine">
          <span>{loading ? "处理中" : "就绪"}</span>
          <button className="iconButton" onClick={refreshSites} title="刷新站点">
            <RefreshCw size={16} />
          </button>
        </div>
      </header>

      <div className="workspace">
        <aside className="sidebar">
          <form className="createBox" onSubmit={handleCreateSite}>
            <div className="sectionTitle">创建站点</div>
            <Field label="租户" tone="required" hint="单公司使用时保持 default 即可。">
              <input
                value={newSite.tenant_id}
                onChange={(event) => setNewSite({ ...newSite, tenant_id: event.target.value })}
              />
            </Field>
            <Field label="站点名称" tone="required" hint="后台中识别这个官网项目的名称。">
              <input
                value={newSite.name}
                onChange={(event) => setNewSite({ ...newSite, name: event.target.value })}
                placeholder="例如：某某科技官网"
              />
            </Field>
            <Field label="模板" tone="required" hint="当前先保持 template_basic。">
              <input
                value={newSite.template_id}
                onChange={(event) => setNewSite({ ...newSite, template_id: event.target.value })}
              />
            </Field>
            <Field label="域名" hint="没有正式域名可以先留空。">
              <input
                value={newSite.domain ?? ""}
                onChange={(event) => setNewSite({ ...newSite, domain: event.target.value })}
                placeholder="example.com"
              />
            </Field>
            <button className="primaryButton" type="submit">
              <Plus size={16} />
              新建空壳官网
            </button>
          </form>

          <div className="siteListHeader">
            <span>站点</span>
            <span>{sites.length}</span>
          </div>
          <div className="siteList">
            {sites.map((site) => (
              <button
                key={site.id}
                className={site.id === selectedSiteId ? "siteItem active" : "siteItem"}
                onClick={() => {
                  setSelectedSiteId(site.id);
                  setActiveSection("dashboard");
                }}
              >
                <span>{site.name}</span>
                <small>{site.status}</small>
              </button>
            ))}
            {sites.length === 0 && <div className="emptyState">还没有站点</div>}
          </div>
        </aside>

        <main className="contentArea">
          <div className="messageBar">{message || "先创建站点，再维护资料和预览前台。"}</div>

          {!selectedSite && <div className="blankPanel">请选择或创建一个站点。</div>}

          {selectedSite && siteDraft && (
            <>
              <nav className="moduleNav" aria-label="站点模块导航">
                {workspaceSections.map((section) => {
                  const Icon = section.icon;
                  return (
                    <button
                      key={section.id}
                      className={activeSection === section.id ? "moduleNavItem active" : "moduleNavItem"}
                      onClick={() => {
                        if (section.id === "preview") {
                          openPreview({
                            title: "总体预览",
                            description: "查看当前官网首页和整体内容。",
                            path: `/api/sites/${siteDraft.id}/preview`
                          });
                          return;
                        }
                        setActiveSection(section.id);
                      }}
                    >
                      <Icon size={15} />
                      <span>{section.label}</span>
                    </button>
                  );
                })}
              </nav>

              {activeSection === "dashboard" && (
                <SiteDashboardPanel
                  site={siteDraft}
                  profile={siteProfile}
                  companyProfile={companyProfile}
                  pages={pages}
                  articles={articles}
                  products={products}
                  faqs={faqs}
                  cases={cases}
                  services={services}
                  assets={assets}
                  publishes={publishes}
                  readiness={publishReadiness}
                  onNavigate={setActiveSection}
                />
              )}

              {activeSection === "identity" && (
                <SiteIdentityPanel
                  site={siteDraft}
                  profile={siteProfile}
                  assets={assets}
                  onSiteChange={setSiteDraft}
                  onProfileChange={setSiteProfile}
                  onSave={saveSiteIdentity}
                  onPreview={() =>
                    openFocusedSectionPreview("identity", "顶部预览", "只查看官网顶部品牌、名称、副标题和默认展示效果。")
                  }
                />
              )}

              {activeSection === "company" && (
                <CompanyProfilePanel
                  profile={companyProfile}
                  onChange={setCompanyProfile}
                  onSave={saveCompany}
                  onPreview={() =>
                    openFocusedSectionPreview("company", "档案预览", "只查看企业介绍和联系方式在官网中的展示片段。")
                  }
                />
              )}

              {activeSection === "pages" && (
                <PagePanel
                  pages={pages}
                  selectedId={selectedPageId}
                  draft={pageDraft}
                  newPage={newPage}
                  onNewChange={setNewPage}
                  onDraftChange={setPageDraft}
                  onCreate={handleCreatePage}
                  onSelect={selectPage}
                  onSave={savePage}
                  onRemove={removePage}
                  onPreview={(page) =>
                    openPreview({
                      title: "页面预览",
                      description: "查看当前固定页面在官网中的独立页面效果。",
                      path: `/api/sites/${page.site_id}/preview/focus/pages/${page.slug}`
                    })
                  }
                />
              )}

              {activeSection === "articles" && (
                <ArticlePanel
                  articles={articles}
                  selectedId={selectedArticleId}
                  draft={articleDraft}
                  newArticle={newArticle}
                  assets={assets}
                  onNewChange={setNewArticle}
                  onDraftChange={setArticleDraft}
                  onCreate={handleCreateArticle}
                  onSelect={selectArticle}
                  onSave={saveArticle}
                  onRemove={removeArticle}
                  onPreview={(article) =>
                    openPreview({
                      title: "文章预览",
                      description: "查看当前文章详情页效果。",
                      path: `/api/sites/${article.site_id}/preview/focus/articles/${article.slug}`
                    })
                  }
                />
              )}

              {activeSection === "products" && (
                <ProductPanel
                  products={products}
                  selectedId={selectedProductId}
                  draft={productDraft}
                  newProduct={newProduct}
                  assets={assets}
                  onNewChange={setNewProduct}
                  onDraftChange={setProductDraft}
                  onCreate={handleCreateProduct}
                  onSelect={selectProduct}
                  onSave={saveProduct}
                  onRemove={removeProduct}
                  onPreview={(product) =>
                    openPreview({
                      title: "产品预览",
                      description: "查看当前产品详情页效果。",
                      path: `/api/sites/${product.site_id}/preview/focus/products/${product.slug}`
                    })
                  }
                />
              )}

              {activeSection === "cases" && (
                <CasePanel
                  cases={cases}
                  selectedId={selectedCaseId}
                  draft={caseDraft}
                  newCase={newCase}
                  assets={assets}
                  onNewChange={setNewCase}
                  onDraftChange={setCaseDraft}
                  onCreate={handleCreateCase}
                  onSelect={selectCase}
                  onSave={saveCase}
                  onRemove={removeCase}
                  onPreview={(caseItem) =>
                    openPreview({
                      title: "案例预览",
                      description: "查看当前案例详情页效果。",
                      path: `/api/sites/${caseItem.site_id}/preview/focus/cases/${caseItem.slug}`
                    })
                  }
                />
              )}

              {activeSection === "services" && (
                <ServicePanel
                  services={services}
                  selectedId={selectedServiceId}
                  draft={serviceDraft}
                  newService={newService}
                  onNewChange={setNewService}
                  onDraftChange={setServiceDraft}
                  onCreate={handleCreateService}
                  onSelect={selectService}
                  onSave={saveService}
                  onRemove={removeService}
                  onPreview={(serviceItem) =>
                    openPreview({
                      title: "服务预览",
                      description: "查看当前服务详情页效果。",
                      path: `/api/sites/${serviceItem.site_id}/preview/focus/services/${serviceItem.slug}`
                    })
                  }
                />
              )}

              {activeSection === "faqs" && (
                <FaqPanel
                  faqs={faqs}
                  selectedId={selectedFaqId}
                  draft={faqDraft}
                  newFaq={newFaq}
                  onNewChange={setNewFaq}
                  onDraftChange={setFaqDraft}
                  onCreate={handleCreateFaq}
                  onSelect={selectFaq}
                  onSave={saveFaq}
                  onRemove={removeFaq}
                />
              )}

              {activeSection === "media" && (
                <MediaPanel
                  assets={assets}
                  selectedAssetId={selectedAssetId}
                  assetDraft={assetDraft}
                  assetFile={assetFile}
                  assetAltText={assetAltText}
                  onUpload={handleUploadAsset}
                  onFileChange={setAssetFile}
                  onAltTextChange={setAssetAltText}
                  onSelect={selectAsset}
                  onDraftChange={setAssetDraft}
                  onSave={saveAsset}
                  onRemove={removeAsset}
                />
              )}

              {activeSection === "publish" && (
                <PublishPanel publishes={publishes} readiness={publishReadiness} onPublish={handlePublish} />
              )}

              {activeSection === "preview" && (
                <PreviewPanel
                  siteId={siteDraft.id}
                  previewVersion={previewVersion}
                  target={previewTarget}
                />
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}


function sortPages(left: ContentPage, right: ContentPage) {
  return left.sort_order - right.sort_order || left.created_at.localeCompare(right.created_at);
}

function sortFaqs(left: FAQItem, right: FAQItem) {
  return left.sort_order - right.sort_order || left.created_at.localeCompare(right.created_at);
}
