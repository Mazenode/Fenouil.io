from django.contrib import admin
from django.urls import path, include
from . import views, settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name="accueil"),
    path('articles/', views.articles, name="articles"),
    path('client/', views.client, name="client"),
    path('login/', views.login, name='login'),
    path('accounts/', include('account.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)