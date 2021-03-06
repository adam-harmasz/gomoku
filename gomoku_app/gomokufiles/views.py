from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
import re

from .forms import GomokuFileForm, LoginForm, RegistrationForm
from .models import GomokuFiles, GomokuUser


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        ctx = {
            'form': form,
        }
        return render(request, 'registration.html', ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password_1 = form.cleaned_data['password_1']
            password_2 = form.cleaned_data['password_2']
            email = form.cleaned_data['email']
            user = User.objects.filter(username=username)
            if user:
                ctx = {
                    'err': 'Podany login jest już zajęty',
                    'form': form,
                }
                return render(request, 'registration.html', ctx)
            else:
                if password_1 != password_2:
                    ctx = {
                        'form': form,
                        'err': "Podane hasła są różne!",
                    }
                    return render(request, 'registration.html', ctx)

                else:
                    user = User.objects.create_user(username=username, password=password_1, email=email)
                    login(request, user)
                    gomoku_user = GomokuUser.objects.create(user=user, email=email)
                    return HttpResponseRedirect('/login/')
        else:
            ctx = {
                'form': form,
                'err': 'form not valid'
            }
            return render(request, 'registration.html', ctx)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/main/')
        else:
            form = LoginForm()
            ctx = {
                'form': form,
            }
            return render(request, 'login_form.html', ctx)

    def post(self, request):
        form = LoginForm (request.POST)
        if form.is_valid ():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/main/')
            else:
                return render(request, "login_form.html", {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
            user_id = request.user.pk
            ctx = {
                'user_name': user_name,
            }
            return render(request, 'main.html', ctx)


class UploadFile(LoginRequiredMixin, View):
    def get(self, request):
        form = GomokuFileForm()
        if request.user.is_authenticated():
            user_name = request.user.username
        ctx = {
            'form': form,
            'user_name': user_name,
        }
        return render(request, 'upload_file.html', ctx)

    def post(self, request):
        form = GomokuFileForm(request.POST, request.FILES)
        if request.user.is_authenticated():
            user = GomokuUser.objects.get(user=request.user.id)

        if form.is_valid():
            gomoku_user = form.cleaned_data['gomoku_user']
            # if gomoku_user == 'private':
            #     gomoku_user = request.SESSION
            files = form.cleaned_data['files']
            gomoku_file = GomokuFiles(files=files)
            gomoku_file.save()

            with open('{}'.format(gomoku_file.files), 'r') as f:
                f_content = f.read()
                game_record = f_content.split('\n')
                only_record = []
                # using regex to filter players name, date and score knowing in which row of game record they will occur
                game_date_regex = r'[0-9]+\.[0-9]+\.[0-9]+'
                game_time_regex = r'[0-9]+\:[0-9]+\:[0-9]+'
                regex = r'\".+\"'
                player_regex_2 = r'[a-z0-9]+'
                score_regex = r'(1-0)|(0-1)'
                score = re.search(score_regex, game_record[6]).group()
                player_1 = re.search (player_regex_2, re.search(regex, game_record[4]).group()).group()
                player_2 = re.search (player_regex_2, re.search (regex, game_record[5]).group()).group()
                date = re.search (game_date_regex, re.search (regex, game_record[2]).group()).group()
                time = re.search (game_time_regex, re.search (regex, game_record[7]).group()).group()
                # Making list of only game record
                for item in game_record[-5:-1]:
                    only_record.append(item)
                better_record = []
                # using regex to find only move e.g.(a1, b2, etc.) and chose of colour from game record
                for item in only_record:
                    re_item = re.finditer (r'(white|black|[a-l][0-9]+)', format(item))
                    if re_item is not None:
                        for better_item in re_item:
                            temp_array = []
                            if better_item.group() != 'white' and better_item.group () != 'black' and better_item.group() != '--':
                                temp_array.append(re.search (r'[a-z]', better_item.group()).group())
                                temp_array.append(re.search (r'[0-9]+', better_item.group()).group())
                            else:
                                temp_array.append(better_item.group())
                            better_record.append(temp_array)
                # checking if players switched their colors during the game (after swap opening 2nd player can choose color)
                color_swap = 'yes'
                print(better_record[5], 'test color swapa')
                if better_record[3] == ['white'] or better_record[5] == ['black']:
                    print(better_record[5])
                    color_swap = 'no'
                print (color_swap)
                # removing black|white statements from the list so we have only moves in game record
                if ['black'] in better_record:
                    better_record.remove (['black'])
                    print ('usunięto black')
                elif ['white'] in better_record:
                    better_record.remove (['white'])
                    print ('usunięto white')

                # Add complete info about game to model
                gomoku_file.game_date = '({} {})'.format(date, time)
                gomoku_file.score = score
                gomoku_file.game_record = better_record
                gomoku_file.player_1 = player_1
                gomoku_file.player_2 = player_2
                gomoku_file.color_swap = color_swap
                gomoku_file.game_data = f_content
                gomoku_file.save()

                if gomoku_user == 'private':
                    gomoku_file.gomoku_user.add(user)
                    gomoku_file.save()

            return HttpResponseRedirect('/game-record/{}'.format(gomoku_file.id))
        else:
            form = GomokuFileForm()
        ctx = {
            'form': form,
        }
        return render(request, 'upload_file.html', ctx)


class UploadedGameView(LoginRequiredMixin, View):
    def get(self, request, id):
        gomoku_file = GomokuFiles.objects.get(pk=id)
        player_1 = gomoku_file.player_1
        player_2 = gomoku_file.player_2
        game_record = gomoku_file.game_record
        color_swap = gomoku_file.color_swap
        score = gomoku_file.score
        game_date = gomoku_file.game_date
        if request.user.is_authenticated():
            user_name = request.user.username

        ctx = {
            'game_record': game_record,
            'score': score,
            'player_1': player_1,
            'player_2': player_2,
            'color_swap': color_swap,
            'game_date': game_date,
            'user_name': user_name,
        }
        return render(request, 'game_record.html', ctx)


class GamesListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated():
            user = GomokuUser.objects.get(user=request.user.pk)
            user_name = request.user.username
        games = GomokuFiles.objects.all().exclude(gomoku_user=user)
        private_games = GomokuFiles.objects.filter(gomoku_user=user)
        ctx = {
            'games': games,
            'private_games': private_games,
            'user': user,
            'user_name': user_name,
        }
        return render(request, 'game-list.html', ctx)


class GameDelete(LoginRequiredMixin, DeleteView):
    model = GomokuFiles
    success_url = '/game-list/'
    template_name_suffix = '_confirm_delete'


class AboutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        ctx = {
            'user_name': user_name,
        }
        return render(request, 'about.html', ctx)


class HelpView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        ctx = {
            'user_name': user_name,
        }
        return render(request, 'help.html', ctx)





