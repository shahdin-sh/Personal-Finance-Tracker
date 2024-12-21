# In your app's urls.py
from django.urls import path
from .views import HelloTest


urlpatterns = [
    path('', HelloTest.as_view(), name='hello_test'),
]