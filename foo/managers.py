from django.db import models
from django.core.cache import cache
import hashlib

def generate_cache_key(model, **kwargs):
    key = f"{model.__name__}_"
    for k, v in sorted(kwargs.items()):
        key += f"{k}_{v}_"
    return hashlib.md5(key.encode('utf-8')).hexdigest()

class CachedQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        cache_key = generate_cache_key(self.model, **kwargs)
        obj = cache.get(cache_key)
        if obj:
            return obj
        obj = super().get(*args, **kwargs)
        cache.set(cache_key, obj)
        return obj

class CachedManager(models.Manager):
    def get_queryset(self):
        return CachedQuerySet(self.model, using=self._db)

    def invalidate_cache(self, instance):
        for field in instance._meta.fields:
            if field.name != 'id':
                cache_key = generate_cache_key(instance.__class__, **{field.name: getattr(instance, field.name)})
                cache.delete(cache_key)
        cache_key = generate_cache_key(instance.__class__, pk=instance.pk)
        cache.delete(cache_key)

