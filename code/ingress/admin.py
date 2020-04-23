from django.contrib import admin
from ingress.models import Ingress
# Register your models here.
class ingressAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "domain", "uid", "accept_tls", "accept_ssl")
admin.site.register(Ingress, ingressAdmin)