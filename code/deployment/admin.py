from django.contrib import admin

from deployment.models import Deployment, ClusterIP
# Register your models here.


class DeploymentAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "replicas", "uid")
admin.site.register(Deployment, DeploymentAdmin)



class ClusterIPAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "port", "uid")
admin.site.register(ClusterIP, ClusterIPAdmin)