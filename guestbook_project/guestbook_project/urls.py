from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface URL
    path('admin/', admin.site.urls),

    # API endpoints under '/api/' namespace
    path('api/', include('guestbook.urls', namespace='guestbook')),
]
