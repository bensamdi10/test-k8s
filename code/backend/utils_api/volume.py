
from service.models import Service
from environnement.models import Environnement
from deployment.models import Deployment
from store.models import  PersistentVolume
import uuid
from backend.api.serializers import PersistentVolumeSerializer

class VolumeAPI:

    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def serialize(self, element_object):
        serializer = PersistentVolumeSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = PersistentVolume.objects.all().filter(uid=uid)
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
    def getDeployment(self, uid):
        deployment = Deployment.objects.all().filter(uid=uid)

        if deployment.count() == 1:
            return deployment[0]
        else:
            return None

    def save(self, data, element_object=None):
        if element_object == None:
            volume = PersistentVolume()
            uid = self.generateUID()
            volume.uid = uid
        else:
            volume = element_object


        uid_env = self.parseData(data, "environnement")
        environnement = self.getEnv(uid_env)

        uid_deployment = self.parseData(data, "parent")
        deployment = self.getDeployment(uid_deployment)

        if not environnement == None and not deployment == None:
            volume.name = self.parseData(data, "name")
            volume.access_mode = self.parseData(data, "access_mode")
            volume.storage = self.parseData(data, "storage")
            volume.volume_mode = self.parseData(data, "volume_mode")
            volume.mount_path = self.parseData(data, "mount_path")
            volume.sub_path = self.parseData(data, "sub_path")
            #volume.selector = self.parseData(data, "selector")

            volume.save()

            environnement.persistent_volume.add(volume)
            deployment.persistent_volume.add(volume)

            return { "status" : "success", "message" : "Saved", "element" :  "volume", "uid" : volume.uid }
        else:
            return {"status": "error", "message": "Volume Not exist", "uid" : volume.uid, "element" :  "volume"}

    def update(self, request, data, element):
        return self.save(request, data, element)

    def generateYaml(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            object_element = {
                "apiVersion": "v1",
                "kind": "PersistentVolumeClaim",
                "metadata": {"name": element.slug},
                "spec": {
                    "accessModes" : [element.access_mode],
                    "resources": {
                        "requests": {
                            "storage": element.storage,
                        }
                    }
                },
            }
            return object_element
        else:
            return None