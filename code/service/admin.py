from django.contrib import admin
from service.models import Service
# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "type", "on_branch", "uid")
admin.site.register(Service, ServiceAdmin)