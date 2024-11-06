from django.db import models
from common.models import Timestamped
from users.models import User
from cars.models import Car



class Comment(Timestamped):
    """Комментарии к автомобилю"""
    content = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'<Comment к {self.car.model}>'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"