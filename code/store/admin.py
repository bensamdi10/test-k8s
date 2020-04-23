from django.contrib import admin
from store.models import Variable, PersistentVolume, Template
# Register your models here.


class VariableAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "value", "secret", "uid", "slug")
admin.site.register(Variable, VariableAdmin)



class PersistentVolumeAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "access_mode", "storage", "volume_mode", "storage_class", "mount_path", "sub_path")
admin.site.register(PersistentVolume, PersistentVolumeAdmin)



class TemplateAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "description", "type", "uid")
admin.site.register(Template, TemplateAdmin)