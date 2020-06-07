from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# all urlpaths associated with the user part of the website
urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form, name='form'),
    path("otp/<str:pk>", views.otp, name="otp"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
