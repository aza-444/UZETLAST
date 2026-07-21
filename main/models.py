from django.db import models
from django.utils import timezone
import os
from django.core.exceptions import ValidationError


def validate_svg_or_image(file):
    """SVG va oddiy rasm formatlarini qabul qiladi"""
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp']
    if ext.lower() not in valid_extensions:
        raise ValidationError("Faqat rasm yoki SVG formatidagi fayllar ruxsat etiladi (.svg, .png, .jpg, .jpeg, .gif, .webp)")

class SiteSettings(models.Model):
    """Sayt umumiy sozlamalari"""
    # Contact info
    phone_1 = models.CharField(max_length=50, blank=True, verbose_name="Telefon 1")
    phone_2 = models.CharField(max_length=50, blank=True, verbose_name="Telefon 2")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Address multilingual
    address_uz = models.CharField(max_length=300, blank=True, verbose_name="Manzil (UZ)")
    address_ru = models.CharField(max_length=300, blank=True, verbose_name="Manzil (RU)")
    address_en = models.CharField(max_length=300, blank=True, verbose_name="Address (EN)")
    map_iframe = models.TextField(blank=True, verbose_name="Xarita Iframe (Google/Yandex)", help_text="Xaritani ulash uchun Iframe kodini shu yerga kiriting")

    
    # Social media
    telegram = models.URLField(blank=True, verbose_name="Telegram")
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    youtube = models.URLField(blank=True, verbose_name="YouTube")
    
    # Theme colors (editable via admin)
    primary_color = models.CharField(max_length=7, default='#e8910c', help_text='Asosiy brand rangi (hex)', verbose_name='Primary Color')
    accent_color = models.CharField(max_length=7, default='#0284c7', help_text='Ikkinchi darajali rang (hex)', verbose_name='Accent Color')
    bg_color = models.CharField(max_length=7, default='#f3f6fa', help_text='Sahifa umumiy foni (hex)', verbose_name='Sahifa foni')
    bg_card_color = models.CharField(max_length=7, default='#ffffff', help_text='Karta/blok foni (hex)', verbose_name='Karta foni')
    bg_section_color = models.CharField(max_length=7, default='#e7edf5', help_text='Bo\'lim foni (alternativ, hex)', verbose_name='Bo\'lim foni')
    text_color = models.CharField(max_length=7, default='#0b1220', help_text='Asosiy matn rangi (hex)', verbose_name='Text Color')
    text_secondary_color = models.CharField(max_length=7, default='#3d4f66', help_text='Ikkinchi darajali matn rangi (hex)', verbose_name='Secondary Text Color')
    border_color = models.CharField(max_length=40, default='rgba(15,35,60,0.1)', help_text='Chegara rangi — rgba yoki hex (masalan: rgba(0,0,0,0.1))', verbose_name='Chegara rangi')
    meta_title_uz = models.CharField(max_length=200, blank=True, verbose_name="Meta Title (UZ)")
    meta_title_ru = models.CharField(max_length=200, blank=True, verbose_name="Meta Title (RU)")
    meta_title_en = models.CharField(max_length=200, blank=True, verbose_name="Meta Title (EN)")
    meta_description_uz = models.TextField(blank=True, verbose_name="Meta Description (UZ)")
    meta_description_ru = models.TextField(blank=True, verbose_name="Meta Description (RU)")
    meta_description_en = models.TextField(blank=True, verbose_name="Meta Description (EN)")
    meta_keywords = models.TextField(
        blank=True,
        default="uz uzet uzenergo uze energo ta'minlash energetika katalog mahsulotlar elektr jihozlari transformator generator",
        verbose_name="Meta Keywords (SEO)"
    )
    
    # Logo & favicon
    logo = models.ImageField(upload_to='settings/', blank=True, verbose_name="Logo")
    favicon = models.ImageField(upload_to='settings/', blank=True, verbose_name="Favicon")

    # Brand / company name (navbar & footer)
    company_name_uz = models.CharField(
        max_length=200, blank=True, default="O'ZENERGOTA'MINLASH",
        verbose_name="Kompaniya nomi (UZ)"
    )
    company_name_ru = models.CharField(
        max_length=200, blank=True, default="АО O'ZENERGOTA'MINLASH",
        verbose_name="Kompaniya nomi (RU)"
    )
    company_name_en = models.CharField(
        max_length=200, blank=True, default="JSC O'ZENERGOTA'MINLASH",
        verbose_name="Company name (EN)"
    )
    company_tagline_uz = models.CharField(
        max_length=200, blank=True, default="AKSIYADORLIK JAMIYATI",
        verbose_name="Tagline (UZ)"
    )
    company_tagline_ru = models.CharField(
        max_length=200, blank=True, default="АКЦИОНЕРНОЕ ОБЩЕСТВО",
        verbose_name="Tagline (RU)"
    )
    company_tagline_en = models.CharField(
        max_length=200, blank=True, default="JOINT STOCK COMPANY",
        verbose_name="Tagline (EN)"
    )
    footer_text_uz = models.TextField(
        blank=True,
        default="O'zbekistonda energetika uskunalarini yetkazib berish bo'yicha ishonchli hamkor",
        verbose_name="Footer matni (UZ)"
    )
    footer_text_ru = models.TextField(
        blank=True,
        default="Надёжный партнёр по поставке энергетического оборудования в Узбекистане",
        verbose_name="Footer matni (RU)"
    )
    footer_text_en = models.TextField(
        blank=True,
        default="Reliable partner for energy equipment supply in Uzbekistan",
        verbose_name="Footer text (EN)"
    )

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"

    def address(self, lang='uz'):
        val = getattr(self, f'address_{lang}', '')
        return val if val else self.address_uz

    def meta_title(self, lang='uz'):
        val = getattr(self, f'meta_title_{lang}', '') or ''
        if val:
            return val
        if lang == 'uz':
            return "O'zenergota'minlash — Energetika uskunalari"
        return self.meta_title_ru or "O'zenergota'minlash"

    def meta_description(self, lang='uz'):
        return getattr(self, f'meta_description_{lang}', self.meta_description_uz) or self.meta_description_uz

    def company_name(self, lang='uz'):
        val = getattr(self, f'company_name_{lang}', '') or ''
        return val if val else (self.company_name_uz or "O'ZENERGOTA'MINLASH")

    def company_tagline(self, lang='uz'):
        val = getattr(self, f'company_tagline_{lang}', '') or ''
        return val if val else (self.company_tagline_uz or '')

    def footer_text(self, lang='uz'):
        val = getattr(self, f'footer_text_{lang}', '') or ''
        return val if val else (self.footer_text_uz or '')


class HeroSection(models.Model):
    """Bosh sahifa hero bo'limi"""
    title_uz = models.CharField(max_length=200, verbose_name="Sarlavha (UZ)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Sarlavha (RU)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Title (EN)")
    
    subtitle_uz = models.TextField(verbose_name="Qisqa tavsif (UZ)")
    subtitle_ru = models.TextField(blank=True, verbose_name="Qisqa tavsif (RU)")
    subtitle_en = models.TextField(blank=True, verbose_name="Short description (EN)")
    
    btn_catalog_uz = models.CharField(max_length=100, default="Katalog", verbose_name="Katalog tugmasi (UZ)")
    btn_catalog_ru = models.CharField(max_length=100, default="Каталог", verbose_name="Katalog tugmasi (RU)")
    btn_catalog_en = models.CharField(max_length=100, default="Catalog", verbose_name="Catalog button (EN)")
    
    btn_contact_uz = models.CharField(max_length=100, default="Bog'lanish", verbose_name="Bog'lanish tugmasi (UZ)")
    btn_contact_ru = models.CharField(max_length=100, default="Связаться", verbose_name="Bog'lanish tugmasi (RU)")
    btn_contact_en = models.CharField(max_length=100, default="Contact Us", verbose_name="Contact button (EN)")

    badge_uz = models.CharField(
        max_length=120, blank=True, default="Energetika uchun yechimlar",
        verbose_name="Hero badge (UZ)"
    )
    badge_ru = models.CharField(
        max_length=120, blank=True, default="Решения для энергетики",
        verbose_name="Hero badge (RU)"
    )
    badge_en = models.CharField(
        max_length=120, blank=True, default="Solutions for Energy",
        verbose_name="Hero badge (EN)"
    )
    
    background_image = models.ImageField(upload_to='hero/', blank=True, verbose_name="Fon rasmi (Asosiy/Qorong'i)")
    background_image_light = models.ImageField(upload_to='hero/', blank=True, verbose_name="Fon rasmi (Kunduzgi rejim)")
    background_video = models.FileField(
        upload_to='hero/videos/',
        blank=True,
        verbose_name="Fon video (Qorong'i)",
        help_text="Ixtiyoriy. Qisqa MP4/WebM (tavsiya: 3–8 soniya, <3MB). Bo'sh bo'lsa engil canvas animatsiya ishlaydi."
    )
    background_video_light = models.FileField(
        upload_to='hero/videos/',
        blank=True,
        verbose_name="Fon video (Kunduzgi)",
        help_text="Ixtiyoriy. Kunduzgi rejim uchun. Bo'sh bo'lsa qorong'i video yoki canvas ishlatiladi."
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Hero bo'limi"
        verbose_name_plural = "Hero bo'limi"

    def __str__(self):
        return self.title_uz

    def title(self, lang='uz'):
        val = getattr(self, f'title_{lang}', '')
        return val if val else self.title_uz

    def subtitle(self, lang='uz'):
        val = getattr(self, f'subtitle_{lang}', '')
        return val if val else self.subtitle_uz

    def btn_catalog(self, lang='uz'):
        return getattr(self, f'btn_catalog_{lang}', self.btn_catalog_uz)

    def btn_contact(self, lang='uz'):
        return getattr(self, f'btn_contact_{lang}', self.btn_contact_uz)

    def badge(self, lang='uz'):
        val = getattr(self, f'badge_{lang}', '') or ''
        return val if val else (self.badge_uz or '')


class AboutSection(models.Model):
    """Kompaniya haqida bo'limi"""
    title_uz = models.CharField(max_length=200, default="Kompaniya haqida", verbose_name="Sarlavha (UZ)")
    title_ru = models.CharField(max_length=200, default="О компании", verbose_name="Sarlavha (RU)")
    title_en = models.CharField(max_length=200, default="About Company", verbose_name="Title (EN)")
    
    content_uz = models.TextField(verbose_name="Matn (UZ)")
    content_ru = models.TextField(blank=True, verbose_name="Matn (RU)")
    content_en = models.TextField(blank=True, verbose_name="Text (EN)")
    
    asosiy_vazifa_uz = models.TextField(blank=True, verbose_name="Asosiy vazifa (UZ)")
    asosiy_vazifa_ru = models.TextField(blank=True, verbose_name="Asosiy vazifa (RU)")
    asosiy_vazifa_en = models.TextField(blank=True, verbose_name="Asosiy vazifa (EN)")
    
    vision_uz = models.TextField(blank=True, verbose_name="Vizyon (UZ)")
    vision_ru = models.TextField(blank=True, verbose_name="Vizyon (RU)")
    vision_en = models.TextField(blank=True, verbose_name="Vision (EN)")
    
    image = models.ImageField(upload_to='about/', blank=True, verbose_name="Rasm")
    
    # Stats
    years_experience = models.PositiveIntegerField(default=10, verbose_name="Tajriba yillari")
    clients_count = models.PositiveIntegerField(default=500, verbose_name="Mijozlar soni")
    projects_count = models.PositiveIntegerField(default=1000, verbose_name="Loyihalar soni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Kompaniya haqida"
        verbose_name_plural = "Kompaniya haqida"

    def __str__(self):
        return self.title_uz

    def title(self, lang='uz'):
        val = getattr(self, f'title_{lang}', '')
        return val if val else self.title_uz

    def content(self, lang='uz'):
        val = getattr(self, f'content_{lang}', '')
        return val if val else self.content_uz

    def mission(self, lang='uz'):
        val = getattr(self, f'asosiy_vazifa_{lang}', '')
        return val if val else self.asosiy_vazifa_uz

    def vision(self, lang='uz'):
        val = getattr(self, f'vision_{lang}', '')
        return val if val else self.vision_uz


class Service(models.Model):
    """Xizmatlar"""
    name_uz = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (RU)")
    name_en = models.CharField(max_length=200, blank=True, verbose_name="Name (EN)")
    
    description_uz = models.TextField(verbose_name="Tavsif (UZ)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (RU)")
    description_en = models.TextField(blank=True, verbose_name="Description (EN)")
    
    icon = models.CharField(max_length=50, blank=True, default="bi-lightning-charge", verbose_name="Bootstrap Icon klassi")
    image = models.ImageField(upload_to='services/', blank=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ['order']

    def __str__(self):
        return self.name_uz

    def name(self, lang='uz'):
        val = getattr(self, f'name_{lang}', '')
        return val if val else self.name_uz

    def description(self, lang='uz'):
        val = getattr(self, f'description_{lang}', '')
        return val if val else self.description_uz


class CatalogItem(models.Model):
    """Katalog bo'limlari"""
    name_uz = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (RU)")
    name_en = models.CharField(max_length=200, blank=True, verbose_name="Name (EN)")
    
    description_uz = models.TextField(verbose_name="Tavsif (UZ)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (RU)")
    description_en = models.TextField(blank=True, verbose_name="Description (EN)")
    
    image = models.ImageField(upload_to='catalog/', blank=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Katalog bo'limi"
        verbose_name_plural = "Katalog bo'limlari"
        ordering = ['order']

    def __str__(self):
        return self.name_uz

    def name(self, lang='uz'):
        val = getattr(self, f'name_{lang}', '')
        return val if val else self.name_uz

    def description(self, lang='uz'):
        val = getattr(self, f'description_{lang}', '')
        return val if val else self.description_uz


class News(models.Model):
    """Yangiliklar"""
    title_uz = models.CharField(max_length=300, verbose_name="Sarlavha (UZ)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (RU)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Title (EN)")
    
    content_uz = models.TextField(verbose_name="Matn (UZ)")
    content_ru = models.TextField(blank=True, verbose_name="Matn (RU)")
    content_en = models.TextField(blank=True, verbose_name="Text (EN)")
    
    image = models.ImageField(upload_to='news/', blank=True, verbose_name="Rasm")
    published_at = models.DateTimeField(default=timezone.now, verbose_name="Sana")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    slug = models.SlugField(max_length=300, unique=True, blank=True, verbose_name="URL (slug)")

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-published_at']

    def __str__(self):
        return self.title_uz

    def title(self, lang='uz'):
        val = getattr(self, f'title_{lang}', '')
        return val if val else self.title_uz

    def content(self, lang='uz'):
        val = getattr(self, f'content_{lang}', '')
        return val if val else self.content_uz

    def save(self, *args, **kwargs):
        if not self.slug:
            import re
            from django.utils.text import slugify
            base = slugify(self.title_uz[:80] if self.title_uz else 'yangilik')
            if not base:
                base = f'yangilik-{self.pk or "new"}'
            slug = base
            n = 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class CorporateCategory(models.Model):
    """Korporativ hujjatlar kategoriyasi (Ustav, Qarorlar, va h.k.)"""
    name_uz = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (RU)")
    name_en = models.CharField(max_length=200, blank=True, verbose_name="Name (EN)")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL (slug)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Korporativ kategoriya"
        verbose_name_plural = "Korporativ kategoriyalar"
        ordering = ['order']

    def __str__(self):
        return self.name_uz

    def name(self, lang='uz'):
        val = getattr(self, f'name_{lang}', '')
        return val if val else self.name_uz

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.name_uz[:80])
            if not base:
                base = f'category-{self.pk or "new"}'
            slug = base
            n = 1
            while CorporateCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class CorporateDocument(models.Model):
    """Korporativ hujjat"""
    ARCHIVE_YEAR = 0  # Arxiv uchun maxsus qiymat

    category = models.ForeignKey(
        CorporateCategory,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Kategoriya"
    )
    title_uz = models.CharField(max_length=300, verbose_name="Sarlavha (UZ)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (RU)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Title (EN)")

    file = models.FileField(upload_to='corporate_docs/', verbose_name="Fayl (PDF/DOC)")
    year = models.PositiveIntegerField(
        default=2026,
        verbose_name="Yil (0 = Arxiv)"
    )
    is_archive = models.BooleanField(default=False, verbose_name="Arxivda")
    published_date = models.DateField(default=timezone.now, verbose_name="Sana")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Korporativ hujjat"
        verbose_name_plural = "Korporativ hujjatlar"
        ordering = ['order', '-published_date']

    def __str__(self):
        return f"{self.category.name_uz} — {self.title_uz} ({self.display_year})"

    @property
    def display_year(self):
        if self.is_archive:
            return "Arxiv"
        return str(self.year)

    def title(self, lang='uz'):
        val = getattr(self, f'title_{lang}', '')
        return val if val else self.title_uz

    def file_extension(self):
        import os
        if self.file:
            _, ext = os.path.splitext(self.file.name)
            return ext.lower().strip('.')
        return ''


class ContactMessage(models.Model):
    """Aloqa formasi xabarlari"""
    name = models.CharField(max_length=150, verbose_name="Ism")
    phone = models.CharField(max_length=50, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    message = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")

    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Aloqa xabarlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.phone}"


class Partner(models.Model):
    """Bizning hamkorlarimiz"""
    name = models.CharField(max_length=200, verbose_name="Hamkor nomi")
    image = models.FileField(
        upload_to='partners/',
        validators=[validate_svg_or_image],
        verbose_name="Logotip (Rasm yoki SVG)"
    )
    link = models.URLField(blank=True, verbose_name="Saytga havola")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

