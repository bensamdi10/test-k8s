# -*- coding: utf-8 -*-

from django import forms
from .models import Profil
from .models import GENDER
from project_infra.choices import TYPE_PROFIL
from django.utils.translation import ugettext as _



class ProfilForm(forms.Form):
    #from_invitation = forms.CharField(label=_(u'from_invitation'), required=False)
    #token_invitation = forms.CharField(label=_(u'token_invitation'), required=False)
    first_name = forms.CharField(max_length=100, label=_('Nom'), required=True)
    last_name = forms.CharField(max_length=100, label=_('Prénom'), required=True)
    email = forms.EmailField(max_length=100, label=_('E-mail'), required=True)
    gender = forms.ChoiceField(label=_('gender'), required=True, choices=GENDER)
    type = forms.ChoiceField(label=_('type'), required=True, choices=TYPE_PROFIL)
    #phone = forms.CharField(max_length=20, required=True, validators=[PhoneValidator(message="Phone number is invalid")], label=_(u'Phone'))
    password = forms.CharField(label=_('Password'), required=True, widget=forms.PasswordInput(render_value=False))
    confirm_password = forms.CharField(label=_('Confirm password'), required=True,widget=forms.PasswordInput(render_value=False))
    photo_base64 = forms.CharField(widget=forms.Textarea, label=_('photo'), required=False)


class AuthorForm(forms.Form):
    first_name = forms.CharField(max_length=250, label=_('Nom'), required=True)
    last_name = forms.CharField(max_length=250, label=_('Prénom'), required=True)
    email = forms.EmailField(max_length=250, label=_('E-mail'), required=True)
    photo_base64 = forms.CharField(widget=forms.Textarea, label=_('photo'), required=False)
    about = forms.CharField(widget=forms.Textarea, label=_('about'), required=False)

    website = forms.CharField(max_length=250, label=_('website'), required=False)
    facebook = forms.CharField(max_length=250, label=_('facebook'), required=False)
    twitter = forms.CharField(max_length=250, label=_('twitter'), required=False)
    instagram = forms.CharField(max_length=250, label=_('instagram'), required=False)
    linkedin = forms.CharField(max_length=250, label=_('linkedin'), required=False)
    youtube = forms.CharField(max_length=250, label=_('youtube'), required=False)


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, label=_('E-mail'), required=True)
    password = forms.CharField(label=_('Password'), required=True, widget=forms.PasswordInput(render_value=False))

class PasswordForm(forms.Form):
    password = forms.CharField(label=_('Password'), required=True, widget=forms.PasswordInput(render_value=False))
    confirm_password = forms.CharField(label=_('Confirm password'), required=True, widget=forms.PasswordInput(render_value=False))


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, label=_('E-mail'), required=True)



class EditProfilForm(forms.Form):
    first_name = forms.CharField(max_length=100, label=_('Nom'), required=True)
    last_name = forms.CharField(max_length=100, label=_('Prénom'), required=True)
    email = forms.EmailField(max_length=100, label=_('E-mail'), required=True)
    phone = forms.CharField(max_length=20, required=True, label=_('Phone'))

class AboutProfilForm(forms.Form):
    gender = forms.ChoiceField(label=_('gender'), required=False, choices=GENDER)
    about = forms.CharField(widget=forms.Textarea, label=_('About'), required=False)
    photo_base64 = forms.CharField(widget=forms.Textarea, label=_('photo'), required=False)

class SecuityProfilForm(forms.Form):
    current_password = forms.CharField(label=_('current Password'), required=True, widget=forms.PasswordInput(render_value=False))
    new_password = forms.CharField(label=_('new Password'), required=True, widget=forms.PasswordInput(render_value=False))
    confirm_new_password = forms.CharField(label=_('Confirm new password'), required=True, widget=forms.PasswordInput(render_value=False))
