# coding: utf-8
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import (
    SiteSettings, HeroSection, AboutSection,
    Service, CatalogItem, News, ContactMessage,
    CorporateCategory, CorporateDocument, Partner
)


# ─────────────────────────────────────────────────────────────
#  Premium rang palitrasi (admin da ko'rinadigan swatches)
# ─────────────────────────────────────────────────────────────
PREMIUM_LIGHT_COLORS = [
    # Primary (asosiy rang)
    ("#f59e0b", "Amber Gold"),
    ("#0ea5e9", "Sky Blue"),
    ("#8b5cf6", "Violet"),
    ("#10b981", "Emerald"),
    ("#ef4444", "Rose Red"),
    ("#f97316", "Orange"),
    ("#06b6d4", "Cyan"),
    ("#6366f1", "Indigo"),
    ("#ec4899", "Pink"),
    ("#14b8a6", "Teal"),
    ("#84cc16", "Lime"),
    ("#a855f7", "Purple"),
]


class ColorPreviewWidget(forms.TextInput):
    """HTML5 color picker + hex value input"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'type': 'color', 'style': 'width:80px;height:40px;border-radius:8px;cursor:pointer;border:1px solid #ccc;'})

    class Media:
        css = {'all': []}
        js = []


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'primary_color': ColorPreviewWidget(),
            'accent_color': ColorPreviewWidget(),
            'bg_color': ColorPreviewWidget(),
            'bg_card_color': ColorPreviewWidget(),
            'bg_section_color': ColorPreviewWidget(),
            'text_color': ColorPreviewWidget(),
            'text_secondary_color': ColorPreviewWidget(),
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm
    fieldsets = (
        ('📞 Aloqa ma\'lumotlari', {
            'fields': ('phone_1', 'phone_2', 'email')
        }),
        ('📍 Manzil va Xarita', {
            'fields': ('address_uz', 'address_ru', 'address_en', 'map_iframe')
        }),
        ('🌐 Ijtimoiy tarmoqlar', {
            'fields': ('telegram', 'instagram', 'facebook', 'youtube')
        }),
        ('🔍 SEO — O\'zbek', {
            'fields': ('meta_description_uz',)
        }),
        ('🔍 SEO — Русский', {
            'classes': ('collapse',),
            'fields': ('meta_title_ru', 'meta_description_ru')
        }),
        ('🔍 SEO — English', {
            'classes': ('collapse',),
            'fields': ('meta_title_en', 'meta_description_en')
        }),
        ('🔍 SEO Kalit so\'zlar', {
            'fields': ('meta_keywords',)
        }),
        ('🖼️ Logo va Favicon', {
            'fields': ('logo', 'favicon')
        }),
        ('🎨 Tema Ranglari — To\'liq boshqaruv', {
            'description': (
                'Har bir rang maydoniga bosib color picker orqali rang tanlang. '
                'Saqlash tugmasini bosgach saytda darhol aks etadi.<br>'
                '<strong>Tavsiya etilgan Premium ranglar:</strong> '
                + ' '.join(
                    f'<span title="{name}" style="display:inline-block;width:20px;height:20px;'
                    f'background:{hex_};border-radius:4px;margin:2px;border:1px solid #ccc;'
                    f'vertical-align:middle;" ></span> <code>{hex_}</code>'
                    for hex_, name in PREMIUM_LIGHT_COLORS
                )
            ),
            'fields': (
                'primary_color', 'accent_color',
                'bg_color', 'bg_card_color', 'bg_section_color',
                'text_color', 'text_secondary_color',
                'border_color',
            )
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def color_swatches(self, obj):
        colors = [
            (obj.primary_color, 'Primary'),
            (obj.accent_color, 'Accent'),
            (obj.bg_color, 'Background'),
            (obj.text_color, 'Text'),
            (obj.text_secondary_color, 'Secondary'),
        ]
        html = ''
        for c, label in colors:
            html += (
                f'<span title="{label}: {c}" style="display:inline-block;width:28px;height:28px;'
                f'background:{c};border-radius:6px;margin:2px;border:1px solid rgba(0,0,0,0.15);'
                f'vertical-align:middle;"></span>'
            )
        return format_html(html)

    color_swatches.short_description = "Ranglar"
    color_swatches.allow_tags = True


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'is_active')
    fieldsets = (
        ('🇺🇿 O\'zbek tili', {
            'fields': ('title_uz', 'subtitle_uz', 'btn_catalog_uz', 'btn_contact_uz')
        }),
        ('🇷🇺 Русский язык', {
            'classes': ('collapse',),
            'fields': ('title_ru', 'subtitle_ru', 'btn_catalog_ru', 'btn_contact_ru')
        }),
        ('🇬🇧 English', {
            'classes': ('collapse',),
            'fields': ('title_en', 'subtitle_en', 'btn_catalog_en', 'btn_contact_en')
        }),
        ('🖼️ Fon rasmi', {
            'fields': ('background_image', 'is_active')
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'name_uz', 'icon_preview', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name_uz',)
    fieldsets = (
        ('🇺🇿 O\'zbek tili', {
            'fields': ('name_uz', 'description_uz')
        }),
        ('🇷🇺 Русский язык', {
            'classes': ('collapse',),
            'fields': ('name_ru', 'description_ru')
        }),
        ('🇬🇧 English', {
            'classes': ('collapse',),
            'fields': ('name_en', 'description_en')
        }),
        ('⚙️ Qo\'shimcha', {
            'fields': ('icon', 'image', 'order', 'is_active')
        }),
    )

    def icon_preview(self, obj):
        return format_html('<i class="bi {}"></i> {}', obj.icon, obj.icon)
    icon_preview.short_description = "Icon"


@admin.register(CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name_uz', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name_uz',)
    list_filter = ('is_active',)
    fieldsets = (
        ('🇺🇿 O\'zbek tili', {
            'fields': ('name_uz', 'description_uz')
        }),
        ('🇷🇺 Русский язык', {
            'classes': ('collapse',),
            'fields': ('name_ru', 'description_ru')
        }),
        ('🇬🇧 English', {
            'classes': ('collapse',),
            'fields': ('name_en', 'description_en')
        }),
        ('⚙️ Qo\'shimcha', {
            'fields': ('image', 'order', 'is_active')
        }),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'years_experience', 'clients_count', 'projects_count', 'is_active')
    fieldsets = (
        ('🇺🇿 O\'zbek tili', {
            'fields': ('title_uz', 'content_uz', 'asosiy_vazifa_uz', 'vision_uz')
        }),
        ('🇷🇺 Русский язык', {
            'classes': ('collapse',),
            'fields': ('title_ru', 'content_ru', 'asosiy_vazifa_ru', 'vision_ru')
        }),
        ('🇬🇧 English', {
            'classes': ('collapse',),
            'fields': ('title_en', 'content_en', 'asosiy_vazifa_en', 'vision_en')
        }),
        ('📊 Statistika', {
            'fields': ('years_experience', 'clients_count', 'projects_count')
        }),
        ('🖼️ Rasm', {
            'fields': ('image', 'is_active')
        }),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'published_at', 'is_active', 'image_preview')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'published_at')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('slug',)
    fieldsets = (
        ('🇺🇿 O\'zbek tili', {
            'fields': ('title_uz', 'content_uz')
        }),
        ('🇷🇺 Русский язык', {
            'classes': ('collapse',),
            'fields': ('title_ru', 'content_ru')
        }),
        ('🇬🇧 English', {
            'classes': ('collapse',),
            'fields': ('title_en', 'content_en')
        }),
        ('⚙️ Qo\'shimcha', {
            'fields': ('image', 'published_at', 'is_active', 'slug')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.image.url)
        return "—"
    image_preview.short_description = "Rasm"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('name', 'phone', 'email', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'link', 'is_active', 'image_preview')
    list_display_links = ('name',)
    list_editable = ('order', 'is_active')
    search_fields = ('name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="40" style="object-fit:contain;border-radius:4px;"/>', obj.image.url)
        return "—"
    image_preview.short_description = "Logotip"


class CorporateDocumentInline(admin.TabularInline):
    model = CorporateDocument
    extra = 1
    fields = ('title_uz', 'year', 'is_archive', 'published_date', 'file', 'order', 'is_active')
    ordering = ['order', '-published_date']


@admin.register(CorporateCategory)
class CorporateCategoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'name_uz', 'slug', 'doc_count', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name_uz',)
    prepopulated_fields = {'slug': ('name_uz',)}
    inlines = [CorporateDocumentInline]
    fieldsets = (
        ('🇺🇿 O\'zbek tili', {
            'fields': ('name_uz',)
        }),
        ('🇷🇺 Русский язык', {
            'classes': ('collapse',),
            'fields': ('name_ru',)
        }),
        ('🇬🇧 English', {
            'classes': ('collapse',),
            'fields': ('name_en',)
        }),
        ('⚙️ Sozlamalar', {
            'fields': ('slug', 'order', 'is_active')
        }),
    )

    def doc_count(self, obj):
        return obj.documents.filter(is_active=True).count()
    doc_count.short_description = "Hujjatlar"


@admin.register(CorporateDocument)
class CorporateDocumentAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'category', 'display_year_col', 'is_archive', 'published_date', 'file_preview', 'is_active')
    list_editable = ('is_active', 'is_archive')
    list_display_links = ('title_uz',)
    list_filter = ('category', 'is_archive', 'year', 'is_active')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    fieldsets = (
        ('📄 Sarlavha', {
            'fields': ('category', 'title_uz', 'title_ru', 'title_en')
        }),
        ('📁 Fayl va vaqt', {
            'fields': ('file', 'year', 'is_archive', 'published_date')
        }),
        ('⚙️ Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )

    def display_year_col(self, obj):
        return "Arxiv" if obj.is_archive else str(obj.year)
    display_year_col.short_description = "Yil"

    def file_preview(self, obj):
        if obj.file:
            ext = obj.file_extension()
            icons = {'pdf': '📕', 'doc': '📘', 'docx': '📘', 'xls': '📗', 'xlsx': '📗'}
            icon = icons.get(ext, '📄')
            return format_html('{} <a href="{}" target="_blank">Ochish</a>', icon, obj.file.url)
        return "—"
    file_preview.short_description = "Fayl"
