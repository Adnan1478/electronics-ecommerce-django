from django import forms
from .models import Product, Category, Contact, Cart, Order


class ProductForm(forms.ModelForm):
    product_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Product Name",
            }
        ),
        label="Product Name",
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "input",
            }
        ),
        label="Category",
    )

    brand = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Brand",
            }
        ),
        label="Brand",
    )

    price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Price",
            }
        ),
        label="Price",
    )

    color = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Color",
            }
        ),
        label="Color",
    )

    product_desc = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input",
                "placeholder": "Enter Description",
            }
        ),
        label="Description",
        required=False,
    )

    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "input",
            }
        ),
        label="Product Image",
        required=False,
    )

    # New Stock Field
    stock = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Stock",
            }
        ),
        label="Stock",
        required=False,  # Set to True if you want to make it required
    )

    class Meta:
        model = Product
        fields = [
            "product_name",
            "category",
            "brand",
            "price",
            "color",
            "product_desc",
            "image",
            "stock",  # Include stock in the fields list
        ]

class CategoryForm(forms.ModelForm):
    cat_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Product Name",
            }
        ),
        label="Product Name",
    )

    cat_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "textarea",
                "placeholder": "Enter Description",
            }
        ),
        label="Description",
        required=False,
    )

    class Meta:
        model = Category
        fields = ["cat_name", "cat_description"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["full_name", "email", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Enter full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "example@example.com"}),
            "subject": forms.TextInput(attrs={"placeholder": "Title of your message"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Your message here", "rows": 4}
            ),
        }


class OrderForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input",
                "rows": 4,
                "placeholder": "Enter Address",
            }
        ),
        label="Address",
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter City",
            }
        ),
        label="City",
    )

    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter State",
            }
        ),
        label="State",
    )

    zip_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Zip Code",
            }
        ),
        label="Zip Code",
    )

    contact = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Contact Number",
            }
        ),
        label="Contact",
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Enter Full Name",
            }
        ),
        label="Full Name",
    )

    class Meta:
        model = Order
        fields = ["address", "city", "state", "zip_code", "contact", "name"]