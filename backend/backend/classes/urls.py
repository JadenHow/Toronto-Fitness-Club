from django.urls import path

from . import views

app_name = 'classes'
urlpatterns = [
    path('search/', views.class_search_view),
]
