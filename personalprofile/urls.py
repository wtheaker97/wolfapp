from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("create-profile/", views.create_profile, name="create_profile"),
    path("view-profile/", views.view_profile, name="view_profile"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("delete-profile/", views.delete_profile, name="delete_profile"),
]
