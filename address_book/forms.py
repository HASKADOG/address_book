from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AddAddressForm(forms.Form):
    """
    Address creation form
    Also used for address editing
    """

    address = forms.CharField(label="Address", max_length=300)


class DeleteAddressForm(forms.Form):
    """
    Address deletion form
    """

    address_id = forms.IntegerField(label="address_id")


class LoginForm(forms.Form):
    """
    User authentication form
    """

    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(label="password", max_length=30)


class CreateUserForm(UserCreationForm):
    """
    User registration form
    """

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
