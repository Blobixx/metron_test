from django.db import models
from django.core.validators import MinValueValidator


# Hat model
class Hat(models.Model):
    class Color(models.TextChoices):
        PURPLE = 'P'
        YELLOW = 'Y'
        GREEN = 'G'

    color = models.CharField(max_length=1, choices=Color.choices)


# Character model
class Character(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField('age', validators=[MinValueValidator(0)])
    weight = models.FloatField('weight', validators=[MinValueValidator(0)])
    human = models.BooleanField()
    # One to One relationship
    # Since hat is not set if not human, allow blank=True, and null in db
    hat = models.OneToOneField('Hat', on_delete=models.CASCADE, null=True, blank=True)


