import logging
from django.db import models

class BarQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

class CustomManager(models.Manager):
    def get_queryset(self):
        queryset = BarQuerySet(self.model, using=self._db).active()
        logging.debug(queryset.query)  # Log the SQL query for debugging
        return queryset

def override_manager(new_manager):
    def decorator(model_class):
        if not issubclass(new_manager, models.Manager):
            raise TypeError("new_manager must be a subclass of models.Manager")
        
        model_class.add_to_class('objects', new_manager())
        return model_class

    return decorator

@override_manager(CustomManager)
class Bar(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Configure logging
logging.basicConfig(level=logging.DEBUG)

