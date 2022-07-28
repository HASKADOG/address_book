import requests
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.http import HttpResponseForbidden
from .models import Address
from .forms import AddAddressForm, LoginForm, DeleteAddressForm, CreateUserForm


def register(request):
    """
    Registers a new user
    """

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/")

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

                return redirect("/")
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

    return redirect("/login")


def index(request):
    """
    The main page
    """
    if not request.user.is_authenticated:
        return redirect("/login")

    addresses = Address.objects.filter(owner=request.user.id)

    context = {
        "addresses": addresses,
        "user": request.user,
        "api_key": "AIzaSyD2i-XugVBME63U6sMDyRmjfyLAGaVWOcM",
    }

    return render(request, "address_book/index.html", context)


def add_address(request):
    """
    Address creation form
    Uses google maps api for address correction
    """

    if request.method == "POST":
        form = AddAddressForm(request.POST)

        if form.is_valid():
            params = {
                "address": form.cleaned_data["address"],
                "key": "AIzaSyD2i-XugVBME63U6sMDyRmjfyLAGaVWOcM",
            }
            gmaps_request = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json", params=params
            ).json()

            if len(gmaps_request["results"]) < 1 or gmaps_request["status"] != "OK":
                return redirect(
                    f"/error/Please check if address '{form.cleaned_data['address']}' exists!"
                )

            address = Address(
                raw_address=form.cleaned_data["address"],
                address=gmaps_request["results"][0]["formatted_address"],
                creation_date=datetime.now(),
                owner=request.user,
            )

            address.save()

            return redirect("/")


def edit_address(request, address_id):
    """
    Address edit forms
    Uses google maps api for address correction
    """
    address = Address.objects.filter(id=address_id).get()
    if address.owner.id != request.user.id:
        return redirect("/error/This address belongs to another user!")

    if not address:
        return Http404("No addresses with this id!")

    if request.method == "POST":
        form = AddAddressForm(request.POST)

        if form.is_valid():
            params = {
                "address": form.cleaned_data["address"],
                "key": "AIzaSyD2i-XugVBME63U6sMDyRmjfyLAGaVWOcM",
            }
            gmaps_request = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json", params=params
            ).json()

            if len(gmaps_request["results"]) < 1 or gmaps_request["status"] != "OK":
                return redirect(
                    f"/error/Please check if address '{form.cleaned_data['address']}' exists!"
                )

            address.raw_address = form.cleaned_data["address"]
            address.address = gmaps_request["results"][0]["formatted_address"]
            address.creation_date = datetime.now()
            address.owner = request.user

            address.save()

            return redirect("/")

    contex = {"address": address}

    return render(request, "address_book/edit_address.html", contex)


def delete_address(request):
    """
    Address delete
    """
    if request.method == "POST":
        form = DeleteAddressForm(request.POST)

        if form.is_valid():
            address = Address.objects.filter(id=form.cleaned_data["address_id"]).get()

            if address.owner.id != request.user.id:
                return redirect("/error/This address belongs to another user!")

            address.delete()

            return redirect("/")
