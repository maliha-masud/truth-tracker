from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"), #call views' home function, allow us to view the HTTP response returned; when empty string path
    path("input/", views.input, name = "input"),
    path("login_form.html", views.login_form, name = "login_form"),
    path("signin/", views.signin, name = "signin_pg"),
    path("about-dataset/", views.about_dataset, name = "about_dataset"),

    path('process-text/', views.process_text),
]