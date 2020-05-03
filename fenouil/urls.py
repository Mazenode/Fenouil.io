from django.contrib import admin
from django.urls import path, include
from . import views, settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name="accueil"),
    path('articles/', views.articles, name="articles"),
    path('individu/', views.individu, name="individu"),
    path('login/', views.login, name='login'),
    path('envoi_mail/', views.envoi_mail, name='envoi_mail'),
    path('envoi_SMS/', views.envoi_SMS, name='envoi_SMS'),
    path('envoi_papier/', views.envoi_papier, name='envoi_papier'),
    path('creer_individu/', views.creer_individu, name='creer_individu'),
    path('liste_anomalies/', views.liste_anomalies, name='liste_anomalies'),
    path('creer_cible_routage/<int:etape>/', views.creer_cible_routage, name='creer_cible_routage'),
    path('valider_cible_routage/', views.valider_cible_routage, name='valider_cible_routage'),
    path('saisir_commande/', views.saisir_commande, name='saisir_commande'),
    path('signaler_anomalie/', views.signaler_anomalie, name='signaler_anomalie'),
    path('accounts/', include('account.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)