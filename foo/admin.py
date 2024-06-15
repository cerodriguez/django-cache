from django.contrib import admin
from .models import MyModel, RelatedModel

admin.site.register(MyModel)
admin.site.register(RelatedModel)
