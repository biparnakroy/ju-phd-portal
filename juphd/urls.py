"""juphd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from juphd import settings , dev_settings


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', include('juphd_app.urls')),
]
if settings.DEBUG == None or settings.DEBUG == True:
  urlpatterns += static(dev_settings.STATIC_URL, document_root=dev_settings.STATICFILES_DIRS)
  urlpatterns += static(dev_settings.MEDIA_URL, document_root=dev_settings.MEDIA_ROOT)
