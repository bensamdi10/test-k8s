from django.db import models

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(blank=True, default=True)
    day = models.CharField(max_length=200, default="", blank=True)
    day_time = models.CharField(max_length=200, default="", blank=True)
    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)
    name_space = models.CharField(max_length=200, default="default", blank=True)
    ip = models.CharField(max_length=200, default="default", blank=True)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.token

    def __unicode__(self):
        return 'Proposal for: %s' % self.token