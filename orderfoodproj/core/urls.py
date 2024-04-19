from django.urls import path 
from .views.index import * 
from .views.login import * 
from .views.register import *
from .views.menu import * 
from .views.restaurant import * 
from .views.cart import * 
from .views.dish import *
from .views.profile import * 
from .views.order import * 

# For User
urlpatterns = [
    # GET
    path('', index, name='index'),
    path('login/',get_login_view, name='get-login-view'),
    path('logout/', get_logout_view, name='logout-view'),
    path('register/', get_register_view, name='register-view'),
    path('register-provider/', get_register_provider_view, name='register-provider-view'),
    path('menu/<slug:slug>/', get_menu_detail_view, name='menu-detail-view'),
    path('restaurant/<slug:slug>/', get_restaurant_view, name='restaurant-detail-view'),
    path('cart/detail/', cart_detail_view, name='cart-detail-view'),
    path('profile/', profile_view, name='profile_view'),

    path('place-order/', place_order_view, name='place_order'),
    # POST
    path('do-login/', post_login_view, name='post-login-view'),
    path('do-register/', post_register_view, name='post-register-view'),
    path('do-register-provider/', post_register_provider_view, name='post-register-provider-view'),

    #Cart feature
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

    #order feature
    path('submit-order/', submit_order_view, name='submit_order'),
]

# For Restaurant Admin
urlpatterns += [
    # GET
    path('restaurant-admin/', get_restaurant_admin_view, name='restaurant-admin-view'),
    path('restaurant-admin/dish/', get_dish_admin_view, name='dish-admin-view'),
    path('restaurant-admin/add-dish/', get_add_dish_admin_view, name='add-dish-admin-view'),
    path('restaurant-admin/edit-dish/<pk>/', get_edit_dish_admin_view, name='edit-dish-admin-view'),
    path('restaurant-admin/order/', get_order_admin_view, name='order-admin-view'),
    path('restaurant-admin/profile/<slug:slug>/',get_edit_profile_restaurant_view, name='restaurant-profile-admin-view'),

    # POST
    path('restaurant-admin/profile/save/<slug:slug>/', post_save_profile_restaurant_admin_view, name='save-restaurant-admin-profile-view'),
    path('restaurant-admin/add-dish/save/', post_add_dish_admin_view, name='post-add-dish-admin-view'),
    path('restaurant-admin/delete/dish/<pk>/', post_delete_dish_admin_view, name='post-delete-dish-admin-view'),
    path('restaurant-admin/edit-dish/save/<pk>/', post_edit_dish_admin_view, name='post-edit-dish-admin-view'),
    path('restaurant-admin/update-order/<pk>/', post_update_order_admin_view, name='post-update-order-admin-view'),

    # API
    path('restaurant-admin/order/<pk>/', get_detail_order_admin_api, name='detail-order-admin-api'),
    

]

urlpatterns += [
    # API
    # GET
    path('dishes/<pk>/', get_dish_data_api, name='get-dish-data-api'),

]
