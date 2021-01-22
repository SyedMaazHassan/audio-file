from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('add-song', views.add_song, name="add-song"),
    path('play/<song_name>', views.play, name="play"),
    path('mark_as_favorite', views.mark_as_favorite, name="mark_as_favorite"),
    path('add-to-playlist', views.add_to_playlist, name="add-to-playlist")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
