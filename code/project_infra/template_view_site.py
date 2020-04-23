# -*- coding: utf-8 -*-


from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import time
from account.models import Profil
import uuid


class TemplateViewSite(TemplateView):

    menus = {}
    widgets = {}
    blocks = {}
    language = "ar"
    apply_view = False
    custom_view = None
    name = "home"
    path_theme = None
    messages = []

    def getProfil(self, request):
        if request.user.is_anonymous == True:
            return None
        profil = Profil.objects.all().filter(user=request.user)
        if profil.count() == 1:
            profil = profil[0]
            return profil
        else:
            return None

    def generateUID(self):
        return str(uuid.uuid4())[:8]

    def defaultData(self, request):

        profil = self.getProfil(request)
        if not profil == None:
            if profil.type == "author" :
                return  {
                "first_article" : None,
                "sections": [],
                "articles" : [],
                "topics" : [],
                "suggest_topics" : [],
                "authors" : [],
                "bookmarks" : [],
                "popular" : [],
                "suggest_author" : None,
                "author_topics" : [],
                "quotes" : []
            }

            newsletter_profil = profil.newsletter_set.all().count()
            if newsletter_profil == 0:
                request.profil.subscribe = False
            else:
                request.profil.subscribe = True










        return {}




    def getProfilAuth(self, request):
        if request.user.is_authenticated == False:
            return None

        else:
            profil = Profil.objects.all().filter(user=request.user)
            if profil.count() == 1:
                profil = profil[0]
                return profil
            else:
                return None



    def dispatch(self, request, *args, **kwargs):

        split_path = request.path.split("/")
        path_page = request.path
        if request.path.find("/fr/") > -1:
            path_page = path_page.replace("/fr/", "/")

        if request.path.find("/en/") > -1:
            path_page = path_page.replace("/en/", "/")


        request.page_url = path_page

        profil = self.getProfilAuth(request)
        if not profil == None:
            if profil.block_access == True:
                return redirect("/block-account/")
        pseudo = ""
        count_messages = 0
        if not profil == None:
            pseudo = profil.first_name[0]+' '+profil.last_name[0]
            profil.pseudo = pseudo
            count_messages = len(self.messages)
            profil.messages = self.messages
            profil.count_messages = count_messages
            profil.newsletter_subscribe = profil.newsletter_subscribe
        request.profil = profil






        if self.path_theme == None:
            self.path_theme =  ""


        return super(TemplateViewSite, self).dispatch(request, *args, **kwargs)




    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {})





