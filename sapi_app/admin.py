from django.contrib import admin
from . import models

admin.site.register(models.APIKey)
admin.site.register(models.JSONRecord)
