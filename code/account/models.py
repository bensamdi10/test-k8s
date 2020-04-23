# -*- coding: utf-8 -*-


from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from project_infra.choices import GENDER, STATUS_PROFIL, ROLES, TYPE_PROFIL, STATUS_TYPE_PROFIL


THEMES = (
    ('default', 'default'),
    ('dango', 'dango'),
    ('mint', 'mint'),
    ('forest', 'forest'),
    ('navy', 'navy'),
    ('imperial', 'imperial'),
    ('suryp', 'suryp'),
    ('fushia', 'fushia'),
    ('ultra', 'ultra'),
    ('gold', 'gold'),
    ('retro', 'retro'),
    ('pop', 'pop'),
)

LAYOUT_HOME = (
    ('default', 'default'),
    ('edge', 'edge'),
    ('scientist', 'The Scientist'),
    ('flow', 'flow'),
    ('astra', 'astra'),
    ('storm', 'storm'),
    ('chameleon', 'chameleon'),
    ('mechanic', 'mechanic'),
    ('mage', 'mage'),
    ('katana', 'katana'),
    ('vorpal', 'vorpal'),
)

# Create your models here.
class Profil(models.Model):

    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254, blank=True)
    last_name = models.CharField(max_length=254, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=254, blank=True)
    gender = models.CharField(max_length=200, choices=GENDER, blank=True)
    token = models.CharField(max_length=254)
    active = models.BooleanField(blank=True, default=False)
    date_created = models.DateField(auto_now_add=True)
    from_invitation = models.BooleanField(default=False)
    token_invitation = models.CharField(max_length=254, blank=True)
    about = models.TextField(blank=True, default="")
    status = models.CharField(max_length=200, choices=STATUS_PROFIL, default="", blank=True)
    type = models.CharField(max_length=200, choices=TYPE_PROFIL, default="", blank=True)
    status_type = models.CharField(max_length=200, choices=STATUS_TYPE_PROFIL, default="", blank=True)
    photo = models.ImageField(upload_to="uploads/profil",null=True, blank=True)
    role = models.CharField(max_length=200, choices=ROLES, blank=True, default="admin")

    theme = models.CharField(max_length=200, choices=THEMES, default="default")
    layout_home = models.CharField(max_length=200, choices=LAYOUT_HOME, default="default")

    tour_backend = models.BooleanField(default=False)
    tour_site = models.BooleanField(default=False)
    tour_editor = models.BooleanField(default=False)
    newsletter_subscribe = models.BooleanField(default=False)
    block_access = models.BooleanField(default=False)

    def __id__(self):
        return self.id

    def __str__(self):
        return self.first_name

    def sendMail(self, params):
        ctx = params
        url_redirection = settings.DOMAIN+"/account/verify-profil/"+str(ctx["token"])+"/"
        ctx["url_redirection"] = url_redirection
        ctx["profil_name"] = ctx["first_name"]+ " "+ ctx["last_name"]
        message = get_template('emails/email_create_profil.html').render(ctx)
        sujet = '[ريكتو بوست]  تأكيد حساب المستخدم الخاص بك'
        
        msg = EmailMultiAlternatives(sujet, message, settings.EMAIL_HOST_USER, [self.user.email])
        msg.content_subtype = 'html'
        try:
            msg.send()
            return True
        except:
            return False


    def sendMailPassord(self, params):
        ctx = params
        url_redirection = settings.DOMAIN+"/account/password-profil/"+ctx["token"]+"/"
        ctx["url_redirection"] = url_redirection
        ctx["profil_name"] = ctx["first_name"]+ " "+ ctx["last_name"]
        message = get_template('emails/email_password.html').render(ctx)
        sujet = '[ريكتو بوست] هل نسيت كلمة المرور'
        msg = EmailMultiAlternatives(sujet, message, settings.EMAIL_HOST_USER, [self.user.email])
        msg.content_subtype = 'html'
        try:
            msg.send()
            return True
        except:
            return False

    def sendMailReset(self, params):
        ctx = params
        url_redirection = settings.DOMAIN+"/account/login-profil/"
        ctx["url_redirection"] = url_redirection
        ctx["profil_name"] = ctx["first_name"]+ " "+ ctx["last_name"]
        message = get_template('emails/email_reset_password.html').render(ctx)
        sujet = '[ريكتو بوست] إعادة تعيين كلمة المرور'
        msg = EmailMultiAlternatives(sujet, message, settings.EMAIL_HOST_USER, [self.user.email])
        msg.content_subtype = 'html'
        try:
            msg.send()
            return True
        except:
            return False

    def sendDailyMail(self, params):
        ctx = params
        message = get_template('emails/email_daily.html').render(ctx)
        sujet = '[ريكتو بوست]  النشرة البريدية اليومية الخاصة بك'

        msg = EmailMultiAlternatives(sujet, message, settings.EMAIL_HOST_USER, ["bensamdisaid@gmail.com"]) #[self.user.email]
        msg.content_subtype = 'html'
        try:
            msg.send()
            return True
        except:
            return False



    def sendEmailBlockAccess(self, params={}):
        ctx = params
        url_redirection = settings.DOMAIN + "/block-account/"
        ctx["url_redirection"] = url_redirection
        ctx["profil_name"] = ctx["first_name"] + " " + ctx["last_name"]
        message = get_template('emails/email_lock_profil.html').render(ctx)
        sujet = '[ريكتو بوست] حسابكم مقفل'
        msg = EmailMultiAlternatives(sujet, message, settings.EMAIL_HOST_USER, [self.user.email])
        msg.content_subtype = 'html'
        try:
            msg.send()
            return True
        except:
            return False







