# Ubuntu 22.04 / 24.04 serverida loyihani ishga tushirish

Ushbu qo'llanma orqali loyihani (Django) serverda Gunicorn va Nginx yordamida ishga tushirishingiz mumkin.

## 1. Serverni yangilash va kerakli dasturlarni o'rnatish
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git curl -y
```

## 2. Loyihani yuklash va muhitni tayyorlash
Loyiha fayllarini serverning `/var/www/systemc/UZETLAST` papkasiga yuklaganingizdan (yoki git orqali clone qilganingizdan) so'ng:

```bash
cd /var/www/systemc/UZETLAST

# Virtual muhit yaratish
python3 -m venv .venv
source .venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt
pip install gunicorn

# Migratsiyalar va static fayllarni tayyorlash
python manage.py migrate
python manage.py collectstatic --noinput

# Havfsizlik sozlamalari (.env faylini yaratish)
cat <<EOF > .env
DEBUG=False
ALLOWED_HOSTS=uzenergotaminlash.uz,www.uzenergotaminlash.uz,127.0.0.1
DJANGO_SECRET_KEY=$(openssl rand -base64 32)
EOF
```

## 3. Gunicorn xizmatini sozlash
Sizning `deployment/` papkangizda tayyorlangan fayllarni systemd ga ko'chiring:

```bash
sudo cp deployment/gunicorn.socket /etc/systemd/system/
sudo cp deployment/gunicorn.service /etc/systemd/system/

# Xizmatlarni ishga tushirish
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

## 4. Nginx web-serverini sozlash
```bash
sudo cp deployment/uzenergotaminlash.uz.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/uzenergotaminlash.uz.conf /etc/nginx/sites-enabled/

# Nginx holatini tekshirish
sudo nginx -t

# Nginx ni qayta ishga tushirish
sudo systemctl restart nginx
```

## 5. SSL (HTTPS) o'rnatish
Domenga SSL sertifikatini ulash uchun (Certbot):
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d uzenergotaminlash.uz -d www.uzenergotaminlash.uz
```

Barcha jarayon to'g'ri bajarilgan bo'lsa, saytingiz `https://uzenergotaminlash.uz` manzilida to'liq ishga tushadi!
