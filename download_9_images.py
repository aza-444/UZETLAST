import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Service

# Data to update for the remaining 9 services with image keywords
services_data = [
    {
        'name_uz': "Deklaratsiya",
        'keyword': "document,customs"
    },
    {
        'name_uz': "Sertifikat",
        'keyword': "certificate,quality"
    },
    {
        'name_uz': "Ruxsatnomalar",
        'keyword': "license,business"
    },
    {
        'name_uz': "Yuk tushirish-ortish va tashish xizmatlari",
        'keyword': "forklift,loading"
    },
    {
        'name_uz': "Omborlar elektr ta'minoti bilan ta'minlangan, 24/7 monitoring, qo'riqlash xizmati mavjud",
        'keyword': "security,camera"
    },
    {
        'name_uz': "O'rta va yirik hajmdagi yuk tashish xizmatlari",
        'keyword': "truck,highway"
    },
    {
        'name_uz': "Avtokran",
        'keyword': "crane,construction"
    },
    {
        'name_uz': "Tezkor yetkazish",
        'keyword': "delivery,van"
    },
    {
        'name_uz': "Xavfsiz tashuv",
        'keyword': "safe,transport"
    }
]

def run():
    print("Qolgan 9 ta xizmatlar uchun rasm yuklanmoqda...")
    for data in services_data:
        try:
            service = Service.objects.get(name_uz=data['name_uz'])
            
            # Yuklash uchun URL
            url = f"https://loremflickr.com/800/600/{data['keyword']}?random=1"
            print(f"{data['name_uz']} uchun rasm yuklanmoqda ({url})...")
            
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                filename = f"{data['name_uz'].replace(' ', '_').lower()}.jpg"
                service.image.save(filename, ContentFile(response.content), save=True)
                print(f"Muvaffaqiyatli saqlandi: {data['name_uz']}")
            else:
                print(f"Xatolik: {data['name_uz']} (Status code: {response.status_code})")
                
        except Service.DoesNotExist:
            print(f"Topilmadi: {data['name_uz']}")
        except Exception as e:
            print(f"Xatolik: {data['name_uz']} - {e}")
            
    print("Tugadi.")

if __name__ == '__main__':
    run()
