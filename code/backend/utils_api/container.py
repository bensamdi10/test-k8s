
from container.models import Container
from deployment.models import Deployment
from store.models import PersistentVolume, Variable, Template
import uuid
from backend.api.serializers import ContainerSerializer

class ContainerAPI:

    def remove(self, uid):
        element = self.get(uid)
        if not element == None:
            element = element[0]
            element.archive = True
            element.save()

    def saveTemplate(self, uid, data):
        container = self.get(uid)
        if container == None:
            return { "status" : "error", "message" : "Element Not Found" }
        else:
            container = container[0]
            template = Template()
            template.name = self.parseData(data, "name")
            template.description = self.parseData(data, "description")
            template.type = "container"
            uid = self.generateUID()
            template.uid = uid
            template.data = container.commands
            template.save()
            return {"status": "success", "message": "Template Created"}

    def serialize(self, element_object):
        serializer = ContainerSerializer(element_object, many=True).data
        return serializer

    def get(self, uid):
        element = Container.objects.all().filter(uid=uid)
        if element.count() == 1:
            return element
        else:
            return None

    def getVariables(self, uid):
        container = self.get(uid)
        if not container == None:
            variables = container[0].variable.all().filter(archive=False)
            return variables
        else:
            return None

    def generateUID(self):
        return str(uuid.uuid4())[:8]

    def parseData(self, data, label):
        if label in data:
            return data[label]
        else:
            return ""

    def getDeployment(self, uid):
        env = Deployment.objects.all().filter(uid=uid)

        if env.count() == 1:
            return env[0]
        else:
            return None

    def getVolume(self, uid):
        volume = PersistentVolume.objects.all().filter(uid=uid)
        if volume.count() == 1:
            return volume[0]
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
            variable.secret = object["secret_var"]
            variable.uid = self.generateUID()
            variable.save()
            return variable
        else:
            return temp_variable[0]


    def getByID(self, id):
        container = Container.objects.all().filter(id=id)
        if container.count() == 1:
            return container[0]
        else:
            return None

    def save(self, data, element_object=None):
        if element_object == None:
            container = Container()
            uid = self.generateUID()
            container.uid = uid
        else:
            container = element_object

            vars = container.variable.all()
            for vr in vars:
                container.variable.remove(vr)


        uid_deploy = self.parseData(data, "parent")
        deployment = self.getDeployment(uid_deploy)

        if not deployment == None:
            container.name = self.parseData(data, "name")
            container.type = self.parseData(data, "type")
            container.base_image = self.parseData(data, "base_image")
            container.image_name = self.parseData(data, "image_name")
            container.source = self.parseData(data, "source")
            container.port = self.parseData(data, "port")
            container.commands = self.parseData(data, "commands")
            container.cmd = self.parseData(data, "cmd")
            container.volume_path = self.parseData(data, "volume_path")
            container.save()



            list_variables = self.parseData(data, "variables")

            for variable_uid in list_variables:
                variable_item = self.getVariable(variable_uid)
                if not variable_item == None:
                    container.variable.add(variable_item)

            list_variables_items = self.parseData(data, "variables_items")


            print(list_variables_items)
            for var_item in list_variables_items:
                var_item_object = self.saveVariable(var_item)
                if not var_item_object == None:
                    container.variable.add(var_item_object)


            container.deployment.add(deployment)

            return { "status" : "success", "message" : "Saved", "uid" : container.uid, "element" :  "container" }
        else:
            return {"status": "error", "message": "Deployment Not exist", "element" :  "container"}

    def update(self, request, data, element):
        return self.save(request, data, element)


    def createDockerFileContent(self, element):
        list = element.commands
        uid = element.uid
        text_script = "FROM "+element.base_image+"\n\n"
        for item in list:
            text_script += item["command_type"]+ " " + item["command_value"]+"\n\n";

        return { "uid" : uid, "content":  text_script}

    def generateYaml(self, uid, deployment=None):
        element = self.get(uid)
        if not element == None:
            element = element[0]

            cont_variables = element.variable.all().filter(archive=False)
            variables_list = []
            for env in cont_variables:
                env_secret = ""
                if env.secret == True:
                    env_secret = {
                        "secretKeyRef": {
                            "name": env.slug,
                            "key": env.name
                        }
                    }
                    variables_list.append({"name": env.name, "valueFrom": env_secret})
                else:
                    variables_list.append({"name": env.name, "value": env.value})
            split_path = element.volume_path.split("/")
            l_sp = len(split_path)

            volumes = []
            if deployment == None:
                if not element.volume_path == "" and not element.volume_path == " " :
                    volumes.append({
                            "name" : "",
                            "mountPath": element.volume_path,
                            "subPath": split_path[l_sp-1]
                        })
            else:
                volumes_list = deployment.persistent_volume.all().filter(archive=False)
                for vol in volumes_list:
                    if not vol.mount_path == "" and not vol.sub_path == "":
                        object_pvc = {
                            "name": vol.slug,
                            "mountPath": vol.mount_path,
                            "subPath": vol.sub_path
                        }
                        volumes.append(object_pvc)


            dockerfile = self.createDockerFileContent(element)
            object_container = {
                "name": element.slug,
                "image": element.image_name,
                "ports": [{"containerPort": int(element.port)}],
                "volumeMounts": volumes,
                "env": variables_list
            }
            if not element.cmd == "" and not element.cmd == " ":
                object_container["command"] = ["/bin/sh"]
                object_container["args"] = ["-c", element.cmd]

            return { "container" : object_container, "dockerfile" : dockerfile}

    def generateYamlJob(self, uid, deployment=None):
        element = self.get(uid)
        if not element == None:
            element = element[0]

            cont_variables = element.variable.all().filter(archive=False)
            variables_list = []
            for env in cont_variables:
                env_secret = ""
                if env.secret == True:
                    env_secret = {
                        "secretKeyRef": {
                            "name": env.slug,
                            "key": env.name
                        }
                    }
                    variables_list.append({"name": env.name, "valueFrom": env_secret})
                else:
                    variables_list.append({"name": env.name, "value": env.value})
            split_path = element.volume_path.split("/")
            l_sp = len(split_path)

            volumes = []
            if deployment == None:
                volumes.append({
                        "name" : "",
                        "mountPath": element.volume_path,
                        "subPath": split_path[l_sp-1]
                    })
            else:
                volumes_list = deployment.persistent_volume.all().filter(archive=False)
                for vol in volumes_list:
                    object_pvc = {
                        "name": vol.slug,
                        "mountPath": element.volume_path,
                        "subPath": split_path[l_sp - 1]
                    }
                    volumes.append(object_pvc)


            dockerfile = self.createDockerFileContent(element)
            object_container = {
                "name": element.slug,
                "image": element.image_name,
                "command": [element.cmd],
                "env": variables_list
            }
            return { "container" : object_container, "dockerfile" : dockerfile}

    def generateYamlPath(self, uid, path):
        element = self.get(uid)
        if not element == None:

            object_container = {
                "path": path,
                "backend" : {
                    "serviceName" : element.deployment.all()[0].clusterip_set.all()[0].slug,
                    "servicePort" : element.port
                }
            }


            return object_container



