from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views

urlpatterns = [
    path('', views.agent_login, name='agent_login'),
    path('logout/', views.agent_logout, name='agent_logout'),

    path('dashboard/',views.dashboard, name='dashboard'),
    path('properties/', views.property_list, name='property_list'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)