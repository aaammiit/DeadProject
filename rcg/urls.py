"""
URL configuration for Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .import views as v

urlpatterns = [
    path('typeNews1/<str:typ>',v.rcgType),
    path('formFilter1',v.rccfilterData),
    # path('yearData',v.yearData),
    path('findrccCountry/<str:cntry>',v.findrccCountry),
    path('findrccReg/<str:reg>',v.findrccReg),
    path('rccrbProfile/<int:id>',v.rccRb),
    
]
