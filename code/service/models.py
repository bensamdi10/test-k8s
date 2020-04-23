from django.db import models
from project_infra.choices import TYPE_SERVICE
from django.contrib.postgres.fields import JSONField
from environnement.models import Environnement
from store.models import Variable
from django.utils.text import slugify

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    label = models.CharField(max_length=250, default="", blank=True)
    environnement = models.ManyToManyField(Environnement, blank=True, default="")
    variable = models.ManyToManyField(Variable, blank=True, default="")
    description = models.TextField(blank=True, default="")
    uid = models.CharField(max_length=200, blank=True, default="")
    before_install = JSONField(blank = True, default=dict)
    script = JSONField(blank = True, default=dict)
    type = models.CharField(max_length=200, choices=TYPE_SERVICE)
    after_success = JSONField(blank=True, default=dict)
    deploy = JSONField(blank=True, default=dict)
    on_branch = models.CharField(max_length=250, default="")

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

        super(Service, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name
