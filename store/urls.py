from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path("product/", views.product, name="product"),
    path('products/', views.product_list, name='product_list'),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.profile, name="profile"),
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path("cart/", views.view_cart, name="view_cart"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('orderproduct', views.orderproduct, name='orderproduct'),
    path('view_order/<int:p_id>/', views.view_order, name='view_order'), 
    path('download_bill/<int:order_id>/', views.download_bill, name='download_bill'),
    path('user_cancel_order/<int:order_id>/', views.user_cancel_order, name='user_cancel_order'),
    path("buy/<int:item_id>/", views.buy_product, name="buy"),  # Ensure item_id is used here
    path("remove_from_cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('payment_success/', views.payment_success, name='payment_success'),
]
