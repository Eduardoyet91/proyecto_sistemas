from django.contrib import admin
from django.urls import include
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
