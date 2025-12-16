from django.contrib import admin

# Register your models here.
from .models import Report, Filter, Pages  

admin.site.register(Report)
admin.site.register(Filter)
admin.site.register(Pages)