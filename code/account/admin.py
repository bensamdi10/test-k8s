# -*- coding: utf-8 -*-


from django.contrib import admin
from account.models import Profil
# Register your models here.


class ProfilAdmin(admin.ModelAdmin):
   list_display = ('id', 'email', "first_name", "last_name", "type")


admin.site.register(Profil, ProfilAdmin)