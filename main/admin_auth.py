from django.contrib.auth import login as auth_login
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

original_login = admin.site.login

def custom_admin_login(request, extra_context=None):
    if request.method == 'POST' and '2fa_code' in request.POST:
        # User is submitting the 2FA code
        expected_code = request.session.get('2fa_code')
        user_id = request.session.get('2fa_user_id')
        expire_str = request.session.get('2fa_expire')
        
        if not expected_code or not user_id or not expire_str:
            return redirect('admin:login')
            
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            expire_time = timezone.datetime.fromisoformat(expire_str)
        except ValueError:
            return redirect('admin:login')
            
        if timezone.now() > expire_time:
            return render(request, 'admin/login_2fa.html', {'error': "Kod muddati tugagan. Qaytadan urinib ko'ring."})
            
        if request.POST['2fa_code'].strip() == expected_code:
            try:
                user = User.objects.get(id=user_id)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user)
                del request.session['2fa_code']
                del request.session['2fa_user_id']
                del request.session['2fa_expire']
                
                next_url = request.GET.get('next', '/admin/')
                return redirect(next_url)
            except User.DoesNotExist:
                return redirect('admin:login')
        else:
            return render(request, 'admin/login_2fa.html', {'error': "Noto'g'ri kod kiritildi."})
            
    # Call the original login view
    response = original_login(request, extra_context)
    
    # Check if login was successful
    if response.status_code == 302 and request.user.is_authenticated:
        if request.user.is_superuser:
            user = request.user
            logout(request)
            
            code = str(random.randint(100000, 999999))
            request.session['2fa_code'] = code
            request.session['2fa_user_id'] = user.id
            request.session['2fa_expire'] = (timezone.now() + timedelta(minutes=5)).isoformat()
            
            email_error = None
            if not user.email:
                email_error = "Superuser emaili mavjud emas! Admin paneldan email qo'shing."
                print(f"[2FA] Superuser (id={user.id}) emaili yo'q!")
            else:
                try:
                    send_mail(
                        'Admin Panelga kirish kodi',
                        f'Sizning tasdiqlash kodingiz: {code}\nKod 5 daqiqa davomida amal qiladi.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    print(f"[2FA] Kod {user.email} ga muvaffaqiyatli yuborildi.")
                except Exception as e:
                    email_error = f"Email yuborishda xatolik: {e}"
                    print(f"[2FA] Email xatolik: {e}")
                
            if email_error:
                return render(request, 'admin/login_2fa.html', {
                    'email': user.email,
                    'email_error': email_error,
                    'debug_code': code if settings.DEBUG else None,
                })
                
            return render(request, 'admin/login_2fa.html', {'email': user.email})
            
    return response
