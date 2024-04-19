from django.shortcuts import render, redirect 
from django.contrib.auth import get_user_model 
from django.contrib.auth.hashers import make_password 
from django.contrib import messages 
import random 
import string 
from core.models.user import * 
from core.models.restaurant import Restaurant


def generate_random_suffix(length = 6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))


def generate_user(base="user"):
    attempt = 1 
    new_username = base 
    UserModel = get_user_model()
    while UserModel.objects.filter(username=new_username).exists():
        new_username = f"{base}{generate_random_suffix()}" 
    return new_username


# GET: /register/
def get_register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'core/register.html', {})


# POST: /do-register/
def post_register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        UserModel = get_user_model()
        if email != '' and not UserModel.objects.filter(email=email).exists():
            username = generate_user()
            print(username)
            hash_password = make_password(password)
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=hash_password,
                user_type=1
            )
            messages.info(request, "Đăng ký tài khoản thành công!")
            return redirect('get-login-view')
        else:
            messages.info(request, "Email đã tồn tại!")
            return redirect('register-view')   
    else:
        return render(request, 'handle_error/405.html', {})

# test@gmail.com 
# @admin123


# GET: /register-provider/
def get_register_provider_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'core/register-provider.html', {})


# POST: /do-register-provider/
def post_register_provider_view(request):
    if request.method == 'POST':
        # User
        username = request.POST.get('username')
        email = request.POST.get('email') 
        password = request.POST.get('password')

        # Restaurant
        rest_name = request.POST['rest-name']
        rest_address = request.POST['rest-address']
        rest_phone = request.POST['rest-phone']

        # Xử lý logic tạo user
        UserModel = get_user_model()
        if username != '' and not UserModel.objects.filter(username=username).exists():
            if email != '' and not UserModel.objects.filter(email=email).exists():
                hash_password = make_password(password)
                user = CustomUser.objects.create(
                    username=username,
                    email=email,
                    password=hash_password,
                    user_type=2
                )
            else:
                messages.info(request, "Email đã tồn tại!")
                return redirect('register-provider-view')
        else:
            messages.info(request, "Tên tài khoản đã tồn tại!")
            return redirect('register-provider-view')

        provider = user.provider


        # Thêm slug cho restaurant tự động
        # Restaurant 
        restaurant = Restaurant.objects.create(
            name=rest_name,
            phone_number=rest_phone,
            address=rest_address
        )
        # Các giá trị default của rest 
        # Banner default, Logo default 
        # city: cho default

        # Liên kết provider với restaurant
        provider.restaurant = restaurant
        provider.save()

        messages.info(request, "Đăng ký nhà hàng thành công, chờ duyệt trong 24h!")
        return redirect('get-login-view')
    else:
        return render(request, 'handle_error/405.html', {}) 

# provider1
# provider@gmail.com 
# @admin123

# Nguyễn Văn A
# 002352565465
# 0234655677
# Cầu giấy, Hà Nội

# Nhà Hàng 289
# 289 Hoàng Quốc Việt, Cầu Giấy, Hà Nội
# 0234467688

# KD-214522-TX-HN24



# userD1019
# rinnmusic2.2@gmail.com
# @Admin1019