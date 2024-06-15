from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .managers import CachedManager

def cache_model(cls):
    # Attach the custom manager
    cls.add_to_class('objects', CachedManager())

    # Invalidate cache on save
    @receiver(post_save, sender=cls)
    def invalidate_cache_on_save(sender, instance, **kwargs):
        instance.invalidate_cache()

    # Invalidate cache on delete
    @receiver(post_delete, sender=cls)
    def invalidate_cache_on_delete(sender, instance, **kwargs):
        instance.invalidate_cache()

    # Add the invalidate_cache method to the model
    def invalidate_cache(self):
        self._default_manager.invalidate_cache(self)

    cls.invalidate_cache = invalidate_cache
    return cls

