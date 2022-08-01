from datetime import datetime

import pytz
from django.conf import settings as s
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from google_maps_integration import GoogleMapsManager
from .forms import AddAddressForm, LoginForm, DeleteAddressForm, CreateUserForm
from .models import Address


def register(request):
    """
    Registers a new user
    """

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("address_book:index")

    context = {"form": form}

    return render(request, "address_book/register.html", context)


def error(request, error_message):
    """
    Error page for custom error messages
    """

    return render(
        request, "address_book/error_handling.html", context={"error": error_message}
    )


def login_user(request):
    """
    Users authentication
    """
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)

                return redirect("address_book:index")
            else:
                return redirect(
                    f"/error/User '{username}' does not exist or the password is incorrect"
                )

    return render(request, "address_book/login.html")


def logout_user(request):
    """
    Logout
    """
    logout(request)

    return redirect("address_book:login")


@login_required(login_url="address_book:login")
def index(request):
    """
    The main page
    """
    addresses = Address.objects.filter(owner=request.user.id)

    context = {
        "addresses": addresses,
        "user": request.user,
        "api_key": s.GMAPS_API_KEY,
    }

    return render(request, "address_book/index.html", context)


@login_required(login_url="address_book:login")
def add_address(request):
    """
    Address creation form
    Uses google maps api for address correction
    """

    if request.method == "POST":
        form = AddAddressForm(request.POST)

        if form.is_valid():
            GMaps = GoogleMapsManager(api_key=s.GMAPS_API_KEY)

            address = Address(
                raw_address=form.cleaned_data["address"],
                address=GMaps.geocode(form.cleaned_data["address"])["results"][0][
                    "formatted_address"
                ],
                creation_date=datetime.now(tz=pytz.UTC),
                owner=request.user,
            )

            address.save()

            return redirect("address_book:index")


@login_required(login_url="address_book:login")
def edit_address(request, address_id):
    """
    Address edit forms
    Uses google maps api for address correction
    """

    try:
        address = Address.objects.filter(id=address_id).get()
    except Address.DoesNotExist:
        return redirect("/error/This address does not exist!")

    if address.owner.id != request.user.id:
        return redirect("/error/This address belongs to another user!")

    if request.method == "POST":
        form = AddAddressForm(request.POST)

        if form.is_valid():
            GMaps = GoogleMapsManager(api_key=s.GMAPS_API_KEY)

            address.raw_address = form.cleaned_data["address"]
            address.address = GMaps.geocode(form.cleaned_data["address"])["results"][0][
                "formatted_address"
            ]
            address.creation_date = datetime.now(tz=pytz.UTC)
            address.owner = request.user

            address.save()

            return redirect("address_book:index")

    contex = {"address": address}

    return render(request, "address_book/edit_address.html", contex)


@login_required(login_url="address_book:login")
def delete_address(request):
    """
    Address delete
    """
    if request.method == "POST":
        form = DeleteAddressForm(request.POST)

        if form.is_valid():
            try:
                address = Address.objects.filter(
                    id=form.cleaned_data["address_id"]
                ).get()
            except Address.DoesNotExist:
                return redirect("/error/This address does not exist!")

            if address.owner.id != request.user.id:
                return redirect("/error/This address belongs to another user!")

            address.delete()

            return redirect("address_book:index")
