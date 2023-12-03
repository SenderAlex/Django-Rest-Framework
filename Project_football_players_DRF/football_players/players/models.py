from django.db import models

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    football_player_name = models.CharField(max_length=60)
    nationality = models.CharField(max_length=60)
    age = models.IntegerField()
    count_of_club = models.CharField(max_length=60)
    matches = models.IntegerField()
    goals = models.IntegerField()


    def clean(self):  # хитрожопский способ, чтобы id  был NOT NULL!!!
        if not self.id:
            self.id = Player.objects.last().id + 1