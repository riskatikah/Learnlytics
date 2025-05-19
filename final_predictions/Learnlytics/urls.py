#from django.contrib import admin
from django.urls import path
from . import views
#from .views import search_result
#from . import admin_views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name ='about'),
    
]
