from django.contrib import admin
from container.models import Container
# Register your models here.
class ContainerAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "type", "base_image", "image_name", "source", "port", "volume_path", "cmd")
admin.site.register(Container, ContainerAdmin)