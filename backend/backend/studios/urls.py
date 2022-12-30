from . import views
from classes.views import EnrolAPIView, DropAPIView, EnrolMultipleAPIView, DropMultipleAPIView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = 'studios'
urlpatterns = [
    path('', views.StudioListAPIView.as_view()),
    path('search/', views.StudioSearchAPIView.as_view()),
    path('<int:pk>/', views.StudioDetailAPIView.as_view(), name='studio-detail'),
    path('<int:pk>/classes/', views.ClassListAPIView.as_view()),
    path('<str:studio_id>/classes/<int:class_id>/enrol/', EnrolAPIView.as_view()),
    path('<str:studio_id>/classes/<int:class_id>/enrol/multiple', EnrolMultipleAPIView.as_view()),
    path('<str:studio_id>/classes/<int:class_id>/drop/', DropAPIView.as_view()),
    path('<str:studio_id>/classes/<int:class_id>/drop/multiple', DropMultipleAPIView.as_view()),
    path('nearme/', views.NearbyStudioListAPIView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
