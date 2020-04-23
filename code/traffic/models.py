from django.db import models

# Create your models here.
class Traffic(models.Model):
    TYPE = (
        ('pixel', 'Lead'),
        ('click', 'click'),
        ('js', 'js'),
    )
    TYPE_ELEMENT = (
        ('view', 'view'),
        ('author', 'author'),
    )
    TYPE_CONVERSION = (
        ('form_lead', 'form_lead'),
        ('page_view', 'page_view'),
        ('click_btn', 'click_btn'),
        ('download_document', 'download_document'),
        ('play_video', 'play_video'),
        ('pourcent_video', 'play_video'),
        ('read_content', 'pourcent_video'),
        ('open_popup', 'open_popup'),
        ('other', 'other'),
        ('like', 'like'),
        ('bookmark', 'bookmark'),
        ('dislike', 'dislike'),
    )

    name = models.CharField(max_length=254, blank=True)
    type = models.CharField(max_length=200, choices=TYPE, blank=True, default="visite")
    date_created = models.DateField(auto_now_add=True)
    uid = models.CharField(max_length=254, blank=True, default="")
    ip = models.CharField(max_length=254, blank=True, default="")
    element = models.CharField(max_length=200, choices=TYPE_ELEMENT, blank=True, default="")
    id_element = models.CharField(max_length=254, blank=True)
    day = models.CharField(max_length=200, blank=True)
    day_time = models.CharField(max_length=200, blank=True)
    type_conversion = models.CharField(max_length=200, choices=TYPE_CONVERSION, blank=True, default="")


    def __id__(self):
        return self.id

    def __str__(self):
        return self.name