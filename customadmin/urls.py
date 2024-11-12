from django.urls import path
from . import views

urlpatterns = [
    #Admin Login,Registration,Logout,Password forgot
    path('admin_index/', views.admin_index, name='admin_index'),
    path('admin_register/', views.admin_register, name='ad_register'),
    # path('ar/', views.ar, name='ar'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('adminpasswordReset/', views.admin_password_reset_request, name='admin_forgot_password'),
    path('admin_validate-otp/', views.admin_validate_otp, name='admin_validate_otp'),

    # Admin Panel :- List Category,Product List,Add Product Category, Add Product,Update Product,Delete Product,Order List
    path('listCategory/', views.listCategory, name='listCategory'),
    path('add_productCategory/', views.add_productCategory, name='add_productCategory'),
    path('category_update/<int:p_id>/', views.category_update, name='category_update'),
    path('category_delete/<int:p_id>/', views.category_delete, name='category_delete'),
    
    path('listProduct/', views.listProduct, name='listProduct'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_update/<int:p_id>/', views.product_update, name='product_update'),
    path('product_delete/<int:p_id>/', views.product_delete, name='product_delete'),

    path('orderList/', views.orderList, name='orderList'),
    path('approve-order/<int:order_id>/', views.approve_order, name='approve_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('listAdmin/', views.listAdmin, name='listAdmin'),
    path('updateAdmin/<int:p_id>/', views.update_admin, name='change_admin_detail'),
    path('delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),

    path('listFeedback/', views.listFeedback, name='listFeedback'),
    path('inventory/', views.inventory_list_view, name='inventory_list'),
    path('inventory_update/<int:p_id>/', views.inventory_update, name='inventory_update'),
    path('bulkupload/', views.bulkupload, name='bulkupload'),
    path('bulkuploadview/', views.bulkuploadview, name='bulkuploadview'),
    path('export/excel/', views.export_to_excel, name='export_excel'),
]
