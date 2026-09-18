from django.db import models
from apps.core.models import BaseModel

class GlobalSetting(BaseModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.key}: {self.value}"
