# -*- coding: utf-8 -*-


import time
from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from project_infra.middleware import TokenCheck
from account.models import Profil

class TemplateAPIViewCustom(APIView):
    accepted_renderer = True
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    security = True
    login = True

    def checkToken(self, token):
        token_check = TokenCheck()
        return token_check.check(token)

    def getProfil(self, request):
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
        if self.login == True:
            profil = self.getProfil(request)
            if not profil == None:
                if profil.block_access == True:
                    response = Response(
                        {"status": "error", "data": [], "count": 0, "message": _("Token is Required to make this Request")},
                        content_type="application/json", status=status.HTTP_401_UNAUTHORIZED)

                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}

                    return response

        if 'token_api' in request.GET :
            token_api = request.GET["token_api"]
            check_security_token = self.checkToken(token_api)

            if self.security == True and check_security_token == False:

                response = Response(
                    {"status": "error", "data": [], "count": 0, "message": _("Token of API is not Valid or Expired")},
                    content_type="application/json", status=200)

                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}

                return response
            else:
                return super(TemplateAPIViewCustom, self).dispatch(request, *args, **kwargs)
        else:

            response = Response(
                {"status": "error", "data": [], "count": 0, "message": _("Token is Required to make this Request")},
                content_type="application/json", status=status.HTTP_401_UNAUTHORIZED)

            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}

            return response









