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

        # Provider
        fullname = request.POST['fullname'] 
        date_of_birth = request.POST['dob']
        ID_card = request.POST['id_card']
        
        address = request.POST.get('address') 
        phone = request.POST.get('phone')

        business_number = request.POST.get('business-number') 
        business_license = request.FILES['business-license'] 
        food_safty_cert = request.FILES['food-safty-cert']

        # Restaurant
        rest_name = request.POST['rest-name']
        rest_address = request.POST['rest-address']
        resst_phone = request.POST['rest-phone']

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

        # Provider
        # Check ID Card
        if Provider.objects.filter(ID_card=ID_card).exists():
            messages.info(request, "Số CMND đã tồn tại!")
            return redirect('register-provider-view')

        if Provider.objects.filter(phone=phone).exists():
            messages.info(request, "Số điện thoại chủ nhà hàng đã tồn tại!")
            return redirect('register-provider-view')

        if Provider.objects.filter(business_number=business_number).exists():
            messages.info(request, "Số chứng nhận kinh doanh của nhà hàng đã tồn tại!")
            return redirect('register-provider-view')

        if Restaurant.objects.filter(phone_number=resst_phone).exists():
            messages.info(request, "Số điện thoại của nhà hàng đã tồn tại!")
            return redirect('register-provider-view')
        provider = user.provider
        provider.fullname = fullname
        provider.date_of_birth = date_of_birth
        provider.ID_card = ID_card
        provider.address = address
        provider.phone = phone 
        provider.business_number = business_number
        provider.business_license = business_license
        provider.food_safty_cert = food_safty_cert

        # Thêm slug cho restaurant tự động
        # Restaurant 
        restaurant = Restaurant.objects.create(
            name=rest_name,
            phone_number=resst_phone,
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