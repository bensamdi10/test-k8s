
from container.models import Container
from deployment.models import Deployment
from store.models import PersistentVolume, Variable, Template
import uuid
from backend.api.serializers import ContainerSerializer


class ElementExisted:

    def getContainer(self, uid):
        element = Container.objects.all().filter(uid=uid)
        if element.count() == 1:
            return element[0]
        else:
            return None

    def getVolume(self, uid):
        element = PersistentVolume.objects.all().filter(uid=uid)
        if element.count() == 1:
            return element[0]
        else:
            return None

    def save(self, data, object=None):
        print()
        if "container" in data:
            container = self.getContainer(data["container"])
            if not container == None:
                deployment = Deployment.objects.all().filter(uid=data["parent"])
                if deployment.count() == 1:
                    deployment = deployment[0]
                    print(deployment)
                    container.deployment.add(deployment)
                return {"status": "success", "message": "Saved", "uid": container.uid, "element": "container"}


        if "volume" in data:
            volume = self.getVolume(data["volume"])
            print(volume)
            if not volume == None:
                deployment = Deployment.objects.all().filter(uid=data["parent"])
                print(deployment)
                if deployment.count() == 1:
                    deployment = deployment[0]
                    deployment.persistent_volume.add(volume)

            return { "status" : "success", "message" : "Saved", "uid" : volume.uid, "element" :  "volume" }

        return {"status": "error", "message": "Element not exist", "uid": "", "element": ""}