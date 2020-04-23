from django.db import models
from project_infra.choices import CRON_TYPE, RESTART_POLICY
from container.models import Container
from environnement.models import Environnement
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify


# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    uid = models.CharField(max_length=200, blank=True, default="")
    environnement = models.ForeignKey(Environnement, blank=True, default=1, on_delete=models.CASCADE)
    command = models.CharField(max_length=200, blank=True, default="")
    container = models.ManyToManyField(Container, blank=True, default="")
    container_image = models.CharField(max_length=200, blank=True, default="")
    type = models.CharField(max_length=200, choices=CRON_TYPE)
    schedule = models.CharField(max_length=200, blank=True, default="")

    restart_policy = models.CharField(max_length=200, choices=RESTART_POLICY)
    back_off_limit = models.CharField(max_length=200, blank=True, default="5")

    config = JSONField(blank=True, default=dict)

    archive = models.BooleanField(blank=False, default=False)
    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if not self.name == "" and not self.name == " " and not self.name == "-":
            slug_original = slugify(self.name, allow_unicode=True)
            split_slug_original = slug_original.split("_")
            for i in split_slug_original:
                slug_original = slug_original.replace("_", "-")
            self.slug = slug_original

        super(Job, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name