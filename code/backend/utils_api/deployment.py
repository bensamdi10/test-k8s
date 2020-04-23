
from environnement.models import Environnement
from deployment.models import Deployment, ClusterIP
import uuid
from django.utils.text import slugify
from backend.api.serializers import DeploymentSerializer, ClusterIPSerializer

class DeploymentAPI:

    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def serialize(self, element_object):
        serializer = DeploymentSerializer(element_object, many=True).data
        return serializer


    def serializeClusters(self, element_object):
        serializer = ClusterIPSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = Deployment.objects.all().filter(uid=uid)
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


    def createClusterIP(self, deployment, environnement):

        temp_cluster_ip = deployment.clusterip_set.all().filter(archive=False)
        if temp_cluster_ip.count() == 0:
            cluster_ip = ClusterIP()
            slug_name = slugify( deployment.name, allow_unicode=True)
            cluster_ip.name = slug_name+"-cluster-ip-service"
            uid = self.generateUID()
            cluster_ip.uid = uid
            cluster_ip.color = deployment.color
            cluster_ip.color_fade = deployment.color_fade
            containers = deployment.container_set.all()
            if containers.count() > 0 :
                cluster_ip.port = containers[0].port
            cluster_ip.save()
            cluster_ip.deployment.add(deployment)
            cluster_ip.environnement.add(environnement)
        else:
            temp_cluster_ip = temp_cluster_ip[0]
            slug_name = slugify(deployment.name, allow_unicode=True)
            temp_cluster_ip.name = slug_name + "-cluster-ip-service"
            temp_cluster_ip.save()

    def saveInline(self, data, element_object=None):
        if element_object == None:
            return {"status": "error", "message": "Element Not exist", "element": "ingress"}
        else:
            cluster_ip = element_object.clusterip_set.all()
            if cluster_ip.count() == 1 :
                cluster_ip = cluster_ip[0]
                if "port_cluster_ip" in data:
                    cluster_ip.port = self.parseData(data, "port_cluster_ip")

                    cluster_ip.save()

                return {"status": "success", "message": "Saved", "element": "CLuster IP", "uid": element_object.uid}
            else:
                return {"status": "error", "message": "Element Not exist", "element": "CLuster IP"}

    def save(self, data, element_object=None):
        if element_object == None:
            deployment = Deployment()
            uid = self.generateUID()
            deployment.uid = uid
        else:
            deployment = element_object



        uid_env = self.parseData(data, "environnement")
        environnement = self.getEnv(uid_env)
        if not environnement == None:
            deployment.name = self.parseData(data, "name")
            deployment.replicas = self.parseData(data, "replicas")
            deployment.save()
            deployment.environnement.add(environnement)

            self.createClusterIP(deployment, environnement)

            return { "status" : "success", "message" : "Saved", "uid" : deployment.uid, "element" :  "deployment" }
        else:
            return {"status": "error", "message": "Environnement Not exist", "element" :  "deployment"}

    def update(self, request, data, element):
        return self.save(request, data, element)

    def generateYaml(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            volumes = []
            volumes_list = element.persistent_volume.all().filter(archive=False)
            for vol in volumes_list:
                object_pvc = {
                    "name" : vol.slug,
                    "persistentVolumeClaim" :{
                        "claimName" : vol.slug
                        }
                    }
                volumes.append(object_pvc)
            object_element = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata" : {"name": element.slug},
                "spec" : {
                    "replicas" : int(element.replicas),
                    "selector" : {
                        "matchLabels" : {
                            "component" : element.slug
                        }
                    },
                    "template": {
                        "metadata" : {
                            "labels" : {
                                "component": element.slug
                            }
                        },
                        "spec": {
                            "volumes" : volumes,
                            "containers": []

                        }
                    }
                }

            }
            return object_element
        else:
            return None

    def generateClusterIpYaml(self, uid):
        deploy = self.get(uid)
        if not deploy == None:
            deploy = deploy[0]
            element = deploy.clusterip_set.all()[0]
            object_element = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata" : {"name": element.slug},
                "spec" : {
                    "type" : "ClusterIP",
                    "selector" : {
                        "component" : deploy.slug
                    },
                    "ports": [
                        {
                            "port" : int(element.port),
                            "targetPort" : int(element.port)
                        }
                    ]
                }

            }
            return object_element
        else:
            return None

