from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.upload_document, name='upload_document'),
    path('search/', views.search_documents, name='search_documents'),
    path('register/', views.register_user, name='register_user'),
    path('verify-otp/', views.verify_otp_login, name='verify_otp'),
    path('documents/<int:document_id>/verify/', views.verify_document, name='verify_document'),
]
