# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from project_infra.template_api_view_custom import TemplateAPIViewCustom
from project_infra.template_cli_api_view import TemplateCLIAPIView
from backend.api.serializers import *
from backend.factory import Factory
from project_infra.parse_request import ParseRequest
import uuid
from project_infra.middleware import TokenCheck

# SAVE 1 CREATE API
class SaveElement(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10
    login = False
    def post(self, request, element):
        data = request.data
        factory = Factory()

        result = factory.save(element, data, None)
        return Response(result, content_type="application/json", status=200)




# UPDATE API
class UpdateElement(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10
    login = False
    def post(self, request, element, uid):
        data = request.data
        factory = Factory()
        result = factory.update(element, data, uid)
        return Response(result, content_type="application/json", status=200)

class UpdateInlineElement(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10
    login = False
    def post(self, request, element, uid):
        data = request.data
        factory = Factory()
        result = factory.updateInline(element, data, uid)
        return Response(result, content_type="application/json", status=200)

# GET API
class GetElement(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    accepted_renderer = True
    limit_per_page = 10
    login = False


    def get(self, request, element, uid):

        result = { "status" : "success", "message" : "saved", "data" : {} }

        factory = Factory()
        element_json = factory.serialize(element, uid)
        result["data"] = element_json


        return Response(result, content_type="application/json", status=200)

class GetContainers(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    accepted_renderer = True
    limit_per_page = 10
    login = False


    def get(self, request, env):

        result = { "status" : "success", "message" : "saved", "data" : [] }

        factory = Factory()
        containers_json = factory.getContainers(env)
        result["data"] = containers_json


        return Response(result, content_type="application/json", status=200)

class GetVolumes(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    accepted_renderer = True
    limit_per_page = 10
    login = False


    def get(self, request, env):

        result = { "status" : "success", "message" : "saved", "data" : [] }

        factory = Factory()
        containers_json = factory.getVolumes(env)
        result["data"] = containers_json


        return Response(result, content_type="application/json", status=200)


class GetClusters(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    accepted_renderer = True
    limit_per_page = 10
    login = False


    def get(self, request, env):

        result = { "status" : "success", "message" : "saved", "data" : [] }

        factory = Factory()
        containers_json = factory.getClusters(env)
        result["data"] = containers_json


        return Response(result, content_type="application/json", status=200)

class GetEnvVariables(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    accepted_renderer = True
    limit_per_page = 10
    login = False


    def get(self, request, env):

        result = { "status" : "success", "message" : "saved", "data" : [] }

        factory = Factory()
        variables_json = factory.getEnvVariables(env)
        result["data"] = variables_json


        return Response(result, content_type="application/json", status=200)


class GetTemplates(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    accepted_renderer = True
    limit_per_page = 10
    login = False


    def get(self, request, element):
        result = {"status": "success", "message": "saved", "data": []}
        factory = Factory()
        templates = factory.getTemplates(element)
        result["data"] = templates


        return Response(result, content_type="application/json", status=200)

class GenerateYaml(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10
    login = False
    def get(self, request, env):
        data = request.data
        factory = Factory()
        yaml_documents = factory.generateYaml("environnement", env)

        return Response({ "status" : "success", "message" : "ok", "documents" : yaml_documents }, content_type="application/json", status=200)



# DELETE 1 ARCHIVE API

class DeleteElement(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request, element, uid):
        status_save = "success"
        message = "Element has Created successfully"
        step = 0

        factory  =Factory()
        factory.deleteElement(element, uid)



        return Response({ "status" : status_save, "message" : message, "step" : step }, content_type="application/json", status=200)

class ArchiveElement(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request, type, uid):
        status_save = "success"
        message = "Element has Created successfully"
        step = 0
        return Response({ "status" : status_save, "message" : message, "step" : step }, content_type="application/json", status=200)

class ArchiveItems(TemplateAPIViewCustom):

    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request, type):
        status_save = "success"
        message = "Element has Created successfully"
        step = 0
        return Response({ "status" : status_save, "message" : message, "step" : step }, content_type="application/json", status=200)

class RestaureItems(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def get(self, request, type):
        status_save = "success"
        message = "Element has Created successfully"
        step = 0


        return Response({ "status" : status_save, "message" : message, "step" : step }, content_type="application/json", status=200)


# API for RealTIme
class RunEnv(TemplateAPIViewCustom):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def generateUID(self):
        return str(uuid.uuid4())

    def get(self, request, env):
        status_save = "success"


        return Response({ "status" : status_save  }, content_type="application/json", status=200)


# API for CLI
class GetCLICredits(TemplateCLIAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def generateUID(self):
        return str(uuid.uuid4())

    def get(self, request, token, name_space):
        status_save = "success"
        parse_request = ParseRequest()
        #ip = parse_request.parse(request)["ip"]
        ip = "127.0.0.1"
        token_check = TokenCheck()
        token_temp = token_check.checkTokenCli(token, name_space, ip)

        return Response({ "status" : status_save, "token" : token_temp, 'name_space' : name_space  }, content_type="application/json", status=200)



class GenerateYamlCLI(TemplateCLIAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10
    login = False
    def get(self, request, env):
        factory = Factory()
        yaml_documents = factory.generateYaml("environnement", env)

        return Response(yaml_documents, content_type="application/json", status=200)

'''
class ConnectToSocket(TemplateCLIAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    limit_per_page = 10

    def generateUID(self):
        return str(uuid.uuid4())

    def get(self, request):
        status_save = "success"
        message = "Element has Created successfully"

        return Response({ "status" : status_save  }, content_type="application/json", status=200)
        
'''













