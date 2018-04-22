
from django.db import models
from rest_framework.fields import JSONField


class Game(models.Model):
    game_record = JSONField

    def __str__(self):
        return '{}'.format(self.game_record)
