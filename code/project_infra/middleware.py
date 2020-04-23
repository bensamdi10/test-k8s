# -*- coding: utf-8 -*-


from django_user_agents.utils import get_user_agent
from token_api.models import Token
import time
from django.conf import settings
from django.utils import translation
import uuid


class MobileDetection:
    def detect(self, request, template_name):
        user_agent = get_user_agent(request)

        if user_agent.is_mobile or user_agent.is_tablet:
            template_name = str(template_name)
            template_name = "mobile/"+template_name
        return template_name



class TokenCheck:

    def check(self, token):
        type = token[10]
        first_token = token[0:9]
        first_third_token = token[0:2]
        first_third_token2 = token[3:5]
        first_third_token3 = token[6:9]


        second_token = token[11:]
        second_third_token = token[11:13]
        second_third_token2 = token[14:16]
        second_third_token3 = token[17:]

        token_temp = Token.objects.all().filter(token=token)
        first_token_temp = Token.objects.all().filter(token__contains=first_token)
        first_third_token_temp = Token.objects.all().filter(token__contains=first_third_token).count()
        first_third_token_temp2 = Token.objects.all().filter(token__contains=first_third_token2).count()
        first_third_token_temp3 = Token.objects.all().filter(token__contains=first_third_token3).count()


        second_token_temp = Token.objects.all().filter(token__contains=second_token)
        second_third_token_temp = Token.objects.all().filter(token__contains=second_third_token).count()
        second_third_token_temp2 = Token.objects.all().filter(token__contains=second_third_token2).count()
        second_third_token_temp3 = Token.objects.all().filter(token__contains=second_third_token3).count()
        if token_temp.count() > 0:
            return False

        '''
        if first_third_token_temp > 0 and first_third_token_temp2 > 0 :
            return False

        if first_third_token_temp > 0 and first_third_token_temp3 > 0 :
            return False
        if first_third_token_temp2 > 0 and first_third_token_temp3 > 0 :
            return False
        '''
        if first_token_temp.count() > 0:
            return False

        '''
        if second_third_token_temp > 0 and second_third_token_temp3 > 0 :
            return False

        if second_third_token_temp > 0 and second_third_token_temp3 > 0 :
            return False
        if second_third_token_temp2 > 0 and second_third_token_temp3 > 0 :
            return False
        '''
        if second_token_temp.count() > 0:
            return False
        if not type == "s" and not type == "m" and not type == "l" and not type == "z":
            return False

        if token_temp.count() == 0 and first_token_temp.count() == 0 and second_token_temp.count() == 0:
            if type == "s" or type == "m" or type == "l" or type == "z":
                token_api = Token()
                token_api.token = token
                today = time.strftime("%Y-%m-%d")
                token_api.day = today
                token_api.save()
                return True

    def generateToken(self):
        return str(uuid.uuid4())

    def checkTokenCli(self, token, name_space, ip):
        token_temp = Token.objects.all().filter(token=token, name_space=name_space, ip=ip)
        if token_temp.count() == 0:
            token_api = Token()
            token_api.token = self.generateToken()
            today = time.strftime("%Y-%m-%d")
            token_api.day = today
            token_api.name_space = name_space
            token_api.ip = ip
            token_api.save()
            return token_api.token
        else:
            return token_temp.token





class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request, lang_active=None):
        if lang_active == None:
            request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        else:
            request.LANG = lang_active
        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG