import os
import django
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from django.core.files.base import ContentFile
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import CatalogItem, Service

BASE_URL = 'https://uzenergotaminlash.uz'

def get_menu_structure(lang):
    print(f"[{lang.upper()}] Menyular o'qilmoqda...")
    url = f"{BASE_URL}/{lang}/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    xizmatlar_dropdown = None
    for a in soup.find_all('a', class_='nav-link dropdown-toggle'):
        if 'XIZMATLAR' in a.text.upper() or 'УСЛУГИ' in a.text.upper() or 'SERVICES' in a.text.upper():
            xizmatlar_dropdown = a.find_next_sibling('ul')
            break
            
    if not xizmatlar_dropdown:
        print(f"[{lang.upper()}] Xizmatlar menyusi topilmadi!")
        return []

    categories = []
    # Fetch top level categories inside Xizmatlar
    for li in xizmatlar_dropdown.find_all('li', recursive=False):
        parent_a = li.find('a', class_='dropdown-item dropdown-toggle')
        if parent_a:
            cat_name = parent_a.text.strip()
            parent_href = parent_a.get('href', '')
            sub_items = []
            ul = li.find('ul', class_='dropdown-menu')
            if ul:
                for sub_a in ul.find_all('a'):
                    sub_name = sub_a.text.strip()
                    sub_href = sub_a.get('href', '#')
                    if sub_href == '#':
                        # Append sub_name as fragment to make the url unique for caching and distinct image seeding
                        # Using a URL-safe version of sub_name or just string is fine since it's just for local tracking
                        import urllib.parse
                        safe_name = urllib.parse.quote(sub_name)
                        sub_href = f"{parent_href}#{safe_name}"
                    sub_items.append({'name': sub_name, 'href': sub_href})
            categories.append({
                'name': cat_name,
                'sub_items': sub_items
            })
    return categories

def get_clean_desc(desc, max_len=180):
    import re
    if not desc: return ''
    sentences = re.split(r'(?<=[.!?]) +', desc)
    res = ''
    for s in sentences:
        if len(res) + len(s) <= max_len:
            res += (s + ' ')
        else:
            if not res:
                res = s[:max_len].rsplit(' ', 1)[0] + '.'
            break
    return res.strip()

SERVICE_IMAGE_KEYWORDS = {
    "Umumiy foydalanish omborlari": "warehouse,racks",
    "Bojxona ombori": "customs,warehouse,secure",
    "Bojxona rasmiylashtiruvi": "documents,stamp,office",
    "Import": "cargo,ship,port",
    "Eksport": "export,freight,plane",
    "Vaqtinchalik saqlash": "storage,boxes,pallets",
    "Deklaratsiya": "contract,signature,desk",
    "Sertifikat": "certificate,seal,quality",
    "Ruxsatnomalar": "business,permit,document",
    "Yuk tushirish-ortish va tashish xizmatlari": "forklift,loading,truck",
    "Omborlar elektr ta'minoti bilan ta'minlangan, 24/7 monitoring, qo'riqlash xizmati mavjud": "hightech,warehouse,lighting",
    "O'rta va yirik hajmdagi yuk tashish xizmatlari": "convoy,trucks,highway",
    "Avtokran": "crane,truck,heavy",
    "Tezkor yetkazish": "express,delivery,van",
    "Xavfsiz tashuv": "armored,truck,secure"
}

SERVICE_DESCRIPTIONS = {
    "Umumiy foydalanish omborlari": {
        "uz": "Sizning mahsulotlaringizni xavfsiz va ishonchli saqlash uchun mo'ljallangan zamonaviy, barcha qulayliklarga ega omborlarimiz xizmat ko'rsatadi.",
        "ru": "Наши современные склады со всеми удобствами предназначены для безопасного и надежного хранения вашей продукции.",
        "en": "Our modern warehouses with all amenities are designed for the safe and reliable storage of your products."
    },
    "Bojxona ombori": {
        "uz": "Bojxona nazorati ostidagi tovarlarni vaqtinchalik va uzoq muddatli saqlash uchun maxsus bojxona hududiga ega omborlar.",
        "ru": "Склады со специальной таможенной зоной для временного и долгосрочного хранения товаров под таможенным контролем.",
        "en": "Warehouses with a special customs zone for temporary and long-term storage of goods under customs control."
    },
    "Bojxona rasmiylashtiruvi": {
        "uz": "Eksport va import operatsiyalari uchun barcha zaruriy hujjatlarni tezkor va qonuniy rasmiylashtirish xizmatlari.",
        "ru": "Услуги по быстрому и законному оформлению всех необходимых документов для экспортных и импортных операций.",
        "en": "Services for the quick and legal processing of all necessary documents for export and import operations."
    },
    "Import": {
        "uz": "Xorijiy mamlakatlardan tovarlarni O'zbekiston hududiga olib kirish va ularni to'liq nazorat qilish xizmati.",
        "ru": "Услуги по ввозу товаров из зарубежных стран на территорию Узбекистана и их полный контроль.",
        "en": "Services for the import of goods from foreign countries into the territory of Uzbekistan and their full control."
    },
    "Eksport": {
        "uz": "Mahalliy mahsulotlarni xalqaro bozorlarga muvaffaqiyatli yetkazib berish va eksport jarayonlarini boshqarish.",
        "ru": "Успешная поставка местной продукции на международные рынки и управление экспортными процессами.",
        "en": "Successful delivery of local products to international markets and management of export processes."
    },
    "Vaqtinchalik saqlash": {
        "uz": "Yuklaringizni manzildan manzilga yetib borguncha ishonchli va xavfsiz sharoitlarda vaqtinchalik saqlash xizmatlari.",
        "ru": "Услуги по временному хранению ваших грузов в надежных и безопасных условиях до прибытия в пункт назначения.",
        "en": "Temporary storage services for your cargo in reliable and safe conditions until it reaches its destination."
    },
    "Deklaratsiya": {
        "uz": "Bojxona deklaratsiyalarini professional mutaxassislar orqali tez, to'g'ri va xatosiz to'ldirish xizmati.",
        "ru": "Услуги по быстрому, правильному и безошибочному заполнению таможенных деклараций через профессионалов.",
        "en": "Services for fast, correct, and error-free completion of customs declarations by professional specialists."
    },
    "Sertifikat": {
        "uz": "Mahsulotlarning sifati va xavfsizligini tasdiqlovchi barcha turdagi ruxsatnoma va sertifikatlarni olishda ko'maklashish.",
        "ru": "Помощь в получении всех видов разрешений и сертификатов, подтверждающих качество и безопасность продукции.",
        "en": "Assistance in obtaining all types of permits and certificates confirming the quality and safety of products."
    },
    "Ruxsatnomalar": {
        "uz": "Tashqi iqtisodiy faoliyatni amalga oshirish uchun davlat idoralaridan tegishli litsenziya va ruxsatnomalarni yig'ish.",
        "ru": "Сбор соответствующих лицензий и разрешений от государственных органов для осуществления ВЭД.",
        "en": "Gathering appropriate licenses and permits from state bodies to carry out foreign economic activities."
    },
    "Yuk tushirish-ortish va tashish xizmatlari": {
        "uz": "Zamonaviy texnikalar yordamida yuklarni og'irlik va o'lchamiga qarab xavfsiz tushirish hamda ortish.",
        "ru": "Безопасная разгрузка и погрузка грузов в зависимости от их веса и габаритов с помощью современной техники.",
        "en": "Safe unloading and loading of cargo depending on their weight and dimensions using modern equipment."
    },
    "Omborlar elektr ta'minoti bilan ta'minlangan, 24/7 monitoring, qo'riqlash xizmati mavjud": {
        "uz": "G узluksiz elektr energiyasi, 24/7 video nazorat va kuchaytirilgan qo'riqlash tizimi orqali mutlaq xavfsizlik.",
        "ru": "Бесперебойное электроснабжение, круглосуточное видеонаблюдение и усиленная система охраны.",
        "en": "Uninterrupted power supply, 24/7 video surveillance, and an enhanced security system."
    },
    "O'rta va yirik hajmdagi yuk tashish xizmatlari": {
        "uz": "Katta va og'ir hajmdagi sanoat yuklarini maxsus transport vositalari orqali ishonchli manzilga yetkazish.",
        "ru": "Надежная доставка крупногабаритных и тяжеловесных промышленных грузов спецтранспортом к месту назначения.",
        "en": "Reliable delivery of large and heavy industrial cargo to the destination via special vehicles."
    },
    "Avtokran": {
        "uz": "Og'ir va yirik uskunalarni balandlikka ko'tarish hamda joylashtirish uchun zamonaviy va kuchli avtokranlar ijarasi.",
        "ru": "Аренда современных и мощных автокранов для подъема и размещения тяжелого и крупногабаритного оборудования.",
        "en": "Rental of modern and powerful truck cranes for lifting and placing heavy and large equipment."
    },
    "Tezkor yetkazish": {
        "uz": "Shoshilinch yuklaringizni butun mamlakat bo'ylab eng qisqa vaqt ichida, xavfsiz va operativ yetkazib berish xizmati.",
        "ru": "Служба безопасной и оперативной доставки ваших срочных грузов по всей стране в кратчайшие сроки.",
        "en": "Safe and operational delivery service for your urgent cargo across the country in the shortest possible time."
    },
    "Xavfsiz tashuv": {
        "uz": "Nozik va qimmatbaho uskunalarni tashish jarayonida ularning to'liq xavfsizligi va butunligini kafolatlaymiz.",
        "ru": "В процессе транспортировки хрупкого и дорогостоящего оборудования мы гарантируем его полную сохранность.",
        "en": "In the process of transporting delicate and expensive equipment, we guarantee its complete safety."
    }
}

def fetch_details(url, sub_name='', lang='uz'):
    if not url or url == '#':
        return {'desc': '', 'img_url': None}
        
    # Agar xizmat bo'lsa va lug'atda bor bo'lsa, o'zimizning noyob izohni qaytaramiz (saytda bir xil bo'lgani uchun)
    if sub_name in SERVICE_DESCRIPTIONS:
        desc = SERVICE_DESCRIPTIONS[sub_name].get(lang, SERVICE_DESCRIPTIONS[sub_name]['uz'])
    else:
        desc = ''
        
    full_url = urljoin(BASE_URL, url)
    try:
        r = requests.get(full_url, verify=False, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Extract description from <p> tags in the main content if we don't have a predefined one
        if not desc:
            content = soup.find('div', class_='page-content') or soup.find('main') or soup.find('div', class_='container')
            if content:
                ps = content.find_all('p')
                desc = ' '.join([p.text.strip() for p in ps if p.text.strip()])
                desc = get_clean_desc(desc)
            
        # Extract image only from the main content to avoid navbar logos
        img_url = None
        if content:
            for img in content.find_all('img'):
                src = img.get('src', '')
                if src and 'logo' not in src.lower():
                    img_url = urljoin(BASE_URL, src)
                    break
                    
        # Agar rasm topilmasa va bu XIZMAT bo'lsa (lug'atda bor bo'lsa), noyob rasm olamiz
        if (not img_url or 'image2' in img_url or 'image3' in img_url) and sub_name in SERVICE_DESCRIPTIONS:
            seed = abs(hash(sub_name)) % 10000
            keyword = SERVICE_IMAGE_KEYWORDS.get(sub_name, 'industry,logistics')
            img_url = f'https://loremflickr.com/800/600/{keyword}?random={seed}'
                
        return {'desc': desc, 'img_url': img_url}
    except Exception as e:
        print(f"[{url}] Sahifa yuklashda xatolik: {e}")
        return {'desc': '', 'img_url': None}

def download_image(url):
    if not url: return None
    try:
        r = requests.get(url, verify=False, timeout=10)
        if r.status_code == 200:
            return r.content
    except Exception as e:
        pass
    return None

def main():
    print("Bazani tozalash...")
    CatalogItem.objects.all().delete()
    Service.objects.all().delete()
    print("Baza tozalandi.")

    langs = ['uz', 'ru', 'en']
    menu_data = {}
    
    # 1. Barcha tillar bo'yicha menyu strukturasini olish
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(get_menu_structure, lang): lang for lang in langs}
        for f in futures:
            lang = futures[f]
            menu_data[lang] = f.result()

    uz_cats = menu_data.get('uz', [])
    ru_cats = menu_data.get('ru', [])
    en_cats = menu_data.get('en', [])
    
    if not uz_cats:
        print("Menyular topilmadi.")
        return
    
    # Barcha detallarni parallel yuklash uchun ro'yxat tayyorlash
    urls_to_fetch = []
    
    for cat_idx in range(len(uz_cats)):
        uz_cat = uz_cats[cat_idx]
        ru_cat = ru_cats[cat_idx] if cat_idx < len(ru_cats) else uz_cat
        en_cat = en_cats[cat_idx] if cat_idx < len(en_cats) else uz_cat
        
        for sub_idx in range(len(uz_cat['sub_items'])):
            uz_sub = uz_cat['sub_items'][sub_idx]
            ru_sub = ru_cat['sub_items'][sub_idx] if sub_idx < len(ru_cat['sub_items']) else uz_sub
            en_sub = en_cat['sub_items'][sub_idx] if sub_idx < len(en_cat['sub_items']) else uz_sub
            
            ref_name = uz_sub['name'] # Always use UZ name for dictionary lookups
            if uz_sub['href'] != '#':
                urls_to_fetch.append({'lang': 'uz', 'url': uz_sub['href'], 'ref_name': ref_name})
            if ru_sub['href'] != '#':
                urls_to_fetch.append({'lang': 'ru', 'url': ru_sub['href'], 'ref_name': ref_name})
            if en_sub['href'] != '#':
                urls_to_fetch.append({'lang': 'en', 'url': en_sub['href'], 'ref_name': ref_name})
                
    print(f"Jami {len(urls_to_fetch)} ta sahifadan (3 tilda) qo'shimcha ma'lumot yuklab olinmoqda...")
    details_cache = {}
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(fetch_details, item['url'], item['ref_name'], item['lang']): (item['lang'], item['url']) for item in urls_to_fetch}
        for f in futures:
            lang, url = futures[f]
            details_cache[(lang, url)] = f.result()
            
    print("Rasmlar yuklanmoqda...")
    img_urls = {details_cache[(lang, url)]['img_url'] for lang, url in details_cache if details_cache[(lang, url)]['img_url']}
    img_cache = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_image, img_url): img_url for img_url in img_urls}
        for f in futures:
            img_url = futures[f]
            img_cache[img_url] = f.result()
            
    catalog_order = 1
    service_order = 1
    
    # 2. Ma'lumotlarni bazaga saqlash
    for cat_idx in range(len(uz_cats)):
        uz_cat = uz_cats[cat_idx]
        ru_cat = ru_cats[cat_idx] if cat_idx < len(ru_cats) else uz_cat
        en_cat = en_cats[cat_idx] if cat_idx < len(en_cats) else uz_cat
        
        is_catalog = cat_idx < 6
        
        for sub_idx in range(len(uz_cat['sub_items'])):
            uz_sub = uz_cat['sub_items'][sub_idx]
            ru_sub = ru_cat['sub_items'][sub_idx] if sub_idx < len(ru_cat['sub_items']) else uz_sub
            en_sub = en_cat['sub_items'][sub_idx] if sub_idx < len(en_cat['sub_items']) else uz_sub
            
            uz_details = details_cache.get(('uz', uz_sub['href']), {'desc': '', 'img_url': None})
            ru_details = details_cache.get(('ru', ru_sub['href']), {'desc': '', 'img_url': None})
            en_details = details_cache.get(('en', en_sub['href']), {'desc': '', 'img_url': None})
            
            img_url = uz_details['img_url']
            img_content = img_cache.get(img_url) if img_url else None
            filename = f"image_{cat_idx}_{sub_idx}.jpeg" if img_url else None
            
            if is_catalog:
                obj = CatalogItem(
                    name_uz=uz_sub['name'],
                    name_ru=ru_sub['name'],
                    name_en=en_sub['name'],
                    description_uz=uz_details['desc'],
                    description_ru=ru_details['desc'] if ru_details['desc'] else uz_details['desc'],
                    description_en=en_details['desc'] if en_details['desc'] else uz_details['desc'],
                    order=catalog_order,
                    is_active=True
                )
                if img_content and filename:
                    obj.image.save(filename, ContentFile(img_content), save=False)
                obj.save()
                catalog_order += 1
                print(f"Katalog: {uz_sub['name']} saqlandi.")
            else:
                obj = Service(
                    name_uz=uz_sub['name'],
                    name_ru=ru_sub['name'],
                    name_en=en_sub['name'],
                    description_uz=uz_details['desc'],
                    description_ru=ru_details['desc'] if ru_details['desc'] else uz_details['desc'],
                    description_en=en_details['desc'] if en_details['desc'] else uz_details['desc'],
                    order=service_order,
                    icon='bi-check-circle',
                    is_active=True
                )
                if img_content and filename:
                    obj.image.save(filename, ContentFile(img_content), save=False)
                obj.save()
                service_order += 1
                print(f"Xizmat: {uz_sub['name']} saqlandi.")

    print(f"Tugadi! Katalog: {catalog_order-1}, Xizmatlar: {service_order-1}")

if __name__ == '__main__':
    main()
