# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny

from project_infra.middleware import TokenCheck

class TemplateCLIAPIView(APIView):
    accepted_renderer = True
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    security = True
    login = True

    def checkToken(self, token):
        token_check = TokenCheck()
        return token_check.check(token)

    def dispatch(self, request, *args, **kwargs):

        return super(TemplateCLIAPIView, self).dispatch(request, *args, **kwargs)









