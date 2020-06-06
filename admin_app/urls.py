from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.sign_in_up, name='sign_in_up'),
    path('login', views.manager_login, name='manager_login'),
    path('register', views.manager_register, name='manager_register'),
    path('logout',views.manager_logout,name='manager_logout'),
    path('admin_page', views.admin_page, name='admin_page'),
    path('profile/<int:key>/', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
