from django.views import View
from rest_framework import generics
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import detail
from django.views.generic import list
from django.views.generic import edit
from rest_framework import generics, parsers
from rest_framework.response import Response

from .models import Game
from .serializers import GameSerializer

# Create your views here.


class GameCreateView(generics.CreateAPIView):
    # parser_classes = (parsers.JSONParser,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        game = self.request.data
        _ = serializer.save(game=game)
        return Response(_)


class GameListView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        game = serializer.save()


def show_html(request):
    return render(request, 'gomoku_project/templates/test.html')


class simpleView(View):
    def get(self, request):
        return render(request, 'gomoku_project/templates/test_bootstrap.html')
