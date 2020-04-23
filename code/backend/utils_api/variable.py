
from service.models import Service
from environnement.models import Environnement
from store.models import  Variable
import uuid

from backend.api.serializers import VariableSerializer


class VariableAPI:

    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def serialize(self, element_object):
        serializer = VariableSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = Variable.objects.all().filter(uid=uid)
        if element.count() == 1:
            return element
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
            if object["secret_var"] == "" or object["secret_var"] == " ":
                temp_variable.secret = False
            else:
                variable.secret = object["secret_var"]
            variable.uid = self.generateUID()
            variable.save()
            return variable
        else:
            return temp_variable[0]

    def correctData(self, data):
        for d in data:
            if data[d] == "true":
                data[d] = True
            if data[d] == "false" or data[d] == None:
                data[d] =  False
        return data

    def save(self, data, element_object=None):
        if element_object == None:
            variable = Variable()
            uid = self.generateUID()
            variable.uid = uid
        else:
            variable = element_object





        uid_env = self.parseData(data, "environnement")
        environnement = self.getEnv(uid_env)
        if not environnement == None:
            list_variables_items = self.parseData(data, "variables_items")
            for var_item in list_variables_items:
                var_item = self.correctData(var_item)
                temp_variable = self.getVariable(var_item["uid_var"])
                if temp_variable == None:
                    var_item_object = self.saveVariable(var_item)
                    if not var_item_object == None:
                        environnement.variable.add(var_item_object)

                else:
                    temp_variable.name = var_item["name_var"]
                    temp_variable.value = var_item["value_var"]
                    if var_item["secret_var"] == "" or var_item["secret_var"] == " " :
                        temp_variable.secret = False
                    else:
                        temp_variable.secret = var_item["secret_var"]
                    temp_variable.save()



            return { "status" : "success", "message" : "Saved", "element" :  "variable" }
        else:
            return {"status": "error", "message": "Environnement Not exist", "element" :  "variable"}

    def update(self, request, data, element):
        return self.save(request, data, element)



