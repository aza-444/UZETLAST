import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import CorporateDocument, CorporateCategory

def translate_db():
    print("Kategoriyalarni tarjima qilish...")
    # Category mappings
    cat_translations = {
        "E'lonlar": {"ru": "Объявления", "en": "Announcements"},
        "Moliyaviy hisobotlar": {"ru": "Финансовые отчеты", "en": "Financial Reports"},
        "Muhim faktlar": {"ru": "Важные факты", "en": "Important Facts"},
        "Ustav": {"ru": "Устав", "en": "Charter"},
    }
    
    for cat in CorporateCategory.objects.all():
        if cat.name_uz in cat_translations:
            cat.name_ru = cat_translations[cat.name_uz]["ru"]
            cat.name_en = cat_translations[cat.name_uz]["en"]
            cat.save()
            print(f"[OK] Kategoriya: {cat.name_uz}")

    print("\nHujjatlarni tarjima qilish...")
    
    doc_translations = {
        "«Oʻzenergotaʼminlash» AJ ortiqcha tovar-moddiy zaxiralarini sotadi": {
            "ru": "АО «O'zenergotaminlash» реализует излишки товарно-материальных запасов",
            "en": "JSC O'zenergotaminlash sells surplus inventory"
        },
        "Boshqalar": {"ru": "Прочие", "en": "Others"},
        "Tanlovlar va tenderlar": {"ru": "Конкурсы и тендеры", "en": "Competitions and tenders"},
        "Umumiy aksiyadorlar yig'ilishini o'tkazish": {"ru": "Проведение общего собрания акционеров", "en": "Holding a general meeting of shareholders"},
        "Auditorlik xulosasi_Auditorlik xulosalari": {"ru": "Аудиторское заключение_Аудиторские заключения", "en": "Audit report_Audit reports"},
        "Choraklik hisobot_BHMS": {"ru": "Квартальный отчет_НСБУ", "en": "Quarterly report_NAS"},
        "Moliyaviy hisobot_MHXS": {"ru": "Финансовый отчет_МСФО", "en": "Financial report_IFRS"},
        "Yillik hisobot_BHMS": {"ru": "Годовой отчет_НСБУ", "en": "Annual report_NAS"},
        "20% dan ortiq kapitalga teng aksiyalarni sotib olish": {"ru": "Приобретение акций, составляющих более 20% капитала", "en": "Acquisition of shares equal to more than 20% of capital"},
        "35% aksiyalarning egasi": {"ru": "Владелец 35% акций", "en": "Owner of 35% of shares"},
        "50% dan ortiq aktivlar uchun qarz olish": {"ru": "Привлечение займа на сумму более 50% активов", "en": "Borrowing for more than 50% of assets"},
        "50% dan ortiq kapital uchun qarz olish": {"ru": "Привлечение займа на сумму более 50% капитала", "en": "Borrowing for more than 50% of capital"},
        "Affillangan shaxs bilan bitim": {"ru": "Сделка с аффилированным лицом", "en": "Transaction with an affiliated person"},
        "Affillangan shaxslar ro'yxatini o'zgartirish": {"ru": "Изменение списка аффилированных лиц", "en": "Change in the list of affiliated persons"},
        "Aktivlarning 10% dan ortiq qismini o'z ichiga olgan bitim": {"ru": "Сделка, включающая более 10% активов", "en": "Transaction involving more than 10% of assets"},
        "Boshqaruv organi aksiyalaridagi egalik o'zgarishi": {"ru": "Изменение владения акциями органом управления", "en": "Change in share ownership by management body"},
        "Boshqaruv organi qarorlari": {"ru": "Решения органа управления", "en": "Decisions of the management body"},
        "Boshqaruv tuzilmasidagi o'zgarishlar": {"ru": "Изменения в структуре управления", "en": "Changes in the management structure"},
        "Emitent tomonidan qimmatli qog'ozlarni qayta sotib olish huquqi": {"ru": "Право эмитента на обратный выкуп ценных бумаг", "en": "Right of the issuer to repurchase securities"},
        "Katta hajmdagi bitim": {"ru": "Крупная сделка", "en": "Major transaction"},
        "Manzil_elektron pochta_veb-saytni o'zgartirish": {"ru": "Изменение адреса_электронной почты_веб-сайта", "en": "Change of address_email_website"},
        "Qimmatli qog'ozlar bo'yicha daromad yig'ilishi": {"ru": "Начисление доходов по ценным бумагам", "en": "Accrual of income on securities"},
        "Qimmatli qog'ozlarni amalga oshirish muddati": {"ru": "Срок реализации ценных бумаг", "en": "Securities execution period"},
        "Qimmatli qog'ozlarni chiqarish": {"ru": "Выпуск ценных бумаг", "en": "Issuance of securities"},
        "Nizomlar": {"ru": "Положения", "en": "Regulations"},
        "Ustav": {"ru": "Устав", "en": "Charter"},
    }

    count = 0
    for doc in CorporateDocument.objects.all():
        original = doc.title_uz
        # Split by year pattern if it exists (e.g. "_2026-06-04" or " (XLSX)")
        base_name = original
        suffix = ""
        
        # Some are exactly like "2024-09-23_Ustav" -> prefix is date
        if re.match(r'^\d{4}-\d{2}-\d{2}_', base_name):
            prefix = base_name[:11]
            base_name = base_name[11:]
            suffix = prefix + suffix # put prefix in suffix to append later... actually let's just keep prefix 
            
            # swap
            if base_name in doc_translations:
                doc.title_ru = prefix + doc_translations[base_name]["ru"]
                doc.title_en = prefix + doc_translations[base_name]["en"]
                doc.save()
                count += 1
                continue
                
        # Regex for generic date suffixes "_2016-04-29" or "_2016-04-29_1" or " (XLSX)"
        match = re.search(r'(_\d{4}-\d{2}-\d{2}.*| \(XLSX\)|_1|_2|_3|_4)$', base_name)
        if match:
            suffix = match.group(0)
            base_name = base_name[:match.start()]
            
        if base_name in doc_translations:
            doc.title_ru = doc_translations[base_name]["ru"] + suffix
            doc.title_en = doc_translations[base_name]["en"] + suffix
            doc.save()
            count += 1
        elif original in doc_translations:
            doc.title_ru = doc_translations[original]["ru"]
            doc.title_en = doc_translations[original]["en"]
            doc.save()
            count += 1
        else:
            print(f"[NO TRANSLATION FOUND] {original}")
            
    print(f"\nJami {count} ta hujjat tarjima qilindi.")

if __name__ == "__main__":
    translate_db()
