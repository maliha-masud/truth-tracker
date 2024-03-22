from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"), #call views' home function, allow us to view the HTTP response returned; when empty string path
    path("input/", views.input, name = "input"),
    path("login_form.html", views.login_form, name = "login_form"),
    path("signin/", views.signin, name = "signin_pg"),
    path("about-dataset/", views.about_dataset, name = "about_dataset"),
    path("results/", views.output, name = "results"),
    path("project-overview/", views.project_overview, name = "project-overview"),
    path("user-manual/", views.user_manual, name = "user-manual"),
    path("faq/", views.faq, name = "faq"),

    path('process-text/', views.process_text),
]
