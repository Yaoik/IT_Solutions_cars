from django.db import models
from common.models import Timestamped
from users.models import User

class Make(Timestamped):
    """Марка автомобиля"""
    name = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return f'<Make {self.name}>'

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"


class Car(Timestamped):
    make = models.ForeignKey(Make, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=64)
    year = models.PositiveSmallIntegerField(null=True)
    description = models.CharField(max_length=512)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'<Car {self.model}>'

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
