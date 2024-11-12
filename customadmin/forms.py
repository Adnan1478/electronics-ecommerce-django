from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from store.models import AdminLogin


class AdminRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Enter Username",
            }
        ),
        label="Username",
    )

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "type": "email",
                "placeholder": "Enter Email",
            }
        ),
        label="Email",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "type": "password",
                "placeholder": "Enter Password",
                "id": "id_password1",
            }
        ),
        label="Password",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "type": "password",
                "placeholder": "Re-enter Password",
                "id": "id_password2",
            }
        ),
        label="Confirm Password",
    )

    contact = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Enter Contact Number",
            }
        ),
        label="Contact",
    )

    admin_right = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "radio-input"}),
        choices=[(True, "Yes"), (False, "No")],
        label="Admin Rights",
    )

    class Meta:
        model = AdminLogin
        fields = ("username", "email", "password1", "password2", "contact", 'admin_right')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

    def save(self, commit=True):
        user = super(AdminRegistrationForm, self).save(commit=False)
        user.password = make_password(
            self.cleaned_data["password1"]
        )  # Use password1 for hashing
        if commit:
            user.save()
        return user


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Enter Username",
            }
        ),
        label="Username",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "type": "password",
                "placeholder": "Enter Password",
                "id": "id_password",  # Add id to match the JavaScript function
            }
        ),
        label="Password",
    )
