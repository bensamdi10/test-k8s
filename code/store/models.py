from django.db import models
from django.contrib.postgres.fields import JSONField
from project_infra.choices import TYPE_TEMPLATE, VOLUME_MODE, ACCESS_MODE_VOLUME
from django.utils.text import slugify
# Create your models here.


class Variable(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    value = models.CharField(max_length=250, default="")
    uid = models.CharField(max_length=200, blank=True, default="")
    archive = models.BooleanField(blank=False, default=False)
    secret = models.BooleanField(blank=False, default=False)
    date = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.name == "" and not self.name == " " and not self.name == "-":
            slug_original = slugify(self.name, allow_unicode=True)
            split_slug_original = slug_original.split("_")
            for i in split_slug_original:
                slug_original = slug_original.replace("_", "-")
            self.slug = slug_original

        super(Variable, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    description = models.TextField(blank=True, default="")
    uid = models.CharField(max_length=200, blank=True, default="")
    type = models.CharField(max_length=200, choices=TYPE_TEMPLATE)
    data = JSONField(blank=True, default=dict)
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

        super(Template, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name




class PersistentVolume(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    description = models.TextField(blank=True, default="")
    uid = models.CharField(max_length=200, blank=True, default="")
    access_mode = models.CharField(max_length=200, choices=ACCESS_MODE_VOLUME)
    storage = models.CharField(max_length=250, default="")
    volume_mode = models.CharField(max_length=200, choices=VOLUME_MODE)
    storage_class = models.CharField(max_length=200, blank=True, default="")
    mount_path = models.CharField(max_length=200, blank=True, default="")
    sub_path = models.CharField(max_length=200, blank=True, default="")
    selector = models.CharField(max_length=200, blank=True, default="")
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

        super(PersistentVolume, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name


class Path(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    path = models.CharField(max_length=250, default="")
    port = models.CharField(max_length=250, default="")
    description = models.TextField(blank=True, default="")
    uid = models.CharField(max_length=200, blank=True, default="")
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


        super(Path, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name

class Secret(models.Model):
    name = models.CharField(max_length=250, default="")
    slug = models.CharField(max_length=250, default="", blank=True)
    label = models.CharField(max_length=250, default="")
    value = models.CharField(max_length=250, default="")
    uid = models.CharField(max_length=200, blank=True, default="")
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

        super(Secret, self).save(*args, **kwargs)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.name