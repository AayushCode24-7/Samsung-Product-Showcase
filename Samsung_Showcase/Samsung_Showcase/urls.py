"""
URL configuration for Samsung_Showcase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Home page route (matches name='home' from your navbar)
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Routes corresponding to your navbar link names to fix NoReverseMatch errors
    path('shop/', TemplateView.as_view(template_name='shop.html'), name='Shop'),
    path('phones/', TemplateView.as_view(template_name='phone.html'), name='Phone'),
    path('wearables/', TemplateView.as_view(template_name='wearables.html'), name='Wearables'),
    path('tv-av/', TemplateView.as_view(template_name='tv.html'), name='Tv'),
    path('appliances/', TemplateView.as_view(template_name='appliances.html'), name='Appliances'),
    path('pc-monitors/', TemplateView.as_view(template_name='pc.html'), name='Pc'),
]