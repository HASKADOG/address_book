from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add_address", views.add_address, name="add_address"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("delete_address", views.delete_address, name="delete_address"),
    path("edit_address/<int:address_id>", views.edit_address, name="edit_address"),
    path("register", views.register, name="register"),
    path("error/<str:error_message>", views.error, name="error"),
]
