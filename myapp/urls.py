
from django.urls import path

from myapp.views import home

app_name="myapp"
urlpatterns = [
    path('',home,name="home"),
]
