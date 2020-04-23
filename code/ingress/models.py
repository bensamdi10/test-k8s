from django.db import models
from project_infra.choices import INGRESS_ANNOTATIONS
from store.models import Path
from container.models import Container
from environnement.models import Environnement
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify

# Create your models here.
class Ingress(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    uid = models.CharField(max_length=200, blank=True, default="")
    annotations = JSONField(blank=True, default=dict)
    environnement = models.ForeignKey(Environnement, blank=True, default=1, on_delete=models.CASCADE)
    container = models.ManyToManyField(Container, blank=True, default="")
    domain = models.CharField(max_length=250, default="localhost")
    accept_tls = models.BooleanField(blank=False, default=False)
    accept_ssl = models.BooleanField(blank=False, default=False)
    ip_address = models.CharField(max_length=250, default="", blank=True)

    path = JSONField(blank=True, default=dict)
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

        super(Ingress, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name