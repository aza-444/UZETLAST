from django.apps import AppConfig
from django.contrib import admin


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = "Asosiy bo'lim"

    def ready(self):
        admin.site.site_header = "UZEnergo Ta'minlash — Admin Panel"
        admin.site.site_title = "UZEnergo Ta'minlash"
        admin.site.index_title = "Saytni to'liq boshqarish"
