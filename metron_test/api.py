from rest_framework import routers
from app import views

router = routers.DefaultRouter()
router.register(r'hat', views.HatViewSet)
router.register(r'character', views.CharacterViewSet)