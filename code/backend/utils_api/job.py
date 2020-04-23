
from job.models import Job
from environnement.models import Environnement
from container.models import Container
from store.models import PersistentVolume, Variable
import uuid
from backend.api.serializers import JobSerializer

class JobAPI:


    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def serialize(self, element_object):
        serializer = JobSerializer(element_object, many=True).data
        return serializer


    def get(self, uid):
        element = Job.objects.all().filter(uid=uid)
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

    def getContainer(self, uid):
        container = Container.objects.all().filter(uid=uid)
        if container.count() == 1:
            return container[0]
        else:
            return None

    def save(self, data, element_object=None):
        if element_object == None:
            job = Job()
            uid = self.generateUID()
            job.uid = uid
        else:
            job = element_object


        uid_env = self.parseData(data, "environnement")
        environnement = self.getEnv(uid_env)

        if not environnement == None:
            job.name = self.parseData(data, "name")
            job.command = self.parseData(data, "command")
            job.type = self.parseData(data, "type")
            job.schedule = self.parseData(data, "schedule")
            job.restart_policy = self.parseData(data, "restart_policy")
            job.back_off_limit = self.parseData(data, "back_off_limit")
            job.container_image = self.parseData(data, "container_image")
            job.environnement = environnement
            #job.config = self.parseData(data, "config")


            job.save()

            uid_container = self.parseData(data, "container")
            container_item = self.getContainer(uid_container)
            if not container_item == None:
                job.container.add(container_item)






            return { "status" : "success", "message" : "Saved", "element" :  "job", "uid" : job.uid }
        else:
            return {"status": "error", "message": "Environnement Not exist", "element" :  "job"}

    def update(self, request, data, element):
        return self.save(request, data, element)



    def generateYaml(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            kind = "Job"
            if element.type == "cron":
                kind = "CronJob"
            object_element = {}
            if element.type == "job" :
                object_element = {
                    "apiVersion": "batch/v1",
                    "kind": "Job",
                    "metadata" : { "name" : element.slug },
                    "spec" : {
                        "template": {
                            "spec": {
                                "containers": [],
                                "restartPolicy": element.restart_policy
                            }
                        },
                        "backoffLimit": int(element.back_off_limit)
                    },

                }
            if element.type == "cron":
                object_element = {
                    "apiVersion": "batch/v1beta1",
                    "kind": "CronJob",
                    "metadata": {"name": element.slug},
                    "spec": {
                        "schedule": element.schedule,
                        "jobTemplate": {
                            "spec": {
                                "template": {
                                    "spec": {
                                        "containers": [],
                                        "restartPolicy": element.restart_policy
                                    }
                                },
                            },

                        }
                    }


                }
            return object_element
        else:
            return None


