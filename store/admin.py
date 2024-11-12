from django.contrib import admin
from .models import AdminLogin,Order,Cart,Login,Category,Product,UserUpload

# Register your models here.
admin.site.register(AdminLogin)
admin.site.register(Login)
admin.site.register(Category)
admin.site.register(UserUpload)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
