
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from API.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.obtain_auth_token,name='api-token-auth'),
    path('signup/', RegisterView.as_view(), name='auth_register'),
    path('', include('API.urls'))
]
