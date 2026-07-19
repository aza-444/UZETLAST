import os
import django
import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import CatalogItem, Service

BASE_URL = 'https://uzenergotaminlash.uz'

def fetch_lang_data(lang):
    print(f"[{lang.upper()}] Sahifa yuklanmoqda...")
    url = f"{BASE_URL}/{lang}/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    cards = soup.find_all('div', class_='catalog-banner-card')
    
    data = []
    for card in cards:
        # Title can be in h5 or h3
        title_elem = card.find('h5') or card.find('h3')
        title = title_elem.text.strip() if title_elem else ''
        
        # Description in p
        p_elem = card.find('p')
        desc = p_elem.text.strip() if p_elem else ''
        
        # Image in style
        style = card.get('style', '')
        m = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
        img_url = m.group(1) if m else None
        if img_url and not img_url.startswith('http'):
            img_url = urljoin(BASE_URL, img_url)
            
        data.append({
            'title': title,
            'desc': desc,
            'img_url': img_url
        })
    print(f"[{lang.upper()}] {len(data)} ta element topildi.")
    return lang, data

def download_image(url):
    if not url: return None
    print(f"Rasm yuklanmoqda: {url}")
    try:
        r = requests.get(url, verify=False, timeout=10)
        return r.content
    except Exception as e:
        print(f"Rasm yuklashda xatolik: {e}")
        return None

def main():
    langs = ['uz', 'ru', 'en']
    lang_results = {}
    
    # 1. Sahifalarni parallel yuklash
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_lang_data, lang) for lang in langs]
        for f in futures:
            lang, data = f.result()
            lang_results[lang] = data
            
    # Asos sifatida 'uz' olamiz
    uz_data = lang_results.get('uz', [])
    ru_data = lang_results.get('ru', [])
    en_data = lang_results.get('en', [])
    
    if len(uz_data) != 8:
        print(f"Kutilgan 8 ta o'rniga {len(uz_data)} ta topildi.")
        return

    # 2. Rasmlarni parallel yuklash
    img_urls = [item['img_url'] for item in uz_data]
    with ThreadPoolExecutor(max_workers=8) as executor:
        images_content = list(executor.map(download_image, img_urls))
        
    # 3. Bazaga saqlash
    # Dastlabki 6 tasi CatalogItem, qolgan 2 tasi Service
    print("Ma'lumotlar bazaga saqlanmoqda...")
    for i in range(8):
        uz = uz_data[i]
        ru = ru_data[i] if i < len(ru_data) else uz_data[i]
        en = en_data[i] if i < len(en_data) else uz_data[i]
        
        img_content = images_content[i]
        filename = uz['img_url'].split('/')[-1] if uz['img_url'] else f'image_{i}.png'
        
        if i < 6:
            # CatalogItem
            obj, created = CatalogItem.objects.update_or_create(
                name_uz=uz['title'],
                defaults={
                    'order': i+1,
                    'name_ru': ru['title'],
                    'name_en': en['title'],
                    'description_uz': uz['desc'],
                    'description_ru': ru['desc'],
                    'description_en': en['desc'],
                    'is_active': True
                }
            )
            if img_content:
                obj.image.save(filename, ContentFile(img_content), save=True)
            print(f"Katalogga saqlandi: {uz['title']}")
        else:
            # Service
            obj, created = Service.objects.update_or_create(
                name_uz=uz['title'],
                defaults={
                    'order': i+1,
                    'name_ru': ru['title'],
                    'name_en': en['title'],
                    'description_uz': uz['desc'],
                    'description_ru': ru['desc'],
                    'description_en': en['desc'],
                    'icon': 'bi-lightning' if i == 6 else 'bi-truck', # example icon
                    'is_active': True
                }
            )
            if img_content:
                obj.image.save(filename, ContentFile(img_content), save=True)
            print(f"Xizmatlarga saqlandi: {uz['title']}")

    print("Barcha ma'lumotlar muvaffaqiyatli saqlandi!")

if __name__ == '__main__':
    # urllib3 warninglarni o'chirish
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()
