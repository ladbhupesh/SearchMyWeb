"""URLs for the server_status app."""
from django.urls import path

from server_status import views


urlpatterns = (
    path('', views.status, name='status'),
)
