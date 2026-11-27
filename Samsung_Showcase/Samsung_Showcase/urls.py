"""
URL configuration for Samsung_Showcase project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Samsung_App.urls")),
]