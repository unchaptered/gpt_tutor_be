"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to configs. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function configs
    1. Add an import:  from my_app import configs
    2. Add a URL to urlpatterns:  path('', configs.home, name='home')
Class-based configs
    1. Add an import:  from other_app.configs import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
