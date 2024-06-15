from django.db import models
from .managers import CachedManager


class MyModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    #objects = CachedManager()

class RelatedModel(models.Model):
    my_model = models.ForeignKey(MyModel, on_delete=models.CASCADE, related_name='related_models')
    name = models.CharField(max_length=255)

    objects = CachedManager()

