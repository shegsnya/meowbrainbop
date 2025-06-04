from django.contrib import admin
from django.urls import path,include
from quiz import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'), 
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

