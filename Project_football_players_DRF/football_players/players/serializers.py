from .models import Player
from rest_framework import serializers

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'football_player_name', 'nationality', 'age', 'count_of_club', 'matches', 'goals')
        # можно вместо всех этих полей '__all__'
        extra_kwargs = {'id': {'read_only': False}}

