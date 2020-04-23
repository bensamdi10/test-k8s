from django.contrib import admin

from environnement.models import Environnement
# Register your models here.


class EnvironnementAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "type", "uid")
admin.site.register(Environnement, EnvironnementAdmin)
