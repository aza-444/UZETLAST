import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Service

# Data to update for the remaining 9 services
services_data = [
    {
        'name_uz': "Deklaratsiya",
        'name_ru': "Декларация",
        'name_en': "Declaration",
        'desc_uz': "Bojxona deklaratsiyalarini professional mutaxassislar orqali tez, to'g'ri va xatosiz to'ldirish xizmati.",
        'desc_ru': "Услуги по быстрому, правильному и безошибочному заполнению таможенных деклараций через профессионалов.",
        'desc_en': "Services for fast, correct, and error-free completion of customs declarations by professional specialists."
    },
    {
        'name_uz': "Sertifikat",
        'name_ru': "Сертификат",
        'name_en': "Certificate",
        'desc_uz': "Mahsulotlarning sifati va xavfsizligini tasdiqlovchi barcha turdagi ruxsatnoma va sertifikatlarni olishda ko'maklashish.",
        'desc_ru': "Помощь в получении всех видов разрешений и сертификатов, подтверждающих качество и безопасность продукции.",
        'desc_en': "Assistance in obtaining all types of permits and certificates confirming the quality and safety of products."
    },
    {
        'name_uz': "Ruxsatnomalar",
        'name_ru': "Разрешения",
        'name_en': "Permits",
        'desc_uz': "Tashqi iqtisodiy faoliyatni amalga oshirish uchun davlat idoralaridan tegishli litsenziya va ruxsatnomalarni yig'ish.",
        'desc_ru': "Сбор соответствующих лицензий и разрешений от государственных органов для осуществления ВЭД.",
        'desc_en': "Gathering appropriate licenses and permits from state bodies to carry out foreign economic activities."
    },
    {
        'name_uz': "Yuk tushirish-ortish va tashish xizmatlari",
        'name_ru': "Погрузочно-разгрузочные работы",
        'name_en': "Loading and Unloading Services",
        'desc_uz': "Zamonaviy texnikalar yordamida yuklarni og'irlik va o'lchamiga qarab xavfsiz tushirish hamda ortish.",
        'desc_ru': "Безопасная разгрузка и погрузка грузов в зависимости от их веса и габаритов с помощью современной техники.",
        'desc_en': "Safe unloading and loading of cargo depending on their weight and dimensions using modern equipment."
    },
    {
        'name_uz': "Omborlar elektr ta'minoti bilan ta'minlangan, 24/7 monitoring, qo'riqlash xizmati mavjud",
        'name_ru': "Круглосуточный мониторинг и охрана",
        'name_en': "24/7 Security and Monitoring",
        'desc_uz': "Uzluksiz elektr energiyasi, 24/7 video nazorat va kuchaytirilgan qo'riqlash tizimi orqali mutlaq xavfsizlik.",
        'desc_ru': "Бесперебойное электроснабжение, круглосуточное видеонаблюдение и усиленная система охраны.",
        'desc_en': "Uninterrupted power supply, 24/7 video surveillance, and an enhanced security system."
    },
    {
        'name_uz': "O'rta va yirik hajmdagi yuk tashish xizmatlari",
        'name_ru': "Перевозка средних и крупных грузов",
        'name_en': "Medium and Large Cargo Transport",
        'desc_uz': "Katta va og'ir hajmdagi sanoat yuklarini maxsus transport vositalari orqali ishonchli manzilga yetkazish.",
        'desc_ru': "Надежная доставка крупногабаритных и тяжеловесных промышленных грузов спецтранспортом к месту назначения.",
        'desc_en': "Reliable delivery of large and heavy industrial cargo to the destination via special vehicles."
    },
    {
        'name_uz': "Avtokran",
        'name_ru': "Автокран",
        'name_en': "Truck Crane",
        'desc_uz': "Og'ir va yirik uskunalarni balandlikka ko'tarish hamda joylashtirish uchun zamonaviy va kuchli avtokranlar ijarasi.",
        'desc_ru': "Аренда современных и мощных автокранов для подъема и размещения тяжелого и крупногабаритного оборудования.",
        'desc_en': "Rental of modern and powerful truck cranes for lifting and placing heavy and large equipment."
    },
    {
        'name_uz': "Tezkor yetkazish",
        'name_ru': "Экспресс доставка",
        'name_en': "Express Delivery",
        'desc_uz': "Shoshilinch yuklaringizni butun mamlakat bo'ylab eng qisqa vaqt ichida, xavfsiz va operativ yetkazib berish xizmati.",
        'desc_ru': "Служба безопасной и оперативной доставки ваших срочных грузов по всей стране в кратчайшие сроки.",
        'desc_en': "Safe and operational delivery service for your urgent cargo across the country in the shortest possible time."
    },
    {
        'name_uz': "Xavfsiz tashuv",
        'name_ru': "Безопасная перевозка",
        'name_en': "Safe Transportation",
        'desc_uz': "Nozik va qimmatbaho uskunalarni tashish jarayonida ularning to'liq xavfsizligi va butunligini kafolatlaymiz.",
        'desc_ru': "В процессе транспортировки хрупкого и дорогостоящего оборудования мы гарантируем его полную сохранность.",
        'desc_en': "In the process of transporting delicate and expensive equipment, we guarantee its complete safety."
    }
]

def run():
    print("Qolgan 9 ta xizmatlar yangilanmoqda...")
    for data in services_data:
        try:
            service = Service.objects.get(name_uz=data['name_uz'])
            service.name_ru = data['name_ru']
            service.name_en = data['name_en']
            service.description_uz = data['desc_uz']
            service.description_ru = data['desc_ru']
            service.description_en = data['desc_en']
            
            # Note: Not updating images because the AI quota was exceeded.
            
            service.save()
            print(f"Muvaffaqiyatli yangilandi: {data['name_uz']}")
        except Service.DoesNotExist:
            print(f"Topilmadi: {data['name_uz']}")
            
    print("Tugadi.")

if __name__ == '__main__':
    run()
