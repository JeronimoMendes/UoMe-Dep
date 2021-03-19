from django.contrib import admin
from .models import CommonAccount, Log

# Register your models here.
admin.site.register(CommonAccount)
admin.site.register(Log)