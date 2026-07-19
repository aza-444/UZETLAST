import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Service, HeroSection

def run():
    print("Populating Services...")
    # Warehouse Service
    Service.objects.update_or_create(
        name_uz="Ombor ijarasi va xizmatlari",
        defaults={
            "description_uz": "Ombor katalogi — kompaniyamiz omborlarida mavjud bo'lgan barcha uskunalar, ehtiyot qismlar va materiallarning to'liq ro'yxati. Ushbu bo'limda siz energetika sohasida ishlatiladigan turli xil mahsulotlarni ko'rishingiz mumkin.",
            "name_ru": "Аренда склада и услуги",
            "description_ru": "Каталог склада — полный список оборудования, запасных частей и материалов, имеющихся на наших складах.",
            "name_en": "Warehouse Rental & Services",
            "description_en": "Warehouse catalog — a complete list of equipment, spare parts, and materials available in our warehouses.",
            "icon": "bi-box-seam",
            "order": 1
        }
    )

    # Transport Service
    Service.objects.update_or_create(
        name_uz="Transport xizmati",
        defaults={
            "description_uz": "Transport katalogi — kompaniyamiz balansidagi transport vositalari va maxsus texnikalarning to'liq ro'yxati. Ushbu bo'limda yuk mashinalari, avtobus va boshqa transport vositalarini ko'rishingiz mumkin.",
            "name_ru": "Транспортные услуги",
            "description_ru": "Каталог транспорта — полный перечень транспортных средств и спецтехники на балансе нашей компании.",
            "name_en": "Transport Services",
            "description_en": "Transport catalog — a complete list of vehicles and special equipment on our company's balance sheet.",
            "icon": "bi-truck",
            "order": 2
        }
    )
    print("Services populated!")

    # Set generated hero image
    print("Setting Hero Background...")
    hero = HeroSection.objects.first()
    if not hero:
        hero = HeroSection.objects.create(
            title_uz="O'zenergota'minlash AJ",
            subtitle_uz="O'zbekistonda energetika uskunalari bo'yicha ishonchli hamkor",
            btn_catalog_uz="Katalog",
            btn_contact_uz="Bog'lanish"
        )
    
    img_path = "/home/aza/.gemini/antigravity/brain/1bbc7cbb-9f95-4118-a04f-7667a5153e1b/hero_background_energy_1783583176119.png"
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            hero.background_image.save('hero_bg_premium.png', File(f), save=True)
        print("Hero image updated successfully.")
    else:
        print("Hero image not found at path:", img_path)

if __name__ == "__main__":
    run()
