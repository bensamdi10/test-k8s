from django.db import models

from store.models import PersistentVolume
from environnement.models import Environnement
from django.utils.text import slugify

# Create your models here.
class Deployment(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    uid = models.CharField(max_length=200, blank=True, default="")
    replicas = models.CharField(max_length=200, blank=True, default="1")
    environnement = models.ManyToManyField(Environnement, blank=True, default="")
    archive = models.BooleanField(blank=False, default=False)
    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)
    persistent_volume = models.ManyToManyField(PersistentVolume, blank=True, default="")

    color = models.CharField(max_length=250, default="", blank=True)
    color_fade = models.CharField(max_length=250, default="", blank=True)


    def save(self, *args, **kwargs):
        if not self.name == "" and not self.name == " " and not self.name == "-":
            slug_original = slugify(self.name, allow_unicode=True)
            split_slug_original = slug_original.split("_")
            for i in split_slug_original:
                slug_original = slug_original.replace("_", "-")
            self.slug = slug_original

        super(Deployment, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name


class ClusterIP(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    uid = models.CharField(max_length=200, blank=True, default="")
    deployment = models.ManyToManyField(Deployment, blank=True, default="")
    environnement = models.ManyToManyField(Environnement, blank=True, default="")
    archive = models.BooleanField(blank=False, default=False)
    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)

    port = models.CharField(max_length=200, blank=True, default="")

    color = models.CharField(max_length=250, default="", blank=True)
    color_fade = models.CharField(max_length=250, default="", blank=True)

    def save(self, *args, **kwargs):
        if not self.name == "" and not self.name == " " and not self.name == "-":
            slug_original = slugify(self.name, allow_unicode=True)
            split_slug_original = slug_original.split("_")
            for i in split_slug_original:
                slug_original = slug_original.replace("_", "-")
            self.slug = slug_original

        super(ClusterIP, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name