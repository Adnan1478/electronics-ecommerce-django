import openpyxl
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password

from store.models import AdminLogin, Product, Category, Order, Cart, Contact,Inventory
from .forms import AdminRegistrationForm, AdminLoginForm

from store.forms import ProductForm, CategoryForm
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string


import io
import csv

# Admin Login
def admin_index(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")
    # username = request.session.get('username')  # Retrieve username from session
    return render(request, "admin/adminpanel.html", {"username": username})


# def ar(request):
#     if request.method == 'POST':
#         form = AdminRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()  # This will handle saving the user with the hashed password
#             messages.success(request, "Your account has been created successfully.")
#             return redirect('ad_register')  # Redirect to the login page after successful registration
#         else:
#             # If form is not valid, the errors will be shown in the template
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = AdminRegistrationForm()

#     return render(request, 'admin/AdminRegister.html', {'form': form})


def admin_register(request):
    username = request.session.get("username")

    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    if not user.admin_right:
        messages.error(
            request, "You do not have the necessary admin rights to add a admin."
        )
        return redirect(
            "admin_index"
        )  # Redirect to the admin index or an appropriate page

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("comfirmpassword")
        contact = request.POST.get("contact")
        admin_right = request.POST.get("admin_right") == "1"

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            hashed_password = make_password(password)
            admin_user = AdminLogin(
                username=username,
                email=email,
                password=hashed_password,
                contact=contact,
                admin_right=admin_right,
            )
            admin_user.save()
            messages.success(request, "Admin account has been created successfully.")
            return redirect("listAdmin")  # Redirect after successful registration

    return render(request, "admin/AdminRegister.html")


def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = AdminLogin.objects.get(username=username)
                if check_password(password, user.password):
                    # Store user information in session
                    request.session["user_id"] = user.id
                    request.session["username"] = user.username
                    request.session["is_authenticated"] = (
                        True  # Custom session key to check authentication
                    )
                    return redirect("admin_index")
                else:
                    form.add_error("password", "Incorrect password")
            except AdminLogin.DoesNotExist:
                form.add_error("username", "User does not exist")
    else:
        form = AdminLoginForm()
    return render(request, "admin/AdminLogin.html", {"form": form})


def admin_logout(request):
    logout(request)
    request.session.flush()  # Clear all session data
    return redirect("admin_login")


def admin_password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if AdminLogin.objects.filter(email=email).exists():
            otp = get_random_string(length=6, allowed_chars="1234567890")
            # Save OTP to user's profile or session, here using session for simplicity
            request.session["reset_otp"] = otp
            request.session["reset_email"] = email
            # Send OTP via email
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect("admin_validate_otp")
        else:
            messages.error(request, "Email not found")
    return render(request, "admin/forgot_password.html")


def admin_validate_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if otp == request.session.get("reset_otp"):
            if new_password == confirm_password:
                email = request.session.get("reset_email")
                user = AdminLogin.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Password reset successful")
                return redirect("admin_login")
            else:
                messages.error(request, "Passwords do not match")
        else:
            messages.error(request, "Invalid OTP")
    return render(request, "admin/validate_otp.html")


# Admin Panel :- Product List,Add Product Category, Add Product,Update Product,Delete Product


def listProduct(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    products = Product.objects.all()
    admin_right = user.admin_right  # Fetch admin_right value

    return render(
        request,
        "admin/product_list.html",
        {"products": products, "admin_right": admin_right},  # Pass this to the template
    )


def listCategory(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")
    category = Category.objects.all()
    admin_right = user.admin_right  # Fetch admin_right value
    return render(
        request,
        "admin/category_list.html",
        {"category": category, "admin_right": admin_right},  # Pass this to the template
    )


def category_update(request, p_id):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")
    catObj = get_object_or_404(Category, cat_id=p_id)
    form = CategoryForm(instance=catObj)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=catObj)
        if form.is_valid():
            form.save()
            return redirect("listCategory")
    return render(request, "admin/category_update.html", {"form": form})


def category_delete(request, p_id):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")
    obj = get_object_or_404(Category, cat_id=p_id)
    if request.method == "GET":
        obj.delete()
        return redirect("listCategory")
    return redirect("admin_index")


def product_update(request, p_id):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")
    productObj = get_object_or_404(Product, product_id=p_id)
    form = ProductForm(instance=productObj)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=productObj)
        if form.is_valid():
            form.save()
            return redirect("listProduct")
    return render(request, "admin/product_update.html", {"form": form})


def product_delete(request, p_id):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")
    obj = get_object_or_404(Product, product_id=p_id)
    if request.method == "GET":
        obj.delete()
        return redirect("listProduct")
    return redirect("admin_index")


def add_productCategory(request):
    username = request.session.get("username")

    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    # Check if the user has admin rights
    if not user.admin_right:
        messages.error(
            request,
            "You do not have the necessary admin rights to add a product category.",
        )
        return redirect(
            "admin_index"
        )  # Redirect to the admin index or an appropriate page

    if request.method == "POST":
        category_name = request.POST.get("cat_name")
        category_description = request.POST.get("cat_decs")

        # Create and save the new category
        category = Category(
            cat_name=category_name, cat_description=category_description
        )
        category.save()

        messages.success(request, "Product category added successfully.")
        return redirect("listCategory")  # Redirect after successful submission

    return render(request, "admin/add_productCategory.html")


def add_product(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    if not user.admin_right:
        messages.error(
            request,
            "You do not have the necessary admin rights to add a products.",
        )
        return redirect(
            "admin_index"
        )  # Redirect to the admin index or an appropriate page

    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        brand = request.POST.get("brand")
        price = request.POST.get("price")
        color = request.POST.get("color")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        stock = request.POST.get("stock")


        # Fetch the category object
        category = Category.objects.get(cat_id=category_id)

        # Create the Product instance
        product = Product(
            product_name=name,
            category=category,
            brand=brand,
            price=price,
            color=color,
            product_desc=description,
            image=image,
            stock=stock
        )
        product.save()
        messages.success(request, "Product added successfully.")
        return redirect("listProduct")

    # Fetch all categories to populate the dropdown
    categories = Category.objects.all()
    return render(request, "admin/add_product.html", {"categories": categories})

def orderList(request):
    username = request.session.get("username")

    # Verify if the user exists and has admin rights
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    if not user.admin_right:
        messages.error(request, "You do not have the necessary admin rights.")
        return redirect("admin_index")

    # Filter out orders with null or empty required fields
    orders = Order.objects.all()

    if orders.exists():
        return render(request, "admin/view_order.html", {"orders": orders})
    else:
        messages.info(request, "No orders found.")
        return render(request, "admin/view_order.html", {"orders": []})
    

# Approve or cancel order
def approve_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.status = 'PROCESSING'
    order.save()
    # messages.success(request, 'Order has been approved successfully.')
    return redirect('orderList')  # Adjust the redirect URL as per your view name.

def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if order.status != 'CANCELED':  # Only proceed if the order is not already canceled
        order.status = 'CANCELED'
        order.save()
        
        # Increment the product's stock by the quantity in the order
        product = order.product
        product.stock += order.quantity
        product.save()
        
        # messages.success(request, 'Order has been canceled successfully.')

    return redirect('orderList')  # Adjust the redirect URL as per your view name


def listAdmin(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    # Check if the current user has admin rights
    if not user.admin_right:
        messages.error(request, "You do not have the necessary admin rights.")
        return redirect("admin_index")

    # Fetch all admin records
    adminRegister = AdminLogin.objects.all()

    return render(
        request,
        "admin/view_adminList.html",
        {"adminRegister": adminRegister, "admin_right": user.admin_right},
    )


def update_admin(request, p_id):
    username = request.session.get("username")

    # Check if the user is logged in and has admin rights
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    # Get the admin object to update
    adminObj = get_object_or_404(AdminLogin, id=p_id)

    if request.method == "POST":
        # Get data from the request
        username = request.POST.get("username")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        admin_right = (
            request.POST.get("admin_right") == "True"
        )  # Convert string to boolean

        # Update the admin object
        adminObj.username = username
        adminObj.email = email
        adminObj.contact = contact
        adminObj.admin_right = admin_right
        adminObj.save()  # Save changes

        messages.success(request, "Admin details updated successfully.")
        return redirect("listAdmin")

    return render(
        request,
        "admin/update_admin_detail.html",
        {"form": AdminRegistrationForm(instance=adminObj)},
    )


def delete_admin(request, admin_id):
    username = request.session.get("username")

    # Check if the user is logged in and has admin rights
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    if not user.admin_right:
        messages.error(
            request, "You do not have the necessary admin rights to delete an admin."
        )
        return redirect(
            "admin_index"
        )  # Redirect to the admin index or an appropriate page

    # Get the admin object to delete
    adminObj = get_object_or_404(AdminLogin, id=admin_id)
    adminObj.delete()
    messages.success(request, "Admin deleted successfully.")
    return redirect("listAdmin")  # Redirect to the admin list page


def listFeedback(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    # Check if the current user has admin rights
    if not user.admin_right:
        messages.error(request, "You do not have the necessary admin rights.")
        return redirect("admin_index")

    # Fetch all admin records
    feedback = Contact.objects.all()

    return render(
        request,
        "admin/view_feedback.html",
        {"feedback": feedback, "admin_right": user.admin_right},
    )



#Inventory
# def inventory_list_view(request):
#     # Fetch all inventory records with related product data
#     inventory_list = Inventory.objects.select_related('product__category').all()
#     return render(request, 'admin/inventory.html', {'inventory_list': inventory_list})

def inventory_list_view(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    products = Product.objects.all()
    admin_right = user.admin_right  # Fetch admin_right value

    return render(
        request,
        "admin/inventory.html",
        {"products": products, "admin_right": admin_right},  # Pass this to the template
    )


def inventory_update(request, p_id):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")
    productObj = get_object_or_404(Product, product_id=p_id)
    form = ProductForm(instance=productObj)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=productObj)
        if form.is_valid():
            form.save()
            return redirect("inventory_list")
    return render(request, "admin/product_stock_update.html", {"form": form})


# Bulk Upload
def bulkuploadview(request):
    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    # Check if the current user has admin rights
    if not user.admin_right:
        messages.error(request, "You do not have the necessary admin rights.")
        return redirect("admin_index")
    
    return render(request,"admin/bulkupload.html")

def bulkupload(request):

    username = request.session.get("username")
    try:
        user = AdminLogin.objects.get(username=username)
    except AdminLogin.DoesNotExist:
        return redirect("admin_login")

    # Check if the current user has admin rights
    if not user.admin_right:
        messages.error(request, "You do not have the necessary admin rights.")
        return redirect("admin_index")

    if request.method == "POST":
        upload_type = request.POST.get('upload_type')
        
        try:
            # Get the uploaded CSV file
            csvfile = request.FILES["csvfile"]
            
            # Read and decode the CSV file
            data = io.TextIOWrapper(csvfile.file, encoding='utf-8')
            reader = csv.DictReader(data)

            # Check if the user selected Category or Product for upload
            if upload_type == "category":
                categories = [
                    Category(cat_name=row["cat_name"], cat_description=row["cat_description"])
                    for row in reader if row["cat_name"] and row["cat_description"]
                ]
                if categories:
                    Category.objects.bulk_create(categories)
                    return HttpResponse("Categories successfully uploaded and saved.")
                else:
                    return HttpResponse("No valid categories found.", status=400)

            elif upload_type == "product":
                products = [
                    Product(
                        product_name=row["product_name"], 
                        product_desc=row["product_desc"], 
                        price=row["price"], 
                        color=row["color"], 
                        brand=row["brand"], 
                        category_id=row["category_id"]  # Ensure category_id is included in CSV
                    )
                    for row in reader if row["product_name"] and row["price"] and row["category_id"]
                ]
                if products:
                    Product.objects.bulk_create(products)
                    return HttpResponse("Products successfully uploaded and saved.")
                else:
                    return HttpResponse("No valid products found.", status=400)
            
            return HttpResponse("Invalid upload type selected.", status=400)

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return HttpResponse("Invalid request method.", status=405)


def export_to_excel(request):
    # Create a new Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Categories and Products"

    # Add header row
    sheet.append(["Category ID", "Category Name", "Product Name", "Price", "Color", "Brand"])

    # Fetch categories and their products
    categories = Category.objects.all()

    # Loop through categories and their related products
    for category in categories:
        products = Product.objects.filter(category=category)
        if products.exists():
            for product in products:
                sheet.append([category.cat_id, category.cat_name, product.product_name, product.price, product.color, product.brand])
        else:
            # If no products exist for the category, still show the category
            sheet.append([category.cat_id, category.cat_name, "No products", "-", "-", "-"])

    # Save the workbook to a bytes buffer
    from io import BytesIO
    response = BytesIO()
    workbook.save(response)
    response.seek(0)

    # Prepare the response to download the Excel file
    response_excel = HttpResponse(response, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response_excel['Content-Disposition'] = 'attachment; filename=categories_products.xlsx'

    return response_excel