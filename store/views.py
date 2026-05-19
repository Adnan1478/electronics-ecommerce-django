from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Product, Cart, Login, Order,Category,UserUpload
from .forms import ContactForm, OrderForm
from django.utils import timezone
from django.contrib import messages

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def index(request):
    products = Product.objects.all()[:6]  # Fetch all products
    username = request.session.get("username")  # Retrieve username from session
    return render(request, "index.html", {"username": username, "products": products})


def product(request):
    # products = Product.objects.all()  # Fetch all products
    # return render(request, "store/product.html", {"products": products})
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(product_name__icontains=query) | 
            Q(product_desc__icontains=query) |
            Q(category__cat_name__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()  # Fetch all categories for the dropdown
    return render(request, 'store/product.html', {'products': products, 'categories': categories})


def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(product_name__icontains=query) | 
            Q(product_desc__icontains=query) |
            Q(category__cat_name__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()  # Fetch all categories for the dropdown
    return render(request, 'store/searching_product.html', {'products': products, 'categories': categories})

# def profile(request):
#     username = request.session.get("username")
#     try:
#         user = Login.objects.get(username=username)
#     except Login.DoesNotExist:
#         return redirect("login")  # Redirect to login page if user not found
#     return render(request, "store/user_profile.html",{"username": username})


def upload_profile_image(request):
    if request.method == "POST":
        # Get the user based on the session
        username = request.session.get("username")
        user = get_object_or_404(Login, username=username)

        # Get or create a UserUpload instance for the user
        user_upload, created = UserUpload.objects.get_or_create(uid=user)

        # Handle the file upload
        profile_image = request.FILES.get('image')
        if profile_image:
            user_upload.image = profile_image
            user_upload.save()  # Save the new image
            messages.success(request, "Profile image updated successfully!")
        else:
            messages.error(request, "Failed to upload image.")

        return redirect('profile')  # Redirect back to the profile page

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact")  # Replace with your actual success URL
    else:
        form = ContactForm()
    return render(request, "store/contact.html", {"form": form})

def add_to_cart(request, product_id):
    # Fetch the username from the session
    username = request.session.get("username")

    # Fetch the corresponding user from the Login model
    try:
        user = Login.objects.get(username=username)
    except Login.DoesNotExist:
        return redirect("login")  # Redirect to login page if user not found

    # Fetch the product by ID
    product = get_object_or_404(Product, product_id=product_id)
    
    # Get the quantity from the request (default is 1 if not provided)
    quantity = int(request.POST.get("quantity", 0))
    

    # Check if the product already exists in the cart for this user
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        customer=user,
        defaults={"quantity": quantity}
    )

    if not created:
        # If the cart item already exists, increase the quantity
        cart_item.quantity += quantity 
        # cart_item.quantity -=1
        cart_item.save()

    return redirect("view_cart")  # Redirect to the cart view page

def orderproduct(request):
    username = request.session.get("username")
    
    # Fetch the orders for the logged-in customer
    orders = Order.objects.filter(customer__username=username)
    
    # Calculate total price for each order
    for order in orders:
        order.total_price = order.quantity * order.product.price  # quantity * price

    context = {
        'orders': orders,
    }

    return render(request, "store/orderproduct.html", context)

def view_cart(request):
    username = request.session.get("username")
    try:
        user = Login.objects.get(username=username)
    except Login.DoesNotExist:
        return redirect("login")

    cart_items = Cart.objects.filter(customer=user)

    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    context = {
        "cart_items": cart_items,
    }
    return render(request, "store/addtocart.html", context)

def remove_from_cart(request, item_id):
    # Fetch the username from the session
    username = request.session.get("username")

    # Fetch the corresponding user from the Login model
    try:
        user = Login.objects.get(username=username)
    except Login.DoesNotExist:
        return redirect("login")  # Redirect to login page if user not found

    # Get the cart item associated with the user and the specific item_id
    cart_item = get_object_or_404(Cart, cart_id=item_id, customer=user)

    # Delete the cart item
    cart_item.delete()

    return redirect("view_cart")  # Redirect to the cart view page



def buy_product(request, item_id):
    # Fetch the cart item based on item_id
    cart_item = get_object_or_404(Cart, cart_id=item_id)

    # Fetch the username from the session
    username = request.session.get("username")
    user = get_object_or_404(Login, username=username)

    # Check for user's details in UserUpload
    user_details = UserUpload.objects.filter(uid=user).first()  # Use .filter().first() to avoid errors

    # Redirect to user profile if any detail is missing or no profile exists
    if not user_details or (not user_details.name or not user_details.contact or
            not user_details.address or not user_details.city or
            not user_details.state or not user_details.country or
            not user_details.zip_code):
        messages.error(request, "Update your profile details to proceed with the order.")
        return redirect("profile")  # Redirect to profile if details are missing

    # Check if enough stock is available
    if cart_item.product.stock < cart_item.quantity:
        messages.error(request, "Not enough stock available for this product.")
        return redirect("view_cart")  # Redirect to the cart if stock is insufficient

    # Calculate total price
    total_price = cart_item.product.price * cart_item.quantity

    # Initialize Razorpay Client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay Order
    amount_in_paise = int(total_price * 100)
    data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": f"receipt_order_{item_id}_{int(timezone.now().timestamp())}",
    }

    try:
        razorpay_order = client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']
    except Exception as e:
        messages.error(request, f"Error generating Razorpay order: {str(e)}")
        return redirect("view_cart")

    # Create the pending order in our database
    order = Order.objects.create(
        customer=user,
        product=cart_item.product,
        quantity=cart_item.quantity,
        user_details=user_details,
        status='PENDING',
        razorpay_order_id=razorpay_order_id,
        created_at=timezone.now()
    )

    context = {
        "cart_item": cart_item,
        "order": order,
        "user_details": user_details,
        "razorpay_order_id": razorpay_order_id,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount_paise": amount_in_paise,
        "total_price": total_price,
        "user_email": user.email,
        "user_contact": user_details.contact,
        "user_name": user_details.name,
    }

    # Redirect to Razorpay payment page
    return render(request, "store/checkout.html", context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")
        cart_item_id = request.POST.get("cart_item_id")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify payment signature
            client.utility.verify_payment_signature(params_dict)

            # Retrieve and update the order
            order = get_object_or_404(Order, razorpay_order_id=order_id)
            order.status = 'PROCESSING'
            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.save()

            # Deduct product stock
            product = order.product
            product.stock -= order.quantity
            product.save()

            # Remove product from cart
            if cart_item_id:
                try:
                    cart_item = Cart.objects.get(cart_id=cart_item_id)
                    cart_item.delete()
                except Cart.DoesNotExist:
                    pass

            messages.success(request, "Payment successful! Your order has been placed.")
            return render(request, "store/payment_success.html", {
                "order": order,
                "payment_id": payment_id
            })

        except Exception as e:
            # Handle payment verification failure
            try:
                order = Order.objects.get(razorpay_order_id=order_id)
                order.status = 'FAILED'
                order.save()
            except Order.DoesNotExist:
                pass
            
            messages.error(request, f"Payment signature verification failed: {str(e)}")
            return render(request, "store/payment_failed.html", {
                "error": str(e)
            })

    return redirect("view_cart")



def view_order(request, p_id):
    try:
        # Fetch the order based on the provided order_id (p_id)
        view_order = Order.objects.get(order_id=p_id)
        
        # Calculate total price for the order
        total_price = view_order.quantity * view_order.product.price  # quantity * price
        
        context = {
            'order': view_order,
            'total_price': total_price  # Pass the total price to the template
        }
        
        return render(request, "store/view_order.html", context)
    
    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist
        return render(request, "store/error.html", {'message': 'Order not found.'})
    
def download_bill(request, order_id):
    # Fetch the order details
    order = Order.objects.get(order_id=order_id)

    # Calculate total price (quantity * price)
    total_price = order.quantity * order.product.price

    # Render the HTML template to a string with the total price in context
    template_path = 'store/order_bill_template.html'
    context = {
        'order': order,
        'total_price': total_price  # Pass the total price to the template
    }
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{order_id}_{order.product.product_name}_bill.pdf"'

    # Convert the HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If there's an error in PDF creation, display an error message
    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>')

    return response

def user_cancel_order(request, order_id):
    username = request.session.get("username")
    
    if username:
        user = get_object_or_404(Login, username=username)
        
        try:
            # Fetch the order based on the order_id and user
            order = Order.objects.get(order_id=order_id, customer=user)
            
            if order.status != "CANCELED":  # Only proceed if the order is not already canceled
                order.status = "CANCELED"  # Set the status to 'CANCELED'
                order.save()  # Save the order changes
                
                # Increment the product's stock by the order quantity
                product = order.product
                product.stock += order.quantity
                product.save()
            
            return redirect('orderproduct')  # Redirect to the orders page
        
        except Order.DoesNotExist:
            return render(request, "store/error.html", {'message': 'Order not found.'})
    
    return redirect('login')  # Redirect to login if user is not found




def profile(request):
    username = request.session.get("username")  # Retrieve username from session
    user_upload = UserUpload.objects.filter(uid__username=username).first()  # Get user upload details

    if request.method == "POST":
        # Update user details
        if user_upload:
            user_upload.name = request.POST.get("name", "")
            user_upload.contact = request.POST.get("contact", "")
            user_upload.address = request.POST.get("address", "")
            user_upload.city = request.POST.get("city", "")
            user_upload.state = request.POST.get("state", "")
            user_upload.country = request.POST.get("country", "")
            user_upload.zip_code = request.POST.get("zip_code", "")
            user_upload.save()
        else:
            # Create a new UserUpload if it doesn't exist
            UserUpload.objects.create(
                uid=Login.objects.get(username=username),
                name=request.POST.get("name", ""),
                contact=request.POST.get("contact", ""),
                address=request.POST.get("address", ""),
                city=request.POST.get("city", ""),
                state=request.POST.get("state", ""),
                country=request.POST.get("country", ""),
                zip_code=request.POST.get("zip_code", ""),
            )
        return redirect('profile')  # Redirect to the profile page after saving

    return render(request, "store/user_profile.html", {
        "username": username,
        "user_upload": user_upload,
    })