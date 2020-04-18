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
    path('envoi_mail/', views.envoi_mail, name='envoi_mail'),
    path('envoi_SMS/', views.envoi_SMS, name='envoi_SMS'),
    path('envoi_papier/', views.envoi_papier, name='envoi_papier'),
    path('creer_client/', views.creer_client, name='creer_client'),
    path('liste_anomalies/', views.liste_anomalies, name='liste_anomalies'),
    path('signaler_anomalie/', views.signaler_anomalie, name='signaler_anomalie'),
    path('accounts/', include('account.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)