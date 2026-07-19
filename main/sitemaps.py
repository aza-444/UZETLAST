from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['index', 'corporate_index']

    def location(self, item):
        return reverse(item)


class CorporateDocsSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        from main.models import CorporateCategory, CorporateDocument
        result = []
        cats = CorporateCategory.objects.filter(is_active=True)
        for cat in cats:
            docs = cat.documents.filter(is_active=True)
            years = docs.filter(is_archive=False).values_list('year', flat=True).distinct()
            for year in years:
                result.append((cat.slug, str(year)))
            if docs.filter(is_archive=True).exists():
                result.append((cat.slug, 'arxiv'))
        return result

    def location(self, item):
        return reverse('corporate_documents', args=[item[0], item[1]])
