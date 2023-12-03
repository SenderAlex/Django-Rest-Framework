from django.contrib import admin
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'football_player_name', 'nationality', 'age', 'count_of_club', 'matches', 'goals')  # для отображения полей в django administration
    list_filter = ('id', 'football_player_name', 'nationality', 'age', 'count_of_club', 'matches', 'goals')  # для фильтрации по полям
admin.site.register(Player, PlayerAdmin)

