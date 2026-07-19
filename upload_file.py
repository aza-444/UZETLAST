"""
Django management command: import_corporate_docs

Papkadagi (Windows yo'l) fayllarni CorporateCategory / CorporateDocument
modellariga import qiladi. HTTP so'rov yubormaydi — to'g'ridan-to'g'ri
Django ORM orqali bazaga yozadi, shuning uchun serverni ishga tushirish
shart emas.

Joylashtirish:
    <app_nomi>/management/commands/import_corporate_docs.py
    (management/ va commands/ papkalarida __init__.py bo'lishi kerak)

Ishlatish:
    python manage.py import_corporate_docs "C:\\Users\\AZA\\Desktop\\openinfo_last"
    python manage.py import_corporate_docs "C:\\...\\openinfo_last" --dry-run
    python manage.py import_corporate_docs "C:\\...\\openinfo_last" --year 2026
"""
import os
import re
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from website.main.models import  CorporateCategory, CorporateDocument  # app nomini moslang

ALLOWED_EXT = {'.pdf', '.doc', '.docx', '.xls', '.xlsx'}
YEAR_RE = re.compile(r'(20\d{2})')


class Command(BaseCommand):
    help = "4 ta papkadan (E'lonlar, Moliyaviy hisobotlar, Muhim faktlar, Ustav) hujjatlarni import qiladi"

    def add_arguments(self, parser):
        parser.add_argument(
            'base_dir',
            type=str,
            help="Papkalar joylashgan asosiy yo'l, masalan: openinfo_last"
        )
        parser.add_argument(
            '--year',
            type=int,
            default=None,
            help="Fayl nomida yil topilmasa shu yil qo'yiladi (default: joriy yil)"
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Hech narsa yozmasdan faqat nima qilinishini ko'rsatadi"
        )

    def handle(self, *args, **options):
        base_dir = Path(options['base_dir'])
        default_year = options['year'] or 2026
        dry_run = options['dry_run']

        if not base_dir.is_dir():
            raise CommandError(f"Papka topilmadi: {base_dir}")

        folder_names = ["E'lonlar", "Moliyaviy hisobotlar", "Muhim faktlar", "Ustav"]

        created_cats = 0
        created_docs = 0
        skipped = 0

        for folder_name in folder_names:
            folder_path = base_dir / folder_name
            if not folder_path.is_dir():
                self.stdout.write(self.style.WARNING(
                    f"O'tkazib yuborildi (papka topilmadi): {folder_path}"
                ))
                continue

            if dry_run:
                category = CorporateCategory.objects.filter(name_uz=folder_name).first()
                cat_exists = "mavjud" if category else "YARATILADI"
            else:
                category, was_created = CorporateCategory.objects.get_or_create(
                    name_uz=folder_name
                )
                cat_exists = "yaratildi" if was_created else "mavjud edi"
                if was_created:
                    created_cats += 1

            self.stdout.write(f"\n[{folder_name}] kategoriya {cat_exists}")

            for root, _dirs, files in os.walk(folder_path):
                for filename in sorted(files):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext not in ALLOWED_EXT:
                        skipped += 1
                        continue

                    file_path = Path(root) / filename
                    title = os.path.splitext(filename)[0]

                    year_match = YEAR_RE.search(filename)
                    year = int(year_match.group(1)) if year_match else default_year
                    is_archive = year_match is None and options['year'] is None and False
                    # Yilni fayl nomidan topa olmasa ham arxiv qilib belgilamaymiz,
                    # default_year bilan yoziladi — kerak bo'lsa admin'da tuzating.

                    if dry_run:
                        self.stdout.write(
                            f"  -> {file_path.name}  |  title='{title}'  |  year={year}"
                        )
                        continue

                    exists = CorporateDocument.objects.filter(
                        category=category, title_uz=title
                    ).exists()
                    if exists:
                        self.stdout.write(self.style.WARNING(
                            f"  -- allaqachon mavjud, o'tkazildi: {title}"
                        ))
                        skipped += 1
                        continue

                    with open(file_path, 'rb') as fh:
                        doc = CorporateDocument(
                            category=category,
                            title_uz=title,
                            year=year,
                            is_archive=is_archive,
                        )
                        doc.file.save(filename, File(fh), save=True)

                    created_docs += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  + qo'shildi: {title} ({filename}, {year})"
                    ))

        self.stdout.write(self.style.SUCCESS(
            f"\nTayyor. Yangi kategoriya: {created_cats}, "
            f"yangi hujjat: {created_docs}, o'tkazib yuborildi: {skipped}"
            + (" (DRY RUN — hech narsa yozilmadi)" if dry_run else "")
        ))