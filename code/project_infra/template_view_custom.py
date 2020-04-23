# -*- coding: utf-8 -*-


from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from account.profil import ProfilUser
from account.models import Profil
import time
from django.conf import settings
import sys, zipfile, os, os.path, re
from traffic.models import Traffic
from project_infra.parse_request import ParseRequest
import uuid


URL_LOGIN = "/account/login-profil/"

class TemplateViewCustom(TemplateView):
    login = True
    url = ""
    create_view = False
    url_redirect_demo = ""
    demo_template = False
    simple_view = False
    type_profil = "administrator"
    create_client = False
    extra_metrics = []
    messages = []


    def connected(self, request, *args, **kwargs):
        user_check = ProfilUser()
        connected = user_check.checkUser(request)
        return connected

    def loginPage(self, path=""):
        if path == "" or path == None:
            return redirect(URL_LOGIN)
        else:
            return redirect(URL_LOGIN+"?next="+path)

    def getFiles(self, fullpath):

        return os.listdir(fullpath)

    def generateUID(self):
        return str(uuid.uuid4())[:8]


    def getProfil(self, request):
        if request.user.is_anonymous == True:
            return None
        profil = Profil.objects.all().filter(user=request.user)
        if profil.count() == 1:
            profil = profil[0]
            return profil
        else:
            return None

    def saveTraffic(self, request):
        passe = True
        traffic = Traffic()
        uid = self.generateUID()
        traffic.name = "View Author backend "+uid
        traffic.uid = uid
        traffic.element = "author"
        traffic.type = "pixel"
        parse_request = ParseRequest()
        ip_address = parse_request.parse(request)["ip"]
        traffic.ip = ip_address
        profil = self.getProfil(request)
        if profil == None:
            traffic.id_element = "-"
        else:
            traffic.id_element = str(profil.id)

        today = time.strftime("%Y-%m-%d")
        today_time = time.strftime("%Y-%m-%d %H:%M:%S")

        traffic.day = today
        traffic.day_time = today_time

        traffic.save()



        return passe




    def dispatch(self, request, *args, **kwargs):

        passe = self.saveTraffic(request)
        if passe == False :
            return redirect("/backend/block-account/")


        #fullpath = os.path.join(settings.MEDIA_ROOT, "page/template/")


        split_path = request.path.split("/")
        path_page = request.path
        if request.path.find("/fr/") > -1:
            path_page = path_page.replace("/fr/", "/")

        if request.path.find("/en/") > -1:
            path_page = path_page.replace("/en/", "/")

        request.page_url = path_page

        #self.template_name = MobileDetection().detect(request, self.template_name)
        user_check = ProfilUser()
        if self.login == True:
            connect_user = self.connected(request)
            if connect_user:
                profil_user = user_check.getProfil(request)

                if not profil_user == None:
                    if profil_user.block_access == True:
                        return redirect("/block-account/")

                if profil_user.type == "author" :
                    author  = profil_user.author_set.all()[0]
                    profil_user.photo_url = profil_user.photo.url

                request.profil = {
                     "role": profil_user.role,
                     "type": profil_user.type,
                     "status": profil_user.status,
                    "first_name": profil_user.first_name, "last_name": profil_user.last_name,
                    "pseudo": profil_user.first_name[0] + " " +profil_user.last_name[0],
                    "photo": profil_user.photo_url,
                    "id" : profil_user.id,
                    "tour_backend" : profil_user.tour_backend,
                    "tour_site" : profil_user.tour_site,
                    "messages" : self.messages,
                    "count_messages" : len(self.messages)
                }





                return super(TemplateViewCustom, self).dispatch(request, *args, **kwargs)
            else:
                if self.url == "" or self.url == None:
                    self.url = request.path

                return self.loginPage(request.build_absolute_uri())
        else:
            return super(TemplateViewCustom, self).dispatch(request, *args, **kwargs)





