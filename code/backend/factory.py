from backend.utils_api.container import *
from backend.utils_api.project import *
from backend.utils_api.environnement import *
from backend.utils_api.deployment import *
from backend.utils_api.ingress import *
from backend.utils_api.job import *
from backend.utils_api.variable import *
from backend.utils_api.service import *
from backend.utils_api.volume import *
from backend.utils_api.template import *
from backend.utils_api.element_existed import *
import yaml
from django.conf import settings
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import sys
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        self.indent(sequence=4, offset=2)
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

class Factory:

    def correctData(self, data):
        for d in data:
            if data[d] == "true":
                data[d] = True
            if data[d] == "false" or data[d] == None:
                data[d] =  False
        return data

    def getContainers(self, uid):
        utils = self.getUtils("environnement")
        containers = utils.getContainers(uid)
        utils_containers = self.getUtils("container")
        containers = containers.order_by("id")
        result = utils_containers.serialize(containers)

        return result

    def getVolumes(self, uid):
        utils = self.getUtils("environnement")
        volumes = utils.getVolumes(uid)
        utils_volume = self.getUtils("volume")
        volumes = volumes.order_by("id")
        result = utils_volume.serialize(volumes)

        return result

    def getClusters(self, uid):
        utils = self.getUtils("environnement")
        clusters = utils.getClusters(uid)
        utils_deployment = self.getUtils("deployment")
        clusters = clusters.order_by("id")
        result = utils_deployment.serializeClusters(clusters)

        return result

    def save(self, element, data, object=None):
        data = self.correctData(data)
        utils = self.getUtils(element)
        response = { "status" : "error" ,  "message" : "Element Type Not found" }
        if not utils == None:
            if element == "template" :
                response = self.saveTemplate(data)
            else:
                response = self.saveElement(data, object, utils)
        return response

    def update(self, element, data, uid):
        data = self.correctData(data)
        if 'variables_items' in data:
            for dv in data["variables_items"]:
                dv = self.correctData(dv)
        utils = self.getUtils(element)
        object = utils.get(uid)
        response = {"status": "error", "message": "Element Type Not found"}
        if not object == None:
            object = object[0]
            if not utils == None:
                response = self.saveElement(data, object, utils)
            return response

    def updateInline(self, element, data, uid):
        data = self.correctData(data)
        utils = self.getUtils(element)
        object = utils.get(uid)
        response = {"status": "error", "message": "Element Type Not found"}
        if not object == None:
            object = object[0]
            if not utils == None:
                response = self.saveInlineElement(data, object, utils)
            return response

    def get(self, element, uid):
        utils = self.getUtils(element)
        element_object = None
        if not utils == None:
            element_object = utils.get(uid)
        return element_object

    def saveElement(self, data, object, utils):
        return utils.save(data, object)

    def saveInlineElement(self, data, object, utils):
        return utils.saveInline(data, object)

    def getUtils(self, element):
        utils = None
        if element == "project":
            utils = ProjectAPI()

        if element == "environnement":
            utils = EnvironnementAPI()

        if element == "deployment":
            utils = DeploymentAPI()

        if element == "container":
            utils = ContainerAPI()

        if element == "job":
            utils = JobAPI()

        if element == "ingress":
            utils = IngressAPI()

        if element == "variable":
            utils = VariableAPI()

        if element == "service":
            utils = ServiceAPI()

        if element == "volume":
            utils = VolumeAPI()

        if element == "template":
            utils = TemplateAPI()

        if element == "container_existed" or element == "volume_existed":
            utils = ElementExisted()

        return utils

    def getEnvVariables(self, uid):
        utils_env = self.getUtils("environnement")
        variables_env = utils_env.getVariables(uid)
        variables_env = variables_env.order_by("id")
        return utils_env.serializeVariables(variables_env)

    def getByID(self, element, id):
        utils = self.getUtils(element)
        return utils.getByID(id)

    def serialize(self, element, uid):
        utils = self.getUtils(element)
        element_serialize = None
        if not utils == None:
            element_object = utils.get(uid)
            if not element_object == None:
                element_serialize = utils.serialize(element_object)
                utils_variable = self.getUtils("variable")
                if element == "job":
                    container_object = None
                    if len(element_serialize[0]["container"]) > 0 :
                        container_object = self.getByID("container", element_serialize[0]["container"][0])
                    if not container_object == None:
                        element_serialize[0]["container"] = container_object.uid

                if element == "service" or element == "container" :
                    variables = utils.getVariables(element_object[0].uid)
                    if not variables == None:
                        element_serialize[0]["variables"] = utils_variable.serialize(variables)

                if element == "ingress":
                    utils_env = self.getUtils("environnement")
                    clusters = utils_env.getClusters(element_object[0].environnement.uid)

                    utils_deployment = self.getUtils("deployment")
                    clusters = clusters.order_by("-id")
                    element_serialize[0]["clusters"] = utils_deployment.serializeClusters(clusters)

        return element_serialize

    def saveTemplate(self, data):
        utils = self.getUtils(data["parent"])
        response = {"status": "error", "message": "Element Type Not found"}
        if not utils == None:
            response = utils.saveTemplate(data["uid"], data)
        return response

    def getTemplates(self, element):
        utils = self.getUtils("template")
        templates = utils.getTemplates(element)
        return utils.serialize(templates)

    def deleteElement(self, element, uid):
        utils = self.getUtils(element)
        utils.remove(uid)

    def createFiles(self, list, environnement_element):
        base_dir = os.path.join(settings.BASE_DIR, 'yaml')
        base_dir = os.path.join(base_dir, environnement_element.project.slug )
        base_dir = os.path.join(base_dir, environnement_element.slug )
        for item in list:
            if "extension" in item:
                path_file = os.path.join(base_dir, item["slug"] + "."+item["extension"])
            else:
                path_file = os.path.join(base_dir, item["slug"]+".yaml")
            default_storage.save(path_file, ContentFile(item["document"]))

    def generateYaml(self, element, uid):
        utils = self.getUtils(element)
        environnement_element = utils.get(uid)[0]
        deployments = utils.getDeployments(uid)
        ingress = utils.getIngress(uid)[0]
        jobs = utils.getJobs(uid)
        volumes = utils.getVolumes(uid)
        services = utils.getServices(uid)

        yaml_deployments = self.deploymentUtilsYaml(deployments)
        yaml_ingress = self.ingressUtilsYaml(ingress)
        yaml_job = self.jobUtilsYaml(jobs)
        yaml_volumes = self.volumeUtilsYaml(volumes)
        yaml_services = self.serviceUtilsYaml(services, environnement_element)

        env_variables = self.generateVariables(environnement_element, utils)

        list_files = yaml_deployments+yaml_ingress+yaml_job+yaml_volumes+yaml_services
        self.createFiles(list_files, environnement_element)
        return { "documents" : list_files, "project_slug" : environnement_element.project.slug, "env_slug" : environnement_element.slug, "variables" : env_variables }

    def generateVariables(self, environnement, utils):

        cont_variables = utils.getVariables(environnement.uid)
        variables_list = []
        for env in cont_variables:
            variables_list.append({"name": env.name, "value" : env.value, "secret": env.secret, "slug" : env.slug })
        return variables_list

    def serviceUtilsYaml(self, services, environnement):
        list_files = []
        for service in services:
            utils_service = self.getUtils('service')
            object_service = utils_service.generateYaml(service.uid, environnement)
            yaml_service = self.generateYamlDocument(object_service["document"])

            list_files.append(
                {"name": service.name, "slug": "."+service.type, "extension" : "yml", "document": yaml_service, "script" : object_service["script"],
                 "object": object_service})
        return list_files

    def volumeUtilsYaml(self, volumes):
        list_files = []
        for volume in volumes:
            utils_volume = self.getUtils('volume')
            object_volume = utils_volume.generateYaml(volume.uid)
            list_files.append({"name": volume.name, "slug": volume.slug, "document": self.generateYamlDocument(object_volume), "object": object_volume})
        return list_files

    def jobUtilsYaml(self, jobs):
        list_files = []
        for job in jobs:
            utils_deploy = self.getUtils('job')
            object_job = utils_deploy.generateYaml(job.uid)
            containers_job = job.container.all().filter(archive=False)
            containers = []
            for cont in containers_job:
                utils_container = self.getUtils('container')
                object_container = utils_container.generateYamlJob(cont.uid)
                object_container["container"]["command"] = [job.command]
                containers.append(object_container["container"])




            if len(containers) == 0:
                name_image = job.container_image.split("/")[1].split(":")[0]
                containers = [{
                        "name": name_image,
                        "image": job.container_image,
                        "command": [job.command],
                    }]
            if job.type == "job":
                object_job["spec"]["template"]["spec"]["containers"] = containers
            if job.type == "cron":
                object_job["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"] = containers


            list_files.append(
                {"name": job.name, "slug": job.slug, "document": self.generateYamlDocument(object_job),
                 "object": object_job})
        return list_files

    def ingressUtilsYaml(self, ingress):
        list_files = []
        utils_ingress = self.getUtils('ingress')
        object_ingress = utils_ingress.generateYaml(ingress.uid)

        list_files.append({"name": ingress.name, "slug": ingress.slug, "object": object_ingress,  "document": self.generateYamlDocument(object_ingress)})

        return list_files

    def deploymentUtilsYaml(self, deployments ):
        list_files = []
        for deploy in deployments:
            utils_deploy = self.getUtils('deployment')
            object_deploy = utils_deploy.generateYaml(deploy.uid)
            object_cluser_ip = utils_deploy.generateClusterIpYaml(deploy.uid)
            cluster_ip = deploy.clusterip_set.all()[0]
            containers_deployment = deploy.container_set.all().filter(archive=False)
            containers = []
            dockerfiles = []
            for cont in containers_deployment:
                utils_container = self.getUtils('container')
                object_container = utils_container.generateYaml(cont.uid, deploy)
                document_container = object_container["container"]
                dockerfile_container = object_container["dockerfile"]
                containers.append(document_container)
                dockerfiles.append(dockerfile_container)
            object_deploy["spec"]["template"]["spec"]["containers"] = containers
            list_files.append( { "name" : deploy.name, "slug" : deploy.slug, "document" : self.generateYamlDocument(object_deploy), "object" : object_deploy, "dockerfile": dockerfiles } )
            list_files.append( { "name" : cluster_ip.name, "slug" : cluster_ip.slug, "document" : self.generateYamlDocument(object_cluser_ip), "object" : object_cluser_ip } )
        return list_files

    def generateYamlDocument(self,object):
        my_yaml = MyYAML()
        return my_yaml.dump(dict(object))