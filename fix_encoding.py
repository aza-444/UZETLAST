# -*- coding: utf-8 -*-
import re
from pathlib import Path

path = Path("templates/main/index.html")
text = path.read_text(encoding="utf-8")

# Stats section: uncomment
stats_block = """<!-- ===================== STATS ===================== -->
<!--{% if about %}-->
<!--<section class="stats-section">-->
<!--  <div class="container">-->
<!--    <div class="stats-grid">-->
<!--      <div class="stat-card" data-aos="fade-up" data-aos-delay="0">-->
<!--        <div class="stat-icon"><i class="bi bi-calendar-check"></i></div>-->
<!--        <div class="stat-number counter" data-target="{{ about.years_experience }}">0</div>-->
<!--        <div class="stat-label">-->
<!--          {% if lang == 'uz' %}Yillik tajriba{% elif lang == 'ru' %}Лет опыта{% else %}Years Experience{% endif %}-->
<!--        </div>-->
<!--      </div>-->
<!--      <div class="stat-card" data-aos="fade-up" data-aos-delay="100">-->
<!--        <div class="stat-icon"><i class="bi bi-people-fill"></i></div>-->
<!--        <div class="stat-number counter" data-target="{{ about.clients_count }}">0</div>-->
<!--        <div class="stat-label">-->
<!--          {% if lang == 'uz' %}Mijozlar{% elif lang == 'ru' %}Клиенты{% else %}Clients{% endif %}-->
<!--        </div>-->
<!--      </div>-->
<!--      <div class="stat-card" data-aos="fade-up" data-aos-delay="200">-->
<!--        <div class="stat-icon"><i class="bi bi-check-circle-fill"></i></div>-->
<!--        <div class="stat-number counter" data-target="{{ about.projects_count }}">0</div>-->
<!--        <div class="stat-label">-->
<!--          {% if lang == 'uz' %}Loyihalar{% elif lang == 'ru' %}Проекты{% else %}Projects{% endif %}-->
<!--        </div>-->
<!--      </div>-->
<!--      <div class="stat-card" data-aos="fade-up" data-aos-delay="300">-->
<!--        <div class="stat-icon"><i class="bi bi-globe2"></i></div>-->
<!--        <div class="stat-number">24/7</div>-->
<!--        <div class="stat-label">-->
<!--          {% if lang == 'uz' %}Qo'llab-quvvatlash{% elif lang == 'ru' %}"""

# Find stats section and replace with uncommented version using regex
stats_pattern = r"<!-- ===================== STATS ===================== -->.*?<!--{% endif %}-->"
stats_replacement = """<!-- ===================== STATS ===================== -->
{% if about %}
<section class="stats-section">
  <div class="container">
    <div class="stats-grid">
      <div class="stat-card" data-aos="fade-up" data-aos-delay="0">
        <div class="stat-icon"><i class="bi bi-calendar-check"></i></div>
        <div class="stat-number counter" data-target="{{ about.years_experience }}">0</div>
        <div class="stat-label">
          {% if lang == 'uz' %}Yillik tajriba{% elif lang == 'ru' %}Лет опыта{% else %}Years Experience{% endif %}
        </div>
      </div>
      <div class="stat-card" data-aos="fade-up" data-aos-delay="100">
        <div class="stat-icon"><i class="bi bi-people-fill"></i></div>
        <div class="stat-number counter" data-target="{{ about.clients_count }}">0</div>
        <div class="stat-label">
          {% if lang == 'uz' %}Mijozlar{% elif lang == 'ru' %}Клиенты{% else %}Clients{% endif %}
        </div>
      </div>
      <div class="stat-card" data-aos="fade-up" data-aos-delay="200">
        <div class="stat-icon"><i class="bi bi-check-circle-fill"></i></div>
        <div class="stat-number counter" data-target="{{ about.projects_count }}">0</div>
        <div class="stat-label">
          {% if lang == 'uz' %}Loyihalar{% elif lang == 'ru' %}Проекты{% else %}Projects{% endif %}
        </div>
      </div>
      <div class="stat-card" data-aos="fade-up" data-aos-delay="300">
        <div class="stat-icon"><i class="bi bi-globe2"></i></div>
        <div class="stat-number">24/7</div>
        <div class="stat-label">
          {% if lang == 'uz' %}Qo'llab-quvvatlash{% elif lang == 'ru' %}Поддержка{% else %}Support{% endif %}
        </div>
      </div>
    </div>
  </div>
</section>
{% endif %}"""

text, n = re.subn(stats_pattern, stats_replacement, text, flags=re.DOTALL)
print(f"Stats section: {n} replacement(s)")

# Fix mojibake by detecting lines containing typical mojibake chars
def fix_ru_context(text, uz_marker, correct_ru, else_marker):
    """Fix {% elif lang == 'ru' %}MOJIBAKE{% else %}ELSE{% endif %} patterns"""
    pattern = (
        rf"({re.escape(uz_marker)}\{{% elif lang == 'ru' %}})"
        rf"[^\{{%]*?"
        rf"(\{{% else %}}{re.escape(else_marker)}\{{% endif %}})"
    )
    repl = rf"\1{correct_ru}\2"
    new_text, count = re.subn(pattern, repl, text)
    if count:
        print(f"Fixed {count}x: {correct_ru[:40]}...")
    return new_text

fixes = [
    ("{% if lang == 'uz' %}Keng assortimentli energetika uskunalari", "Широкий ассортимент энергетического оборудования", "Wide range of energy equipment"),
    ("{% if lang == 'uz' %}Admin paneldan xizmatlar qo'shing", "Добавьте услуги из админ панели", "Add services from admin panel"),
    ("{% if lang == 'uz' %}Admin paneldan hamkorlarni qo'shing", "Добавьте партнёров из админ панели", "Add partners from the admin panel"),
    ("{% if lang == 'uz' %}Biz bilan bog'laning", "Свяжитесь с нами", "Contact Us"),
    ("{% if lang == 'uz' %}Ismingiz", "Ваше имя", "Your Name"),
    ("{% if lang == 'uz' %}Xabar yuborildi! Tez orada bog'lanamiz.", "Сообщение отправлено! Свяжемся с вами скоро.", "Message sent! We'll contact you soon."),
    ("{% if lang == 'uz' %}Xizmatlar", "Услуги", "Services"),
    ("{% if lang == 'uz' %}Kompaniya xizmatlari", "Услуги компании", "Company services"),
    ("{% if lang == 'uz' %}Kompaniya", "Компания", "Company"),
    ("{% if lang == 'uz' %}Biz haqimizda", "О нас", "About us"),
    ("{% if lang == 'uz' %}harakat", "навигация", "navigate"),
    ("{% if lang == 'uz' %}o'tish", "перейти", "go"),
    ("{% if lang == 'uz' %}yopish", "закрыть", "close"),
]

for uz, ru, else_val in fixes:
    text = fix_ru_context(text, uz, ru, else_val)

# Placeholder fix
text, n = re.subn(
    r'placeholder="\{% if lang == \'uz\' \}Ism Familiya\{% elif lang == \'ru\' \}[^"]*\{% else %\}Full Name\{% endif %\}"',
    'placeholder="{% if lang == \'uz\' %}Ism Familiya{% elif lang == \'ru\' %}Имя Фамилия{% else %}Full Name{% endif %}"',
    text
)
print(f"Placeholder: {n} replacement(s)")

# Footer ru company name
text, n = re.subn(
    r"\{% if lang == 'ru' %\}\s*[^\n]*O'ZENERGOTA'MINLASH",
    "{% if lang == 'ru' %}\n               АО O'ZENERGOTA'MINLASH",
    text
)
print(f"Footer company name: {n} replacement(s)")

# Footer description for ru
text, n = re.subn(
    r"\{% elif lang == 'ru' %\}[^\{%]*\{% else %\}Reliable partner for energy equipment supply in Uzbekistan\{% endif %\}",
    "{% elif lang == 'ru' %}Надёжный партнёр по поставке энергетического оборудования в Узбекистане{% else %}Reliable partner for energy equipment supply in Uzbekistan{% endif %}",
    text
)
print(f"Footer description: {n} replacement(s)")

# Search modal aria-label
text, n = re.subn(
    r'aria-label="\{% if lang == \'uz\' \}Qidiruv\{% elif lang == \'ru\' \}[^"]*\{% else %\}Search\{% endif %\}"',
    'aria-label="{% if lang == \'uz\' %}Qidiruv{% elif lang == \'ru\' %}Поиск{% else %}Search{% endif %}"',
    text
)
print(f"Search aria-label: {n} replacement(s)")

# Search footer kbd arrows
text, n = re.subn(
    r'<kbd>[^<]*</kbd><kbd>[^<]*</kbd> \{% if lang == \'uz\' %\}harakat',
    '<kbd>↑</kbd><kbd>↓</kbd> {% if lang == \'uz\' %}harakat',
    text
)
print(f"Search kbd arrows: {n} replacement(s)")

# Partner link and name classes
text = text.replace(
    'style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;text-decoration:none;"',
    'class="partner-card-link"'
)
text = text.replace('<strong style="color:#333;">', '<strong class="partner-name-fallback">')

# Contact map inline style removal
text = text.replace(
    '<div id="xarita" class="contact-map" data-aos="fade-up" style="margin-top: 40px; border-radius: 12px; overflow: hidden; height: 400px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">\n      <style>\n        .contact-map iframe { width: 100% !important; height: 100% !important; border: 0 !important; }\n      </style>',
    '<div id="xarita" class="contact-map" data-aos="fade-up">'
)

path.write_text(text, encoding="utf-8", newline="\n")
print("File saved as UTF-8")

# Verify no mojibake left
remaining = [i+1 for i, line in enumerate(text.splitlines()) if 'Р ' in line or 'РЎ' in line or 'вЂ' in line or 'РІ' in line]
print(f"Lines with possible mojibake: {remaining}")
