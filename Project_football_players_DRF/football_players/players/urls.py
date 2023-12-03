from django.urls import path, include
from rest_framework import routers
from .views import PlayerViewSet, PlayerCreate, PlayerRetrieveUpdateDelete

router = routers.DefaultRouter()
router.register('players', PlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # осуществляет log out в API
    #path('player-create/', PlayerCreate.as_view(), name='player-create'),
    #path('player-create/<int:pk>/', PlayerRetrieveUpdateDelete.as_view(), name='player-details'),
]