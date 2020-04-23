
from service.models import Service
from environnement.models import Environnement
from store.models import Variable, Template
import uuid
from backend.api.serializers import ServiceSerializer

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import shutil

class ServiceAPI:

    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def saveTemplate(self, uid, data):
        service = self.get(uid)
        if service == None:
            return { "status" : "error", "message" : "Element Not Found" }
        else:
            service = service[0]
            template = Template()
            template.name = self.parseData(data, "name")
            template.description = self.parseData(data, "description")
            template.type = "service"
            uid = self.generateUID()
            template.uid = uid
            template.data = { "before_install" : service.before_install, "after_success" : service.after_success, "script" : service.script, "deploy" : service.deploy }
            template.save()
            return {"status": "success", "message": "Template Created"}

    def serialize(self, element_object):
        serializer = ServiceSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = Service.objects.all().filter(uid=uid)
        if element.count() == 1:
            return element
        else:
            return None

    def getVariables(self, uid):
        service = self.get(uid)
        if not service == None:
            variables = service[0].variable.all().filter(archive=False)
            return variables
        else:
            return None

    def generateUID(self):
        return str(uuid.uuid4())[:8]

    def parseData(self, data, label):
        if label in data:
            return data[label]
        else:
            return None

    def getEnv(self, uid):
        env = Environnement.objects.all().filter(uid=uid)

        if env.count() == 1:
            return env[0]
        else:
            return None

    def getVariable(self, uid):
        variable = Variable.objects.all().filter(uid=uid)
        if variable.count() == 1:
            return variable[0]
        else:
            return None

    def saveVariable(self, object):
        temp_variable = Variable.objects.all().filter(name=object["name_var"], value=object["value_var"])

        if temp_variable.count() == 0 :
            variable = Variable()
            variable.name = object["name_var"]
            variable.value = object["value_var"]
            variable.secret = object["secret_var"]
            variable.uid = self.generateUID()
            variable.save()
            return variable
        else:
            return temp_variable[0]

    def save(self, data, element_object=None):
        if element_object == None:
            service = Service()
            uid = self.generateUID()
            service.uid = uid
        else:
            service = element_object


        uid_env = self.parseData(data, "environnement")
        environnement = self.getEnv(uid_env)

        if not environnement == None:
            service.name = self.parseData(data, "name")
            #service.label = self.parseData(data, "label")
            service.type = self.parseData(data, "type")
            service.before_install = self.parseData(data, "before_install")
            service.script = self.parseData(data, "script")
            service.after_success = self.parseData(data, "after_success")
            service.deploy = self.parseData(data, "deploy")
            service.on_branch = self.parseData(data, "on_branch")
            service.save()


            list_variables = self.parseData(data, "variables")
            for variable_uid in list_variables:
                variable_item = self.getVariable(variable_uid)
                if not variable_item == None:
                    service.variable.add(variable_item)

            list_variables_items = self.parseData(data, "variables_items")
            for var_item in list_variables_items:
                var_item_object = self.saveVariable(var_item)
                if not var_item_object == None:
                    service.variable.add(var_item_object)


            service.environnement.add(environnement)

            return { "status" : "success", "message" : "Saved", "element" :  "service", "uid" : service.uid }
        else:
            return {"status": "error", "message": "Environnement Not exist", "element" :  "service"}

    def update(self, request, data, element):
        return self.save(request, data, element)



    def getListCommandYaml(self, list):
        result = []
        for command in list:
            result.append(command["command_sc"])

        return result


    def createScriptFile(self, list, type, environnement):
        base_dir = os.path.join(settings.BASE_DIR, 'yaml')
        base_dir = os.path.join(base_dir, environnement.project.slug)
        base_dir = os.path.join(base_dir, environnement.slug)
        shutil.rmtree(base_dir)
        path_file = os.path.join(base_dir, "deploy_"+type+".sh")
        text_script = ""
        for item in list:
            text_script += item+"\n";

        default_storage.save(path_file, ContentFile(text_script))

    def createScriptContent(self, list, type):
        text_script = ""
        for item in list:
            text_script += item+"\n";

        return { "type" : type, "content":  text_script}

    def generateYaml(self, uid, environnement):
        element = self.get(uid)
        if not element == None:
            element = element[0]

            cont_variables = element.variable.all().filter(archive=False)
            variables_list = []
            for env in cont_variables:
                variables_list.append(env.name+"="+env.value)

            script = self.createScriptContent(self.getListCommandYaml(element.deploy), element.type)
            object_element = {
                "sudo" : "required",
                "env" : {
                  "global" : variables_list
                },
                "services" : "docker",
                "before_install" : self.getListCommandYaml(element.before_install),
                "script" : self.getListCommandYaml(element.script),
                "after_success" : self.getListCommandYaml(element.after_success),
                "deploy" : {
                    'provider' : "script",
                    "script" :"bash ./deploy_"+element.type+".sh",
                    "on" : {
                        "branch" : element.on_branch
                    }
                },

            }
            return { "document" :  object_element, "script" : script}
        else:
            return None



