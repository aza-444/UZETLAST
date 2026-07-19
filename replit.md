# UZEnergo Ta'minlash — Django Website

Django asosida qurilgan energetika kompaniyasi sayti.

## Ishga tushirish

```bash
bash /home/runner/workspace/website/manage_start.sh
```

## Admin panel

- URL: `http://localhost:8000/admin/`
- Login: `admin`
- Parol: `Admin1234!` (birinchi ishda o'zgartiring)

## Texnik stack

- Python 3.13 + Django 6.0
- SQLite (ma'lumotlar bazasi)
- WhiteNoise (statik fayllar)
- Bootstrap Icons + AOS animation

## Tuzilma

```
website/
├── config/          # Django project settings
├── main/            # Asosiy app (models, views, admin)
│   ├── models.py    # Barcha modellar (3 tilli)
│   ├── admin.py     # To'liq admin panel
│   ├── views.py     # Ko'rinishlar
│   └── urls.py      # URL yo'nalishlar
├── templates/       # HTML shablonlar
├── static/          # CSS, JS fayllar
└── manage_start.sh  # Ishga tushirish skripti
```

## User preferences

- Django backend, Python
- 3 til: UZ (asosiy), RU, EN
- Qorong'u (dark) dizayn
