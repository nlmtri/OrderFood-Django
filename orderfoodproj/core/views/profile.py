from django.shortcuts import render
from core.models.user import * 
from core.models.city import City  

def profile_view(request):
    # Lấy thông tin khách hàng từ cơ sở dữ liệu
    customer = Customer.objects.get(admin=request.user)
    cities = City.objects.all().order_by('name')
    if request.method == 'POST':
        # Xử lý biểu mẫu chỉnh sửa thông tin nếu được gửi đi
        # Đây chỉ là một ví dụ, bạn cần thay đổi logic này để phản ánh yêu cầu cụ thể của bạn
        customer.address = request.POST.get('address')
        customer.phone_number = request.POST.get('phone_number')
        customer.city_id = request.POST.get('city')

        # Lưu các thay đổi vào cơ sở dữ liệu
        customer.save()

    return render(request, 'core/profile.html', {'customer': customer,'cities':cities})
