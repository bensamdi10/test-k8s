
from environnement.models import Environnement
from ingress.models import Ingress
from container.models import Container
import uuid
from store.models import Template
from backend.api.serializers import IngressSerializer

class IngressAPI:

    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def saveTemplate(self, uid, data):
        ingress = self.get(uid)
        if ingress == None:
            return { "status" : "error", "message" : "Element Not Found" }
        else:
            ingress = ingress[0]
            template = Template()
            template.name = self.parseData(data, "name")
            template.description = self.parseData(data, "description")
            template.type = "ingress"
            uid = self.generateUID()
            template.uid = uid
            template.data = { "annotations" : ingress.annotations, "path" : ingress.path}
            template.save()
            return {"status": "success", "message": "Template Created"}

    def serialize(self, element_object):
        serializer = IngressSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = Ingress.objects.all().filter(uid=uid)
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


    def getContainer(self, uid):
        container = Container.objects.all().filter(uid=uid)
        if container.count() == 1:
            return container[0]
        else:
            return None

    def save(self, data, element_object=None):
        if element_object == None:
            ingress = Ingress()
            uid = self.generateUID()
            ingress.uid = uid
        else:
            ingress = element_object


        uid_env = self.parseData(data, "environnement")
        environnement = self.getEnv(uid_env)

        if not environnement == None:
            #ingress.name = self.parseData(data, "name")
            ingress.annotations = self.parseData(data, "annotations")
            ingress.domain = self.parseData(data, "domain")
            ingress.accept_tls = self.parseData(data, "accept_tls")
            ingress.accept_ssl = self.parseData(data, "accept_ssl")
            ingress.path = self.parseData(data, "containers")

            ingress.save()

            list_container = self.parseData(data, "containers")
            for temp_container in list_container:
                print(temp_container)
                uid_container = temp_container["container_name"]
                container_item = self.getContainer(uid_container)
                if not container_item == None:
                    ingress.container.add(container_item)


            ingress.environnement = environnement

            return { "status" : "success", "message" : "Saved", "element" :  "ingress", "uid" : ingress.uid }
        else:
            return {"status": "error", "message": "Environnement Not exist", "element" :  "ingress"}
    def saveInline(self, data, element_object=None):
        if element_object == None:
            return {"status": "error", "message": "Element Not exist", "element": "ingress"}
        else:
            ingress = element_object
            if "accept_tls" in data:
                ingress.accept_tls = self.parseData(data, "accept_tls")
            if "accept_ssl" in data:
                ingress.accept_ssl = self.parseData(data, "accept_ssl")

            ingress.save()

            return { "status" : "success", "message" : "Saved", "element" :  "ingress", "uid" : ingress.uid }

    def update(self, request, data, element):
        return self.save(request, data, element)




    def generateYaml(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            annotations = {
                "kubernetes.io/ingress.class" : "nginx"
            }
            for annot in element.annotations:
                annotations[annot["annotation_name"]] = annot["annotation_value"]

            paths = []
            for path in element.path:
                object_path = {
                    "path": path["container_path"],
                    "backend": {
                        "serviceName": path["container_name"],
                        "servicePort": int(path["container_port"])
                    }
                }
                paths.append(object_path)
            object_element = {
                "apiVersion": "extensions/v1beta1",
                "kind": "Ingress",
                "metadata" : { "name" : element.slug, "annotations":annotations, },

                "spec" : {
                    "rules" : [
                        {
                            "http" : {
                                "paths" : paths
                            }
                        }
                    ]
                }

            }
            return object_element
        else:
            return None



