"""
Seed script — run via: python3 seed_data.py
Idempotent: skips any record that already exists. Admin edits are never wiped.
Real content from uzenergotaminlash.uz
"""
import os
import sys
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import timezone
from main.models import SiteSettings, HeroSection, AboutSection, Service, CatalogItem, News

# ── SITE SETTINGS ──────────────────────────────────────────────────────────
if not SiteSettings.objects.exists():
    SiteSettings.objects.create(
        phone_1='+998 55 501 30 30',
        phone_2='+998 71 202 43 13',
        email='info@uzenergo.uz',
        address_uz="Toshkent shahar, Shayxontohur tumani, Navoiy ko'chasi 16",
        address_ru='г. Ташкент, Шайхантахурский р-н, ул. Навои 16',
        address_en='Tashkent city, Shaykhantakhur district, Navoiy str. 16',
        meta_title_uz="O'ZENERGOTA'MINLASH AJ — Energetika va sanoat korxonalariga ta'minot",
        meta_title_ru="O'ZENERGOTA'MINLASH AJ — Поставки для энергетики и промышленности",
        meta_title_en="UZBEKENERGO SUPPLY JSC — Energy & Industrial Supply",
        meta_description_uz=(
            "O'ZENERGOTA'MINLASH AJ — energetika va sanoat korxonalariga transformatorlar, "
            "generatorlar, armatura, elektr jihozlari, metall va kimyoviy mahsulotlarni yetkazib berish."
        ),
        meta_description_ru=(
            "O'ZENERGOTA'MINLASH AJ transformatorlar, generatorlar, armatura, "
            "elektr jihozlari, metall va kimyoviy materiallar yetkazib beradi."
        ),
        meta_description_en=(
            "UZBEKENERGO SUPPLY JSC delivers transformers, generators, valves, "
            "electrical equipment, metals and chemicals to energy enterprises in Uzbekistan."
        ),
        meta_keywords=(
            "uz uzet uzenergo uze energo taminlash elektr jihozlari "
            "transformator generator uzbekistan o'zenergota'minlash"
        ),
        telegram='https://t.me/uzenergo',
        instagram='https://instagram.com/uzenergo',
    )
    print('Site settings created')
else:
    print('Site settings: already exists, skipping')

# ── HERO ───────────────────────────────────────────────────────────────────
if not HeroSection.objects.exists():
    HeroSection.objects.create(
        title_uz="Energetika va sanoat korxonalariga ishonchli ta'minot xizmati",
        title_ru='Надёжные поставки для энергетики и промышленности',
        title_en='Reliable Supply Services for Energy and Industrial Sectors',
        subtitle_uz=(
            "Ehtiyot qismlar, uskunalar va materiallarni o'z vaqtida yetkazib berish "
            "— ishonchli va uzluksiz ta'minot yechimlar."
        ),
        subtitle_ru=(
            "Своевременная поставка запасных частей, оборудования и материалов "
            "— надёжные и бесперебойные решения."
        ),
        subtitle_en=(
            "Timely delivery of spare parts, equipment and materials "
            "— reliable, uninterrupted supply solutions."
        ),
        btn_catalog_uz='Katalog',
        btn_catalog_ru='Каталог',
        btn_catalog_en='Catalog',
        btn_contact_uz="Bog'lanish",
        btn_contact_ru='Связаться',
        btn_contact_en='Contact Us',
    )
    print('Hero created')
else:
    print('Hero: already exists, skipping')

# ── ABOUT ──────────────────────────────────────────────────────────────────
if not AboutSection.objects.exists():
    AboutSection.objects.create(
        title_uz="O'ZENERGOTA'MINLASH AJ haqida",
        title_ru="O'ZENERGOTA'MINLASH AJ haqida",
        title_en="About UZBEKENERGO SUPPLY JSC",
        content_uz=(
            "O'ZENERGOTA'MINLASH aksiyadorlik jamiyati O'zbekistondagi eng yirik energetika "
            "kompaniyalaridan biri hisoblanadi. Jamiyat energetika tarmog'i korxonalariga "
            "moddiy-texnik resurslar va uskunalarni o'z vaqtida va sifatli yetkazib berish "
            "orqali sohaning barqarorligini ta'minlaydi."
        ),
        content_ru=(
            "O'ZENERGOTA'MINLASH aksiyadorlik jamiyati O'zbekistondagi eng yirik energetika "
            "kompaniyalaridan biri hisoblanadi. Jamiyat energetika tarmog'i korxonalariga "
            "moddiy-texnik resurslar va uskunalarni o'z vaqtida va sifatli yetkazib berish "
            "orqali sohaning barqarorligini ta'minlaydi."
        ),
        content_en=(
            "UZBEKENERGO SUPPLY JSC is one of the largest energy companies in Uzbekistan. "
            "The company ensures industry stability by providing timely and high-quality "
            "supplies of material and technical resources and equipment to energy enterprises."
        ),
        mission_uz=(
            "Jamiyatning dinamik rivojlanishi, investitsiyaviy jozibadorligini oshirish "
            "va aksiyadorlar farovonligini ta'minlash."
        ),
        mission_ru=(
            "Jamiyatning dinamik rivojlanishi, investitsiyaviy jozibadorligini oshirish "
            "va aksiyadorlar farovonligini ta'minlash."
        ),
        mission_en=(
            "Dynamic development of the company, increasing its investment attractiveness "
            "and ensuring shareholder prosperity."
        ),
        vision_uz=(
            "Energetika tarmog'i korxonalariga moddiy-texnik resurslar va uskunalarni "
            "o'z vaqtida va sifatli yetkazib beruvchi yetakchi operator bo'lish."
        ),
        vision_ru=(
            "Energetika tarmog'i korxonalariga moddiy-texnik resurslar va uskunalarni "
            "o'z vaqtida va sifatli yetkazib beruvchi yetakchi operator bo'lish."
        ),
        vision_en=(
            "To become a leading operator for timely and high-quality MTP and equipment "
            "deliveries to energy enterprises."
        ),
        years_experience=30,
        clients_count=1200,
        projects_count=5000,
    )
    print('About created')
else:
    print('About: already exists, skipping')

# ── SERVICES — only seed if none exist ────────────────────────────────────
if Service.objects.exists():
    print('Services: already exist, skipping')
else:
    services = [
        {
            'name_uz': 'Energetika uskunalarini yetkazib berish',
            'name_ru': 'Поставка энергетического оборудования',
            'name_en': 'Energy Equipment Supply',
            'description_uz': (
                "Yuqori kuchlanishli transformatorlar, generatorlar, turbinalar va boshqa "
                "energetika uskunalari. Sifatli uskunalarni yetkazib berish orqali "
                "O'zbekiston energetika tarmog'ining barqaror ishlashini ta'minlaymiz."
            ),
            'description_ru': (
                "Высоковольтные трансформаторы, генераторы, турбины и другое "
                "энергетическое оборудование. Обеспечиваем стабильную работу "
                "энергосистемы Узбекистана."
            ),
            'description_en': (
                "High-voltage transformers, generators, turbines and other power equipment. "
                "We ensure stable operation of Uzbekistan's energy grid."
            ),
            'icon': 'bi-lightning-charge-fill',
            'order': 1,
        },
        {
            'name_uz': 'Armatura va mexanik qismlar',
            'name_ru': 'Арматура и механические части',
            'name_en': 'Valves & Mechanical Parts',
            'description_uz': (
                "Sanoat armaturasi, nasoslar va mexanik uzatmalar. Energetika korxonalari "
                "uchun ishonchli, yuqori sifatli mexanik uskunalarni yetkazib beramiz."
            ),
            'description_ru': (
                "Промышленная арматура, насосы и механические приводы. Поставляем "
                "надёжное высококачественное оборудование для энергопредприятий."
            ),
            'description_en': (
                "Industrial valves, pumps and mechanical drives. We supply reliable, "
                "high-quality mechanical equipment for energy enterprises."
            ),
            'icon': 'bi-gear-wide-connected',
            'order': 2,
        },
        {
            'name_uz': 'Elektr jihozlari',
            'name_ru': 'Электрооборудование',
            'name_en': 'Electrical Equipment',
            'description_uz': (
                "Kabel mahsulotlari, taqsimlash qutilar va avtomatika tizimlari. "
                "Energetika infratuzilmasini qo'llab-quvvatlash uchun zamonaviy "
                "elektr jihozlarini taklif etamiz."
            ),
            'description_ru': (
                "Кабельная продукция, распределительные щиты и системы автоматики. "
                "Современное электрооборудование для поддержки энергетической инфраструктуры."
            ),
            'description_en': (
                "Cable products, distribution boards and automation systems. "
                "Modern electrical equipment to support the energy infrastructure."
            ),
            'icon': 'bi-plug-fill',
            'order': 3,
        },
        {
            'name_uz': 'Metall mahsulotlar',
            'name_ru': 'Металлопродукция',
            'name_en': 'Metal Products',
            'description_uz': (
                "Prokat metall, quvurlar va maxsus qotishmalar. Elektr tarmoqlari va "
                "energetika inshootlari uchun sifatli metall materiallarni yetkazib beramiz."
            ),
            'description_ru': (
                "Прокат металла, трубы и специальные сплавы. Качественные металлические "
                "материалы для электросетей и энергообъектов."
            ),
            'description_en': (
                "Rolled metal, pipes and special alloys. Quality metal materials "
                "for power grids and energy facilities."
            ),
            'icon': 'bi-building-fill',
            'order': 4,
        },
        {
            'name_uz': 'Kimyoviy mahsulotlar',
            'name_ru': 'Химические продукты',
            'name_en': 'Chemical Products',
            'description_uz': (
                "Sanoat reagentlari, moylar va kimyoviy qo'shimchalar. Energetika "
                "korxonalarining uzluksiz ishlashi uchun zarur kimyoviy materiallar."
            ),
            'description_ru': (
                "Промышленные реагенты, масла и химические добавки. Необходимые "
                "химические материалы для бесперебойной работы энергопредприятий."
            ),
            'description_en': (
                "Industrial reagents, oils and chemical additives. Necessary chemical "
                "materials for uninterrupted operation of energy enterprises."
            ),
            'icon': 'bi-droplet-fill',
            'order': 5,
        },
        {
            'name_uz': 'Qurilish materiallari',
            'name_ru': 'Строительные материалы',
            'name_en': 'Construction Materials',
            'description_uz': (
                "O'tga chidamli g'ishtlar, izolyatsiya plitalari va qurilish aralashmalari. "
                "Energetika ob'ektlarini qurish va ta'mirlash uchun maxsus materiallar."
            ),
            'description_ru': (
                "Огнеупорный кирпич, изоляционные плиты и строительные смеси. "
                "Специальные материалы для строительства и ремонта энергообъектов."
            ),
            'description_en': (
                "Refractory bricks, insulation boards and building mixes. "
                "Special materials for construction and repair of energy facilities."
            ),
            'icon': 'bi-bricks',
            'order': 6,
        },
    ]
    for sd in services:
        s = Service.objects.create(**sd)
        print(f'  Service: {s.name_uz}')

# ── CATALOG ITEMS — only seed per-service if that service has no items ─────
catalog = [
    ('Energetika uskunalarini yetkazib berish', [
        ('Rotorlar', 'Роторы', 'Rotors',
         "Elektrostansiyalar, bug' va gaz turbinalari hamda yirik sanoat generatorlari uchun "
         "yuqori sifatli rotorlar. Yuqori tezlikda ishonchli ishlash, mukammal dinamik "
         "balanslanish va yuqori tebranishga chidamlilik.",
         "Высококачественные роторы для электростанций, паровых и газовых турбин. "
         "Надёжная работа на высоких скоростях, отличная динамическая балансировка.",
         "High-quality rotors for power plants, steam and gas turbines. Reliable operation "
         "at high speeds, excellent dynamic balancing and vibration resistance.",
         'services/image1.png', 1),

        ('Transformatorlar', 'Трансформаторы', 'Transformers',
         "Elektr energiyasini uzatish va taqsimlash uchun yuqori va past kuchlanishli kuch "
         "transformatorlari. Yog'li va quruq transformatorlarning turli xillari mavjud.",
         "Силовые трансформаторы высокого и низкого напряжения для передачи и распределения "
         "электроэнергии. Масляные и сухие типы.",
         "High and low voltage power transformers for electricity transmission and distribution. "
         "Various types of oil and dry transformers.",
         'services/image2.png', 2),

        ('Generatorlar', 'Генераторы', 'Generators',
         "Sanoat korxonalari va energetika ob'ektlari uchun turbogeneratorlar va zaxira dizel "
         "generatorlari. Uzluksiz quvvat ta'minoti kafolatlangan manba.",
         "Турбогенераторы и резервные дизельные генераторы для промышленных предприятий "
         "и энергообъектов. Гарантированный источник бесперебойного питания.",
         "Turbogenerators and backup diesel generators for industrial enterprises and energy "
         "facilities. Guaranteed source of uninterrupted power.",
         'services/image3.jpeg', 3),

        ('Elektrostansiya uskunalari', 'Оборудование электростанций', 'Power Plant Equipment',
         "Issiqlik elektrostansiyalari va qozonxonalar uchun yordamchi uskunalar, qozon "
         "agregatlar va avtomatika tizimlari. Texnologiyalar uzluksiz ishni ta'minlaydi.",
         "Вспомогательное оборудование, котельные агрегаты и системы автоматики для "
         "тепловых электростанций и котельных.",
         "Auxiliary equipment, boiler units, and automation systems for thermal power plants "
         "and boiler houses.",
         'services/image5.jpeg', 4),

        ('Yuqori kuchlanishli uskunalar', 'Высоковольтное оборудование', 'High-Voltage Equipment',
         "Yirik elektr podstansiyalari uchun yuqori kuchlanishli uskunalar — kommutatsiya "
         "apparaturasi, o'chirish qurilmalari va himoya tizimlari.",
         "Высоковольтное оборудование для крупных электрических подстанций — коммутационная "
         "аппаратура, отключающие устройства и системы защиты.",
         "High-voltage equipment for large electrical substations — switching apparatus, "
         "disconnecting devices and protection systems.",
         'services/image4.png', 5),

        ('Har xil ehtiyot qismlar', 'Запасные части всех видов', 'All Types of Spare Parts',
         "Energetika uskunalarining barcha turlari uchun ehtiyot qismlar. Turbina, generator, "
         "transformator va boshqa uskunalarning ta'mir va texnik xizmatiga mo'ljallangan qismlar.",
         "Запасные части для всех видов энергетического оборудования. Детали для ремонта "
         "и обслуживания турбин, генераторов, трансформаторов.",
         "Spare parts for all types of energy equipment. Parts for repair and maintenance "
         "of turbines, generators, transformers.",
         'services/image6.png', 6),
    ]),

    ('Armatura va mexanik qismlar', [
        ('Shiberlar (zatvory)', 'Задвижки (шиберы)', 'Gate Valves',
         "Sanoat quvur tizimlarida suyuqlik yoki gaz oqimini to'sish uchun. Po'lat va quyma "
         "temir korpuslar, yuqori bosimga chidamlilik, flansli va payvandli ulanish.",
         "Для надёжного перекрытия потоков жидкости или газа в промышленных трубопроводах. "
         "Стальные и чугунные корпуса, высокая устойчивость к давлению.",
         "For reliable shut-off of fluid or gas flows in industrial pipelines. "
         "Steel and cast iron bodies, high pressure resistance.",
         'services/image9.jpeg', 1),

        ('Klapanlar va ventillar', 'Клапаны и вентили', 'Valves',
         "Quvur tizimlarida oqimni nazorat qilish va orqaga qaytishni oldini olish. Himoya, "
         "boshqaruv va rostlash vazifalari. Zangbardosh po'lat va bronza qotishmalar.",
         "Контроль потока и предотвращение обратного хода в трубопроводных системах. "
         "Защитные, управляющие и регулирующие функции.",
         "Flow control and back-flow prevention in piping systems. Protective, control "
         "and regulating functions. Stainless steel and bronze alloys.",
         'services/image10.png', 2),

        ('Nasoslar', 'Насосы', 'Pumps',
         "Sanoat korxonalari va issiqlik ta'minot tizimlari uchun sanoat nasoslar. Yuqori "
         "unumdorlik, suv, yog' va kimyoviy suyuqliklar uchun yaroqli.",
         "Промышленные насосы для предприятий и систем теплоснабжения. Высокая "
         "производительность, пригодны для воды, масла и химических жидкостей.",
         "Industrial pumps for enterprises and heating systems. High performance, "
         "suitable for water, oil and chemical liquids.",
         'services/image11.jpeg', 3),

        ('Metall kesish dastgohlari', 'Металлорежущие станки', 'Machine Tools',
         "Metall kesish dastgohlari, CNC tizimlari, tokarlik va frezerlik mashinalari. "
         "Yuqori aniqlikdagi sanoat ishlab chiqarish uchun energiya tejovchi elektr drayvlar.",
         "Металлообрабатывающие станки, ЧПУ-системы, токарные и фрезерные машины. "
         "Для высокоточного производства с энергосберегающими приводами.",
         "Metalworking machines, CNC systems, lathes and milling machines. "
         "For high-precision manufacturing with energy-saving drives.",
         'services/image12.jpeg', 4),

        ('Avtomatlashtirilgan uskunalar', 'Автоматизированное оборудование', 'Automated Equipment',
         "Avtomatika shkaflari, PLC kontrollerlar, o'lchov panellari va aqlli monitoring "
         "tizimlari. Zavodlarda sanoat jarayonlarini avtomatlashtirish uchun.",
         "Шкафы автоматики, ПЛК-контроллеры, измерительные панели и интеллектуальные "
         "системы мониторинга для автоматизации промышленных процессов.",
         "Automation cabinets, PLC controllers, measurement panels and smart monitoring "
         "gear for automating industrial processes.",
         'services/image13.jpeg', 5),
    ]),

    ('Elektr jihozlari', [
        ('Kabellar va simlar', 'Кабели и провода', 'Cables and Wires',
         "Yuqori va past kuchlanishli kabellar, izolyatsiyalangan o'tkazgichlar. Energetika "
         "tarmoqlari, sanoat korxonalari va turar-joy binolari uchun.",
         "Кабели высокого и низкого напряжения, изолированные проводники. Для энергосетей, "
         "промышленных предприятий и жилых зданий.",
         "High and low voltage cables, insulated conductors. For power grids, "
         "industrial enterprises and residential buildings.",
         'services/image14.jpeg', 1),

        ('Elektr himoya qurilmalari', 'Электрозащитные устройства', 'Electrical Protection Devices',
         "Avtomatik uzgichlar, rele himoya tizimlari, o'chirish qurilmalari. Elektr tarmoqlarini "
         "qisqa tutashuv va ortiqcha yuklamadan himoya qilish.",
         "Автоматические выключатели, системы релейной защиты, отключающие устройства. "
         "Защита электросетей от короткого замыкания и перегрузки.",
         "Circuit breakers, relay protection systems, disconnecting devices. "
         "Protection of power networks from short circuits and overloads.",
         'services/image15.jpeg', 2),

        ("O'lchov asboblari", 'Контрольно-измерительные приборы', 'Measuring Instruments',
         "Tok va kuchlanish o'lchov transformatorlari, elektr hisoblagichlari, raqamli o'lchov "
         "asboblari. Energiya sarfini aniq nazorat qilish uchun.",
         "Трансформаторы тока и напряжения, электросчётчики, цифровые измерительные приборы "
         "для точного контроля потребления энергии.",
         "Current and voltage transformers, electricity meters, digital instruments "
         "for precise energy consumption monitoring.",
         'services/image16.jpeg', 3),
    ]),

    ('Metall mahsulotlar', [
        ('Prokat metall', 'Прокат металла', 'Rolled Metal',
         "Kanal, burchak, dvutavr, list va boshqa turdagi metall prokat. Energetika inshootlari "
         "va sanoat ob'ektlari qurilishi uchun.",
         "Швеллер, уголок, двутавр, лист и другие виды металлопроката. "
         "Для строительства энергетических и промышленных объектов.",
         "Channel, angle, I-beam, sheet and other rolled metal types. "
         "For construction of energy and industrial facilities.",
         'services/image17.png', 1),

        ('Quvurlar va fitinglar', 'Трубы и фитинги', 'Pipes and Fittings',
         "Sanoat quvurlar, fitinglar, flanetslar. Suv ta'minoti, bug' va gaz quvur tizimlari "
         "uchun po'lat va quyma temir quvurlar.",
         "Промышленные трубы, фитинги, фланцы. Стальные и чугунные трубы для систем "
         "водоснабжения, пара и газопроводов.",
         "Industrial pipes, fittings, flanges. Steel and cast iron pipes for water supply, "
         "steam and gas pipeline systems.",
         'services/image18.jpeg', 2),

        ('Maxsus qotishmalar', 'Спецсплавы и конструкции', 'Special Alloys and Structures',
         "Energetika uchun maxsus metallar: issiqlikka chidamli po'lat, mis va alyuminiy "
         "qotishmalar, metall konstruktsiyalar.",
         "Специальные металлы для энергетики: жаропрочная сталь, медные и алюминиевые "
         "сплавы, металлоконструкции.",
         "Special metals for energy: heat-resistant steel, copper and aluminum alloys, "
         "metal structures.",
         'services/image19.jpeg', 3),
    ]),

    ('Kimyoviy mahsulotlar', [
        ('Sanoat reagentlari', 'Промышленные реагенты', 'Industrial Reagents',
         "Suv tozalash, katodli himoya va boshqa sanoat jarayonlari uchun kimyoviy reagentlar. "
         "Energetika korxonalari uchun sertifikatlangan mahsulotlar.",
         "Химические реагенты для водоподготовки, катодной защиты и других промышленных "
         "процессов. Сертифицированные продукты для энергопредприятий.",
         "Chemical reagents for water treatment, cathodic protection and other industrial "
         "processes. Certified products.",
         'services/image7.jpeg', 1),

        ("Moylash materiallari va yog'lar", 'Смазочные материалы и масла', 'Lubricants and Oils',
         "Turbina, kompressor va transmissiya yog'lari. Energetika uskunalarini uzoq muddatli "
         "va ishonchli ishlashini ta'minlash uchun maxsus yog'lar.",
         "Турбинные, компрессорные и трансмиссионные масла. Специальные масла для "
         "долгосрочной и надёжной работы энергооборудования.",
         "Turbine, compressor and transmission oils. Special oils to ensure long-term "
         "and reliable operation of energy equipment.",
         'services/image8.png', 2),

        ("Kimyoviy qo'shimchalar", 'Химические добавки', 'Chemical Additives',
         "Qozon suvini kimyoviy tozalash, zangga qarshi himoya va korroziyaga qarshi vositalar. "
         "Energetika uskunalarining samaradorligini oshiradi.",
         "Химическая обработка котловой воды, антикоррозийные и антиокислительные средства. "
         "Повышают эффективность энергетического оборудования.",
         "Chemical treatment of boiler water, anti-corrosion and antioxidant agents. "
         "Increase the efficiency of energy equipment.",
         'services/image20.png', 3),
    ]),

    ('Qurilish materiallari', [
        ("O'tga chidamli g'ishtlar", 'Огнеупорный кирпич', 'Refractory Bricks',
         "Qozon pechlari, o'choq va yuqori haroratli sanoat jihozlari uchun o'tga chidamli "
         "g'ishtlar. 1800°C gacha haroratga chidaydi.",
         "Огнеупорные кирпичи для котельных печей, топок и высокотемпературного оборудования. "
         "Выдерживают температуру до 1800°C.",
         "Refractory bricks for boiler furnaces and high-temperature industrial equipment. "
         "Withstand temperatures up to 1800°C.",
         'services/image5.jpeg', 1),

        ('Izolyatsiya plitalari va materiallari', 'Изоляционные плиты и материалы',
         'Insulation Boards and Materials',
         "Issiqlik va akustik izolyatsiya plitalari, mineral paxta, shisha tolasi. "
         "Quvur tizimlar va uskunalar uchun izolyatsiya yechimlari.",
         "Теплоизоляционные и акустические плиты, минеральная вата, стекловолокно. "
         "Изоляционные решения для трубопроводов и оборудования.",
         "Thermal and acoustic insulation boards, mineral wool, fiberglass. "
         "Insulation solutions for pipelines and equipment.",
         'services/image6.png', 2),

        ('Qurilish aralashmalari va sementlar', 'Строительные смеси и цементы',
         'Building Mixes and Cements',
         "Energetika ob'ektlari qurilishi va ta'mirlashi uchun maxsus qurilish aralashmalari, "
         "o'tga chidamli sement va boshqa materiallar.",
         "Специальные строительные смеси, огнеупорный цемент и другие материалы для "
         "строительства и ремонта энергетических объектов.",
         "Special building mixes, refractory cement and other materials for construction "
         "and repair of energy facilities.",
         'services/image4.png', 3),
    ]),
]

for service_name, items in catalog:
    try:
        svc = Service.objects.get(name_uz=service_name)
    except Service.DoesNotExist:
        print(f'  ! Service not found: {service_name}')
        continue
    if svc.catalog_items.exists():
        print(f'  Catalog for "{service_name}": already exists, skipping')
        continue
    for name_uz, name_ru, name_en, desc_uz, desc_ru, desc_en, image, order in items:
        CatalogItem.objects.create(
            service=svc,
            name_uz=name_uz, name_ru=name_ru, name_en=name_en,
            description_uz=desc_uz, description_ru=desc_ru, description_en=desc_en,
            image=image, order=order,
        )
        print(f'    + {name_uz}')

# ── NEWS — only seed if none exist ────────────────────────────────────────
if News.objects.exists():
    print('News: already exist, skipping')
else:
    news_items = [
        ("Bugun O'zbekiston Respublikasining Davlat gerbi qabul qilingan kun nishonlanadi",
         "Сегодня Узбекистан отмечает День принятия Государственного герба Республики Узбекистан",
         "Today Uzbekistan marks the Day of the Adoption of the State Emblem",
         ("Bugun O'zbekiston Respublikasining Davlat gerbi qabul qilingan kun nishonlanadi. "
          "O'ZENERGOTA'MINLASH aksiyadorlik jamiyati jamoasi bu munosabat bilan barcha "
          "vatandoshlarimizni qutlaydi."),
         ("Сегодня Узбекистан отмечает День принятия Государственного герба. "
          "Коллектив O'ZENERGOTA'MINLASH AJ поздравляет всех граждан с этим праздником."),
         ("Today Uzbekistan marks the Day of Adoption of the State Emblem. "
          "The team of UZBEKENERGO SUPPLY JSC congratulates all citizens."),
         'news/photo_2026-07-02_14-07-15.jpg',
         datetime.datetime(2026, 7, 2, 14, 0),
         'davlat-gerbi-qabul-qilingan-kun-2026'),

        ("Korxonalarga ishonchli, o'z vaqtida va sifatli mahsulotlarni yetkazib berish",
         "Надёжная, своевременная и качественная доставка продукции на предприятия",
         "Reliable, Timely and High-Quality Product Delivery to Enterprises",
         ("O'ZENERGOTA'MINLASH AJ O'zbekiston energetika korxonalariga uzluksiz va o'z vaqtida "
          "ta'minot xizmatini ko'rsatishni davom ettirmoqda."),
         ("O'ZENERGOTA'MINLASH AJ O'zbekiston energetika korxonalarga uzluksiz va o'z vaqtida "
          "ta'minot xizmatini ko'rsatishni davom ettirmoqda."),
         ("UZBEKENERGO SUPPLY JSC continues to provide uninterrupted and timely supply services "
          "to Uzbekistan's energy enterprises."),
         'news/photo_2026-06-03_11-44-23.jpg',
         datetime.datetime(2026, 6, 3, 11, 44),
         'ishonchli-yetkazib-berish-2026'),

        ('Energotizim barqarorligi — asosiy maqsadimiz',
         "Стабильность энергосистемы — наша главная цель",
         'Energy System Stability — Our Main Goal',
         ("O'ZENERGOTA'MINLASH AJ O'zbekiston energetika tarmog'ining barqaror ishlashini "
          "ta'minlash uchun barcha zarur resurslar va uskunalarni o'z vaqtida yetkazib "
          "berishni asosiy vazifa qilib qo'ygan."),
         ("O'ZENERGOTA'MINLASH AJ O'zbekiston energetika tarmog'ining barqaror ishlashini "
          "ta'minlash uchun barcha zarur resurslar va uskunalarni o'z vaqtida yetkazib "
          "berishni asosiy vazifa qilib qo'ygan."),
         ("UZBEKENERGO SUPPLY JSC has set as its main task the timely delivery of all necessary "
          "resources and equipment for stable operation of the energy system."),
         'news/photo_2026-06-03_11-41-05.jpg',
         datetime.datetime(2026, 6, 3, 11, 41),
         'energotizim-barqarorligi-2026'),

        ('Sifatli xizmat — bizning ustuvor vazifamiz',
         "Качественный сервис — наша приоритетная задача",
         'Quality Service — Our Priority Task',
         ("Kompaniyamiz mijozlarga ko'rsatilayotgan xizmat sifatini doimiy ravishda oshirib "
          "bormoqda. Yangi raqamli tizimlar joriy etilishi bilan buyurtma jarayoni yanada "
          "tezlashdi va qulay bo'ldi."),
         ("Kompaniyamiz mijozlarga ko'rsatilayotgan xizmat sifatini doimiy ravishda oshirib "
          "bormoqda. Yangi raqamli tizimlar joriy etilishi bilan buyurtma jarayoni yanada "
          "tezlashdi va qulay bo'ldi."),
         ("Our company continuously improves service quality. With new digital systems, "
          "the ordering process has become even faster and more convenient."),
         'news/photo_2026-06-03_11-37-50.jpg',
         datetime.datetime(2026, 6, 3, 11, 37),
         'sifatli-xizmat-2026'),

        ('Muhokamalar va muhim qarorlar',
         "Обсуждения и важные решения",
         'Discussions and Important Decisions',
         ("O'ZENERGOTA'MINLASH AJ rahbariyati energetika sohasi rivojlanishiga oid muhim "
          "masalalar yuzasidan yig'ilish o'tkazdi. Kompaniyaning kelgusi yilga strategik "
          "rejalari muhokama qilindi."),
         ("O'ZENERGOTA'MINLASH AJ rahbariyati energetika sohasi rivojlanishiga oid muhim "
          "masalalar yuzasidan yig'ilish o'tkazdi. Kompaniyaning kelgusi yilga strategik "
          "rejalari muhokama qilindi."),
         ("The management of UZBEKENERGO SUPPLY JSC held a meeting on important energy sector "
          "development issues. The company's strategic plans were discussed."),
         'news/photo_2026-05-26_10-23-33.jpg',
         datetime.datetime(2026, 5, 26, 10, 23),
         'muhokamalar-2026'),
    ]

    for title_uz, title_ru, title_en, cont_uz, cont_ru, cont_en, image, dt, slug in news_items:
        News.objects.create(
            title_uz=title_uz, title_ru=title_ru, title_en=title_en,
            content_uz=cont_uz, content_ru=cont_ru, content_en=cont_en,
            image=image, published_at=timezone.make_aware(dt), slug=slug,
        )
        print(f'  News: {title_uz[:60]}')

print('\nSeed complete!')
