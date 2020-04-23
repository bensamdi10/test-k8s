
from project.models import Project
import uuid
from backend.api.serializers import ProjectSerializer

class ProjectAPI:


    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def serialize(self, element_object):
        serializer = ProjectSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = Project.objects.all().filter(uid=uid)
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
            project = Project()
            uid = self.generateUID()
            project.uid = uid
        else:
            project = element_object

        project.name = self.parseData(data, "name")
        project.description = self.parseData(data, "description")
        project.name_space = self.parseData(data, "name_space")
        project.provider = self.parseData(data, "provider")

        project.save()

        return { "status" : "success", "message" : "Project Created succefully", "element" :  "project", "uid" : project.uid }

    def update(self, request, data, element):
        return self.save(request, data, element)



