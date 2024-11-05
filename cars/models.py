from django.db import models
from common.models import Timestamped
from users.models import User

class Make(Timestamped):
    name = models.CharField(max_length=64, unique=True)

class Car(Timestamped):
    make = models.ForeignKey(Make, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=64)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=512)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    