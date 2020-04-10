from django.db import models
from django.dispatch import receiver

from .models import Character


# Called after Character deletion. Delete associated hat
@receiver(models.signals.post_delete, sender=Character)
def delete_related_hat(sender, **kwargs):
    deleted_character = kwargs['instance']
    if deleted_character.hat:
        deleted_character.hat.delete()
