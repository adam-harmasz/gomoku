"""gomoku_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from gomoku_project.views import GameListView, GameCreateView, show_html, simpleView
from gomokufiles.views import UploadFile, UploadedGameView, MainView, GamesListView, GameDelete, LoginView, LogoutView,\
    RegistrationView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/$', show_html, name='test'),
    url(r'^create/$', GameCreateView.as_view()),
    url(r'^test2/$', simpleView.as_view()),

    ################ gomokufiles urls ######################

    url(r'^main/$', MainView.as_view()),
    url(r'^file-test/$', UploadFile.as_view()),
    url(r'^game-record/(?P<id>(\d)+)/$', UploadedGameView.as_view()),
    url(r'^game-list/$', GamesListView.as_view()),
    url(r'^delete-game/(?P<pk>(\d)+)/$', GameDelete.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^registration/$', RegistrationView.as_view()),
]
