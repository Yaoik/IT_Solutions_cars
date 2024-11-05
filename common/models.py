from django.db import models

class Timestamped(models.Model):
    """Абстрактная базовая модель для добавления времени создания/обновления"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

