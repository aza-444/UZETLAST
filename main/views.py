from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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
    """Navbar dropdown uchun kategoriyalar va yillar"""
    from .models import CorporateCategory
    cats = CorporateCategory.objects.filter(is_active=True)
    result = []
    for cat in cats:
        docs = cat.documents.filter(is_active=True)
        years = sorted(
            docs.filter(is_archive=False).values_list('year', flat=True).distinct(),
            reverse=True
        )
        has_archive = docs.filter(is_archive=True).exists()
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
    # Redirect back to the referring page if possible to keep context
    next_url = request.META.get('HTTP_REFERER')
    if not next_url:
        next_url = '/'  # fallback to home page
    return redirect(next_url)


@require_POST
def contact_submit(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    message_text = request.POST.get('message', '').strip()

    if name and phone and message_text:
        ContactMessage.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message_text,
        )
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, 'Xabaringiz yuborildi! Tez orada bog\'lanamiz.')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Barcha maydonlarni to\'ldiring'})
        messages.error(request, 'Iltimos, barcha majburiy maydonlarni to\'ldiring.')

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
    categories = CorporateCategory.objects.filter(is_active=True)

    cat_data = []
    for cat in categories:
        docs = cat.documents.filter(is_active=True)
        years = sorted(
            docs.filter(is_archive=False).values_list('year', flat=True).distinct(),
            reverse=True
        )
        has_archive = docs.filter(is_archive=True).exists()
        cat_data.append({'category': cat, 'years': years, 'has_archive': has_archive})

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
            year_int = 2026
        documents = CorporateDocument.objects.filter(
            category=category, year=year_int, is_archive=False, is_active=True
        )
        current_year = year_int

    # Sidebar: barcha yillar ro'yxati
    all_docs = category.documents.filter(is_active=True)
    years = sorted(
        all_docs.filter(is_archive=False).values_list('year', flat=True).distinct(),
        reverse=True
    )
    has_archive = all_docs.filter(is_archive=True).exists()

    # Barcha kategoriyalar (sidebar "Boshqa bo'limlar" uchun)
    all_categories = CorporateCategory.objects.filter(is_active=True)
    categories_with_url = []
    for c in all_categories:
        if c.slug == cat_slug:
            continue  # joriy kategoriyani o'tkazib yuboramiz
        c_docs = c.documents.filter(is_active=True)
        c_years = sorted(
            c_docs.filter(is_archive=False).values_list('year', flat=True).distinct(),
            reverse=True
        )
        if c_years:
            first_url = f'/korporativ/{c.slug}/{c_years[0]}/'
        elif c_docs.filter(is_archive=True).exists():
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
    from django.shortcuts import get_object_or_404
    doc = get_object_or_404(CorporateDocument, id=doc_id, is_active=True)
    lang = request.session.get('lang', 'uz')
    settings_obj = SiteSettings.objects.first()
    
    # Check if the document exists physically
    import os
    from django.conf import settings
    file_exists = False
    if doc.file and hasattr(doc.file, 'url'):
        file_path = os.path.join(settings.MEDIA_ROOT, doc.file.name)
        file_exists = os.path.exists(file_path)

    context = {
        'lang': lang,
        'settings': settings_obj,
        'menu_items': get_menu_items(lang),
        'corp_nav': get_corporate_nav_data(),
        'doc': doc,
        'file_exists': file_exists,
    }
    return render(request, 'main/corporate_doc_viewer.html', context)
