from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('web.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
]
