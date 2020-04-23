from django.db import models
from project_infra.choices import TYPE_JOURNAL
# Create your models here.


# Create your models here.
class Journal(models.Model):
    name = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=100, choices=TYPE_JOURNAL)
    value = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(blank=False, default=False)
    company = models.CharField(max_length=200, blank=True)
    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)
    date_current = models.CharField(max_length=100, blank=True, default="")

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name