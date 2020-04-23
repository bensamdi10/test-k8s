
from service.models import Service
from environnement.models import Environnement
from store.models import  Template
import uuid
from backend.api.serializers import TemplateSerializer

class TemplateAPI:

    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def getTemplates(self, element):
        templates = Template.objects.all().filter(type=element, archive=False)
        print(templates)
        return templates

    def serialize(self, element_object):
        serializer = TemplateSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = Template.objects.all().filter(uid=uid)
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

    def save(self, data, element_object=None):
        if element_object == None:
            template = Template()
            uid = self.generateUID()
            template.uid = uid
        else:
            template = element_object

        template.name = self.parseData(data, "name")
        template.description = self.parseData(data, "description")
        template.type = self.parseData(data, "type")
        template.data = self.parseData(data, "data")


        template.save()

        return { "status" : "success", "message" : "Saved", "element" :  "template", "uid" : template.uid }


    def update(self, request, data, element):
        return self.save(request, data, element)



