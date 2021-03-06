# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated

from cms.template_api_view_custom import TemplateAPIViewCustom

from account.models import Profil


class ActiveTheme(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request, theme):
        message = "success"

        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            profil.theme = theme
            profil.save()
        else:
            message = "error"
        return Response({ "status" : message }, content_type="application/json", status=200)


class ActiveLayout(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request, layout):
        message = "success"

        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            profil.layout_home = layout
            profil.save()
        else:
            message = "error"
        return Response({ "status" : message }, content_type="application/json", status=200)


class DisableTourBackend(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request):
        message = "success"

        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            profil.tour_backend = True
            profil.save()
        else:
            message = "error"

        return Response({ "status" : message }, content_type="application/json", status=200)



class DisableTourSite(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request):
        message = "success"

        user = request.user
        profils = Profil.objects.all()
        profil = profils.filter(user_id=user.id)
        if profil.count() > 0:
            profil = profil[0]
            profil.tour_site = True
            profil.save()
        else:
            message = "error"


        return Response({ "status" : message }, content_type="application/json", status=200)