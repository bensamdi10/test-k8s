from django.db import models
from project_infra.choices import TYPE_ENV
from project.models import Project
from store.models import Variable, PersistentVolume
from django.utils.text import slugify

# Create your models here.


# Create your models here.
class Environnement(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    project = models.ForeignKey(Project, blank=True, default=1, on_delete=models.CASCADE)
    uid = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=TYPE_ENV)
    variable = models.ManyToManyField(Variable, blank=True, default="")
    persistent_volume = models.ManyToManyField(PersistentVolume, blank=True, default="")
    archive = models.BooleanField(blank=False, default=False)
    current = models.BooleanField(blank=False, default=False)
    color = models.CharField(max_length=250, default="", blank=True)
    color_fade = models.CharField(max_length=250, default="", blank=True)

    settings = models.TextField(blank=True, default="")

    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if not self.name == "" and not self.name == " " and not self.name == "-":
            slug_original = slugify(self.name, allow_unicode=True)
            split_slug_original = slug_original.split("_")
            for i in split_slug_original:
                slug_original = slug_original.replace("_", "-")
            self.slug = slug_original

        super(Environnement, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name