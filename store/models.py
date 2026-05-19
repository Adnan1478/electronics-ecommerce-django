from django.db import models
from django.utils import timezone

class Login(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class AdminLogin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=15)
    admin_right = models.BooleanField(default=False)

    def __str__(self):
        return f'Admin {self.username}'

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=150)
    cat_description = models.TextField()

    def __str__(self):
        return self.cat_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    product_desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.product_name

class UserUpload(models.Model):
    uid = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='user_uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.city}'

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    customer = models.ForeignKey(Login, on_delete=models.CASCADE,null=True)
    # status = models.BooleanField(default=True)  # Uncomment if needed

    def __str__(self):
        return f'Cart {self.cart_id}'

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
        ('REFUNDED', 'Refunded'),
        ('FAILED', 'Payment Failed'),
        ('RETURNED', 'Returned')
    ]

    order_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    customer = models.ForeignKey(Login, on_delete=models.CASCADE)
    user_details = models.ForeignKey(UserUpload, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Order {self.order_id} - {self.status}'

class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.full_name} - {self.subject}'

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.product.product_name} - {self.quantity_available} in stock'

    class Meta:
        verbose_name_plural = "Inventories"
