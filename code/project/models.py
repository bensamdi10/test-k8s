from django.db import models
from project_infra.choices import PROVIDER
from django.utils.text import slugify

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    description = models.TextField(blank=True, default="")
    uid = models.CharField(max_length=200)
    name_space = models.CharField(max_length=200)
    provider = models.CharField(max_length=200, choices=PROVIDER)
    archive = models.BooleanField(blank=False, default=False)
    current = models.BooleanField(blank=False, default=False)

    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if not self.name == "" and not self.name == " " and not self.name == "-":
            slug_original = slugify(self.name, allow_unicode=True)
            split_slug_original = slug_original.split("_")
            for i in split_slug_original:
                slug_original = slug_original.replace("_", "-")
            self.slug = slug_original

        super(Project, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name