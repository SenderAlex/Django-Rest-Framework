from .models import Player
from .serializers import PlayerSerializer
from rest_framework import viewsets
from .permissions import AllForAdminOtherReadOnly
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


class PlayerAPIListPagination(PageNumberPagination):  # определенная пагинация
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = (AllForAdminOtherReadOnly, )  # IsAuthenticatedOrReadOnly -- права доступа только по чтению
    #filter_backends = [filters.SearchFilter]  # фильтрация данных по поиску
    filter_backends = [filters.OrderingFilter]  # фильтрация данных по сортировке в виде http://127.0.0.1:8000/api/player/?ordering=price_usd
    search_fields = ['football_player_name', 'nationality', 'age', 'count_of_club', 'matches', 'goals']  # поиск осуществляется в виде http://127.0.0.1:8000/api/player/?search=2020
    pagination_class = PlayerAPIListPagination  # определенная пагинация


##########################################################
class PlayerCreate(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
###########################################################