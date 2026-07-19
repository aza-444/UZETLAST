from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticViewSitemap, CorporateDocsSitemap

admin.site.site_header = "UZEnergo Ta'minlash — Admin Panel"
admin.site.site_title = "UZEnergo Ta'minlash"
admin.site.index_title = "Sayt boshqaruvi"

sitemaps = {
    'static': StaticViewSitemap,
    'corporate': CorporateDocsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'main/sitemap.xml'}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
