from django.contrib import admin
from newspaper.models import (
    Redactor,
    Topic,
    Newspaper,
)

admin.site.register(Redactor)
admin.site.register(Topic)
admin.site.register(Newspaper)