from django.db import models
from deployment.models import Deployment
from project_infra.choices import TYPE_CONTAINER, VOLUME_TYPE
from django.contrib.postgres.fields import JSONField
from store.models import Variable, PersistentVolume
from django.utils.text import slugify

# Create your models here.
class Container(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    deployment = models.ManyToManyField(Deployment, blank=True, default="")
    variable = models.ManyToManyField(Variable, blank=True, default="")
    persistent_volume = models.ManyToManyField(PersistentVolume, blank=True, default="")
    uid = models.CharField(max_length=200, blank=True, default="")
    type = models.CharField(max_length=200, choices=TYPE_CONTAINER)
    base_image = models.CharField(max_length=250, default="", blank=True)
    image_name = models.CharField(max_length=250, default="", blank=True)
    source = models.CharField(max_length=250, default="", blank=True)

    port = models.CharField(max_length=250, default="", blank=True)
    volume_path = models.CharField(max_length=250, default="", blank=True)
    commands = JSONField(blank = True, default=dict)
    cmd = models.CharField(max_length=250, default="", blank=True)

    color = models.CharField(max_length=250, default="", blank=True)
    color_fade = models.CharField(max_length=250, default="", blank=True)


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

        super(Container, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name