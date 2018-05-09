from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GomokuUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=64, unique=True, default='')


class GomokuFiles(models.Model):
    player_1 = models.CharField(max_length=255, null=True)
    player_2 = models.CharField(max_length=255, null=True)
    files = models.FileField(null=True)
    game_data = models.TextField(null=True)
    color_swap = models.CharField(max_length=50, null=True)
    game_record = models.TextField(null=True)
    score = models.CharField(max_length= 50, null=True)
    game_date = models.CharField(max_length=50, null=True)
    gomoku_user = models.ManyToManyField(GomokuUser, null=True)

    def __str__(self):
        return 'player 1: {}  player 2: {} swap: {}, game record: {}'.format(
            self.player_1,
            self.player_2,
            self.color_swap,
            self.game_record,
        )





# class FilesData(models.Model):
#     name = models.CharField(max_length=255)
#     game_data = models.TextField()
#     gomoku_files = models.OneToOneField(GomokuFiles)
