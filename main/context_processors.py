from .models import SiteSettings


def site_context(request):
    settings_obj = SiteSettings.objects.first()
    lang = request.session.get('lang', 'uz')
    if lang not in ('uz', 'ru', 'en'):
        lang = 'uz'
    return {
        'site_settings': settings_obj,
        'settings': settings_obj,
        'current_lang': lang,
    }
