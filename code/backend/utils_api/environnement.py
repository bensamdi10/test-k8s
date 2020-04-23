
from environnement.models import Environnement
from project.models import Project
from ingress.models import Ingress
from django.utils.text import slugify
import uuid
from backend.api.serializers import EnvironnementSerializer, VariableSerializer

class EnvironnementAPI:


    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def mergeQuery(self, q1, q2):
        q3 = q1.union(q2)
        q3 = q3.distinct()
        return q3

    def getVariables(self, uid):
        env = self.getEnv(uid)
        if not env == None:
            variables = env.variable.all().filter(archive=False)
            deployments = env.deployment_set.all().filter(archive=False)
            for deploy in deployments:
                containers_deploy = deploy.container_set.all().filter(archive=False)
                for container in containers_deploy:
                    vars_container = container.variable.all().filter(archive=False)
                    variables = self.mergeQuery(variables, vars_container)
            return variables
        else:
            return None

    def serializeVariables(self, variables):
        variables = variables.order_by("id")
        serializer = VariableSerializer(variables, many=True).data
        return serializer

    def getContainers(self, uid):
        env = self.getEnv(uid)
        if not env == None:
            containers = None
            deployments = env.deployment_set.all().filter(archive=False)
            for deploy in deployments:
                containers_deploy = deploy.container_set.all().filter(archive=False)
                if containers == None:
                    containers = containers_deploy
                else:
                    containers = self.mergeQuery(containers, containers_deploy)
            return containers

        else:
            return []

    def getVolumes(self, uid):
        env = self.getEnv(uid)
        if not env == None:
            volumes = env.persistent_volume.all().filter(archive=False)
            return volumes

        else:
            return []


    def getClusters(self, uid):
        env = self.getEnv(uid)
        if not env == None:
            clusters = env.clusterip_set.all().filter(archive=False)
            return clusters

        else:
            return []


    def getEnv(self, uid):
        env = Environnement.objects.all().filter(uid=uid)
        if env.count() == 1:
            return env[0]
        else:
            return None
    def serialize(self, element_object):
        serializer = EnvironnementSerializer(element_object, many=True).data
        return serializer


    def get(self, uid):
        element = Environnement.objects.all().filter(uid=uid)
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

    def getProject(self, uid):
        project = Project.objects.all().filter(uid=uid)

        if project.count() == 1:
            return project[0]
        else:
            return None

    def createIngress(self, environnement):
        ingress = Ingress()
        slug_name_env = slugify(environnement.name, allow_unicode=True)
        ingress.name = "ingress-service-"+slug_name_env
        uid = self.generateUID()
        ingress.uid = uid
        ingress.environnement = environnement
        ingress.save()


    def save(self, data, element_object=None):
        if element_object == None:
            environnement = Environnement()
            uid = self.generateUID()
            environnement.uid = uid
        else:
            environnement = element_object


        uid_project = self.parseData(data, "project")
        project = self.getProject(uid_project)

        if not project == None:
            environnement.name = self.parseData(data, "name")
            environnement.type = self.parseData(data, "type")
            environnement.project = project

            environnement.save()

            self.createIngress(environnement)

            return { "status" : "success", "message" : "Saved", "uid" : environnement.uid, "element" :  "environnement" }
        else:
            return {"status": "error", "message": "Project Not exist", "uid" : environnement.uid, "element" :  "environnement"}

    def update(self, request, data, element):
        return self.save(request, data, element)


    def getDeployments(self, uid):
        return self.getChildrends("deployment", uid)

    def getIngress(self, uid):
        return self.getChildrends("ingress", uid)

    def getJobs(self, uid):
        return self.getChildrends("job", uid)
    def getServices(self, uid):
        return self.getChildrends("service", uid)

    def getVolumes(self, uid):
        return self.getChildrends("volume", uid)

    def getChildrends(self, type, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            if type == "deployment":
                return element.deployment_set.all().filter(archive=False)
            if type == "ingress":
                return element.ingress_set.all().filter(archive=False)
            if type == "service":
                return element.service_set.all().filter(archive=False)
            if type == "job":
                return element.job_set.all().filter(archive=False)
            if type == "volume":
                return element.persistent_volume.all().filter(archive=False)
        else:
            return []




