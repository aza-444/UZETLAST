import os
import django
import codecs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import CorporateDocument, CorporateCategory

with codecs.open('titles_dump.txt', 'w', 'utf-8') as f:
    f.write("--- Categories ---\n")
    for c in CorporateCategory.objects.all():
        f.write(f"{c.name_uz} | {c.name_ru} | {c.name_en}\n")
    
    f.write("\n--- Documents ---\n")
    for d in CorporateDocument.objects.all():
        f.write(f"{d.title_uz} | {d.title_ru} | {d.title_en}\n")
