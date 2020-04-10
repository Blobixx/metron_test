from rest_framework import viewsets

from django.db.models.signals import post_delete

from . import serializers
from .models import Character, Hat
from .signals import delete_related_hat


class HatViewSet(viewsets.ModelViewSet):
    queryset = Hat.objects.all()
    serializer_class = serializers.HatSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = serializers.CharacterSerializer


# Signal to delete hat when associated Character is deleted
post_delete.connect(delete_related_hat, sender=Character)
