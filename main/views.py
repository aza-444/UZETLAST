from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.clickjacking import xframe_options_exempt
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from .models import (
    SiteSettings, HeroSection, AboutSection,
    Service, CatalogItem, News, ContactMessage,
    CorporateCategory, CorporateDocument, Partner
)


def get_lang(request):
    lang = request.session.get('lang', 'uz')
    if lang not in ('uz', 'ru', 'en'):
        lang = 'uz'
    return lang


def get_corporate_nav_data():
    """Navbar dropdown uchun kategoriyalar va yillar (prefetch_related bilan optimizatsiyalangan)"""
    from .models import CorporateCategory
    cats = CorporateCategory.objects.filter(is_active=True).prefetch_related('documents')
    result = []
    for cat in cats:
        active_docs = [d for d in cat.documents.all() if d.is_active]
        years = sorted(
            {d.year for d in active_docs if not d.is_archive},
            reverse=True
        )
        has_archive = any(d.is_archive for d in active_docs)
        result.append({'category': cat, 'years': years, 'has_archive': has_archive})
    return result


def index(request):
    lang = get_lang(request)
    hero = HeroSection.objects.filter(is_active=True).first()
    about = AboutSection.objects.filter(is_active=True).first()
    services = Service.objects.filter(is_active=True)
    catalog_items = CatalogItem.objects.filter(is_active=True)
    news = News.objects.filter(is_active=True)[:6]
    partners = Partner.objects.filter(is_active=True)
    settings_obj = SiteSettings.objects.first()

    context = {
        'lang': lang,
        'hero': hero,
        'about': about,
        'services': services,
        'catalog_items': catalog_items,
        'news': news,
        'partners': partners,
        'settings': settings_obj,
        'LANGUAGES': {'uz': "O'zbek", 'ru': 'Русский', 'en': 'English'},
        'menu_items': get_menu_items(lang),
        'corp_nav': get_corporate_nav_data(),
    }
    return render(request, 'main/index.html', context)


def set_language(request, lang):
    if lang in ('uz', 'ru', 'en'):
        request.session['lang'] = lang
    # Faqat shu sayt ichidagi refererga qaytish (open-redirect himoyasi)
    from django.utils.http import url_has_allowed_host_and_scheme
    next_url = request.META.get('HTTP_REFERER', '')
    if not next_url or not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = '/'
    return redirect(next_url)


@require_POST
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def contact_submit(request):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    message_text = request.POST.get('message', '').strip()

    # Uzunlik va mavjudlik tekshiruvlari
    if not (name and phone and message_text):
        err = "Iltimos, barcha majburiy maydonlarni to'ldiring."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': err})
        messages.error(request, err)
        return redirect('/#aloqa')

    if len(name) > 150 or len(phone) > 50 or len(message_text) > 5000 or len(email) > 254:
        err = "Kiritilgan ma'lumotlar uzunlik me'yoridan oshib ketdi."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': err})
        messages.error(request, err)
        return redirect('/#aloqa')

    if email:
        try:
            validate_email(email)
        except ValidationError:
            err = "Email manzili noto'g'ri shaklda kiritildi."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': err})
            messages.error(request, err)
            return redirect('/#aloqa')

    ContactMessage.objects.create(
        name=name,
        phone=phone,
        email=email,
        message=message_text,
    )
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    messages.success(request, 'Xabaringiz yuborildi! Tez orada bog\'lanamiz.')
    return redirect('/#aloqa')


def get_menu_items(lang):
    items = {
        'uz': [
            ('bosh-sahifa', 'Bosh sahifa'),
            ('haqimizda', 'Biz haqimizda'),
            ('katalog', 'Katalog'),
            ('xizmatlar', 'Xizmatlar'),
            ('yangiliklar', 'Yangiliklar'),
            ('aloqa', 'Aloqa'),
            ('korporativ', 'Korporativ boshqaruv'),
        ],
        'ru': [
            ('bosh-sahifa', 'Главная'),
            ('haqimizda', 'О нас'),
            ('katalog', 'Каталог'),
            ('xizmatlar', 'Услуги'),
            ('yangiliklar', 'Новости'),
            ('aloqa', 'Контакты'),
            ('korporativ', 'Корпоративное управление'),
        ],
        'en': [
            ('bosh-sahifa', 'Home'),
            ('haqimizda', 'About Us'),
            ('katalog', 'Catalog'),
            ('xizmatlar', 'Services'),
            ('yangiliklar', 'News'),
            ('aloqa', 'Contact'),
            ('korporativ', 'Corporate Governance'),
        ],
    }
    return items.get(lang, items['uz'])


def corporate_index(request):
    """Korporativ boshqaruv bosh sahifasi"""
    lang = get_lang(request)
    settings_obj = SiteSettings.objects.first()
    cat_data = get_corporate_nav_data()

    context = {
        'lang': lang,
        'settings': settings_obj,
        'menu_items': get_menu_items(lang),
        'cat_data': cat_data,
        'corp_nav': cat_data,
    }
    return render(request, 'main/corporate.html', context)


def corporate_documents(request, cat_slug, year_or_arxiv):
    """Ma'lum kategoriya va yil bo'yicha hujjatlar ro'yxati"""
    lang = get_lang(request)
    settings_obj = SiteSettings.objects.first()
    category = get_object_or_404(CorporateCategory, slug=cat_slug, is_active=True)

    if year_or_arxiv == 'arxiv':
        documents = CorporateDocument.objects.filter(
            category=category, is_archive=True, is_active=True
        )
        current_year = 'arxiv'
    else:
        try:
            year_int = int(year_or_arxiv)
        except (ValueError, TypeError):
            latest = (
                category.documents.filter(is_active=True, is_archive=False)
                .order_by('-year')
                .values_list('year', flat=True)
                .first()
            )
            year_int = latest if latest is not None else 0
        documents = CorporateDocument.objects.filter(
            category=category, year=year_int, is_archive=False, is_active=True
        )
        current_year = year_int

    all_docs = list(category.documents.filter(is_active=True))
    years = sorted(
        {d.year for d in all_docs if not d.is_archive},
        reverse=True
    )
    has_archive = any(d.is_archive for d in all_docs)

    all_categories = CorporateCategory.objects.filter(is_active=True).prefetch_related('documents')
    categories_with_url = []
    for c in all_categories:
        if c.slug == cat_slug:
            continue
        c_docs = [d for d in c.documents.all() if d.is_active]
        c_years = sorted(
            {d.year for d in c_docs if not d.is_archive},
            reverse=True
        )
        if c_years:
            first_url = f'/korporativ/{c.slug}/{c_years[0]}/'
        elif any(d.is_archive for d in c_docs):
            first_url = f'/korporativ/{c.slug}/arxiv/'
        else:
            first_url = f'/korporativ/{c.slug}/'
        categories_with_url.append({'cat': c, 'url': first_url})

    context = {
        'lang': lang,
        'settings': settings_obj,
        'menu_items': get_menu_items(lang),
        'category': category,
        'documents': documents,
        'current_year': current_year,
        'years': years,
        'has_archive': has_archive,
        'categories_with_url': categories_with_url,
        'corp_nav': get_corporate_nav_data(),
    }
    return render(request, 'main/corporate_docs.html', context)


def robots_txt(request):
    from django.http import HttpResponse
    content = """User-agent: *
Allow: /
Disallow: /admin/

Sitemap: {scheme}://{host}/sitemap.xml
""".format(scheme=request.scheme, host=request.get_host())
    return HttpResponse(content, content_type='text/plain')


def document_viewer(request, doc_id):
    from pathlib import Path
    from django.conf import settings as django_settings
    from django.urls import reverse

    doc = get_object_or_404(
        CorporateDocument.objects.select_related('category'),
        id=doc_id,
        is_active=True,
    )
    lang = get_lang(request)
    settings_obj = SiteSettings.objects.first()

    file_exists = False
    file_url = ''
    if doc.file and doc.file.name:
        media_root = Path(django_settings.MEDIA_ROOT).resolve()
        file_path = (media_root / doc.file.name).resolve()
        if file_path.is_relative_to(media_root) and file_path.is_file():
            file_exists = True
            file_url = request.build_absolute_uri(doc.file.url)

    ext = doc.file_extension() if file_exists else ''
    preview_kind = 'other'
    if ext == 'pdf':
        preview_kind = 'pdf'
    elif ext in ('xls', 'xlsx', 'csv'):
        preview_kind = 'excel'
    elif ext in ('doc', 'docx'):
        preview_kind = 'word'
    elif ext in ('png', 'jpg', 'jpeg', 'gif', 'webp'):
        preview_kind = 'image'

    if doc.is_archive:
        year_or_arxiv = 'arxiv'
    else:
        year_or_arxiv = str(doc.year or 'arxiv')
    try:
        back_url = reverse(
            'corporate_documents',
            args=[doc.category.slug, year_or_arxiv],
        )
    except Exception:
        back_url = reverse('corporate_index')

    context = {
        'lang': lang,
        'settings': settings_obj,
        'menu_items': get_menu_items(lang),
        'corp_nav': get_corporate_nav_data(),
        'doc': doc,
        'file_exists': file_exists,
        'file_url': file_url,
        'file_ext': ext,
        'preview_kind': preview_kind,
        'back_url': back_url,
        'is_subpage': True,
    }
    return render(request, 'main/corporate_doc_viewer.html', context)


def document_download(request, doc_id):
    """Force file download (Excel/PDF/Word) — with Path Traversal protection."""
    import mimetypes
    from pathlib import Path
    from django.conf import settings as django_settings

    doc = get_object_or_404(CorporateDocument, id=doc_id, is_active=True)
    if not doc.file or not doc.file.name:
        raise Http404

    media_root = Path(django_settings.MEDIA_ROOT).resolve()
    file_path = (media_root / doc.file.name).resolve()
    if not file_path.is_relative_to(media_root) or not file_path.is_file():
        raise Http404

    content_type, _ = mimetypes.guess_type(str(file_path))
    if not content_type:
        content_type = 'application/octet-stream'

    filename = file_path.name
    response = FileResponse(file_path.open('rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@xframe_options_exempt
def document_file(request, doc_id):
    """Inline file stream for in-browser preview — with Path Traversal protection."""
    import mimetypes
    from pathlib import Path
    from django.conf import settings as django_settings

    doc = get_object_or_404(CorporateDocument, id=doc_id, is_active=True)
    if not doc.file or not doc.file.name:
        raise Http404

    media_root = Path(django_settings.MEDIA_ROOT).resolve()
    file_path = (media_root / doc.file.name).resolve()
    if not file_path.is_relative_to(media_root) or not file_path.is_file():
        raise Http404

    content_type, _ = mimetypes.guess_type(str(file_path))
    if not content_type:
        content_type = 'application/octet-stream'

    filename = file_path.name
    response = FileResponse(file_path.open('rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    response['X-Content-Type-Options'] = 'nosniff'
    return response


def news_detail(request, slug):
    lang = get_lang(request)
    news_item = get_object_or_404(
        News.objects.prefetch_related('images', 'files'),
        slug=slug,
        is_active=True,
        is_detailed=True
    )
    settings_obj = SiteSettings.objects.first()
    context = {
        'lang': lang,
        'settings': settings_obj,
        'menu_items': get_menu_items(lang),
        'corp_nav': get_corporate_nav_data(),
        'news_item': news_item,
        'is_subpage': True,
    }
    return render(request, 'main/news_detail.html', context)


def corporate_detail(request, doc_id):
    lang = get_lang(request)
    doc = get_object_or_404(
        CorporateDocument.objects.prefetch_related('images', 'files'),
        id=doc_id,
        is_active=True,
        is_detailed=True
    )
    settings_obj = SiteSettings.objects.first()
    context = {
        'lang': lang,
        'settings': settings_obj,
        'menu_items': get_menu_items(lang),
        'corp_nav': get_corporate_nav_data(),
        'doc': doc,
        'is_subpage': True,
    }
    return render(request, 'main/corporate_detail.html', context)
