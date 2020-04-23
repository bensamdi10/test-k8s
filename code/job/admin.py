from django.contrib import admin
from job.models import Job
# Register your models here.

class JobAdmin(admin.ModelAdmin):
   list_display = ('id', "name", "type", "uid")
admin.site.register(Job, JobAdmin)
