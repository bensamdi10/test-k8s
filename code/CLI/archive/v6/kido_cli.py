# coding: utf-8
import asyncio
import websockets
import os
import requests
import json
from pathlib import Path
import subprocess
from utils.virtualbox_utils import VirtualBoxUtils
import shutil
import copy
import time
NUMBER_PEER = 5
PORT = 8002


from kubernetes import client, config, watch

from utils.kubernetes_utils import KubernetesUtils


class KidoCLI:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH_CREDITS = os.path.join(BASE_DIR, "store")
    DOMAIN = "http://192.168.1.102:8002"
    DOMAIN_WS = "ws://192.168.1.102"
    TOKEN = ""
    variables = []
    socket = ""
    current = {}
    stop_watch_pods = False

    def __init__(self, **kwargs):
        self.DOMAIN_WS_IP = "ws://192.168.1.102:8002"
        self.loop = kwargs.get('loop', None) or asyncio.get_event_loop()
        self.virtualbox = VirtualBoxUtils()

        self.k8s = KubernetesUtils()
        #result = self.k8s.getEvents()


    async def runCommand(self, command , websocket, data_init,):
        #subprocess.check_call([command], stderr=subprocess.PIPE)
        processus = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



        for line in processus.stdout:
            line = line.decode("utf-8")
            line = str(line)
            line = line.replace("\n", "")
            data_send_initial = self.sendOutput(self.cloneData( data_init, { "output" : line, "action" : "output-terminal", "finish_output": "false" } ))
            await websocket.send(data_send_initial)

        output, error = processus.communicate()

        if processus.returncode != 0:
            return_code = str(processus.returncode)
            message_error = str(return_code) + " "+str(error)
            data_send_termine = self.sendOutput(self.cloneData( data_init, { "output" : message_error, "action" : "output-terminal", "finish_output": "true" } ))
            await websocket.send(data_send_termine)

            return False

        data_send_termine = self.sendOutput(self.cloneData( data_init, { "output" : "", "action" : "output-terminal", "finish_output": "true" } ))
        await websocket.send(data_send_termine)

    async def runTaskCommands(self, list_commands, websocket, data_init, message_termine=""):
        pass_all = True
        for command in list_commands:
            result = await self.runCommand(command, websocket, data_init)
            if result == False:
                pass_all = False
                break
        if pass_all == True:
            data_send_termine = self.sendOutput(self.cloneData( data_init, { "output" : message_termine, "action" : "output-terminal", "finish_output": "true" } ))
            await websocket.send(data_send_termine)

    async def inirEnvironnement(self):
        data_send_vm = self.sendOutput("Create VM for The Environnement", uid, "output-terminal", [], "", "false")
        await websocket.send(data_send_vm)
        commands_vm = self.virtualbox.installVbox()
        await self.runTaskCommands(commands_vm, websocket, recev_data, "VM Created Successfully", "false")

        data_send_kubectl = self.sendOutput("Install Kubectl", uid, "output-terminal", [], "", "false")
        await websocket.send(data_send_kubectl)
        commands_kubectl = self.virtualbox.installKubectl()
        await self.runTaskCommands(commands_kubectl, websocket, recev_data, "Kubectl Installed Successfully", "false")

        data_send_docker = self.sendOutput("Install Docker Engine", uid, "output-terminal", [], "", "false")
        await websocket.send(data_send_docker)
        commands_docker = self.virtualbox.installDocker()
        await self.runTaskCommands(commands_docker, websocket, recev_data, "Docker Installed Successfully", "false")

        data_send_minikube = self.sendOutput("Install Minikube", uid, "output-terminal", [], "", "false")
        await websocket.send(data_send_minikube)
        commands_minikube = self.virtualbox.installMinikube()
        await self.runTaskCommands(commands_minikube, websocket, recev_data, "Minikube Installed Successfully", "false")
        data_send_start_minikube = self.sendOutput("Installation in finished", uid, "output-terminal", [], "", "true")
        await websocket.send(data_send_start_minikube)


    def runCommandSync(self, command):
        processus = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = processus.communicate()
        data_send_termine = ""
        if processus.returncode != 0:
            return_code = str(processus.returncode)
            data_send_termine = str(return_code) + " " + str(error)
        return data_send_termine

    async def runTaskCommandsSync(self, list_commands, websocket, data_init, display_message=True):
        for command in list_commands:
            print(command)
            message_termine = self.runCommandSync(command)
            print(message_termine)
            print("----")
            if display_message == True:
                data_send_termine = self.sendOutput(self.cloneData( data_init, { "output" : message_termine, "action" : "output-terminal", "finish_output": "true" } ))
                await websocket.send(data_send_termine)

    async def runContainer(self, websocket, data_init):
        path = "./store/yaml/"+data_init["context"]["project_name"]+"/"+data_init["context"]["env_name"]+"/code"
        path_file = "./store/yaml/" + data_init["context"]["project_name"] + "/" + data_init["context"]["env_name"]
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(BASE_DIR, 'store')
        base_dir = os.path.join(base_dir, 'yaml')
        base_dir = os.path.join(base_dir, data_init["context"]["project_name"])
        base_dir = os.path.join(base_dir, data_init["context"]["env_name"])


        base_dir = os.path.join(base_dir, "code")
        Path(base_dir).mkdir(parents=True, exist_ok=True)



        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        # for running the commands inside the container like the terminal normal : docker exec -it plateforme_container ls
        commands_container = self.virtualbox.runContainer(data_init, path, path_file)
        await self.runTaskCommandsSync(commands_container, websocket, data_init)
        #os.system("chmod 777 -R store/yaml/" + data_init["context"]["project_name"] + "/")
        workdir_container = "<"+data_init["context"]["name"]+"> # "
        data_send_message = self.sendOutput(self.cloneData( data_init, { "output" : "Image of Container "+data_init["context"]["name"], "action" : "run-inside-container", "finish_output": "true", "workdir" : workdir_container } ))
        await websocket.send(data_send_message)

    def cloneData(self, data, new_dict):
        dict_output = copy.deepcopy(data)
        for key in new_dict:
            if key in data:
                dict_output[key] = new_dict[key]

        return dict_output


    async def connect(self, uri):
            async with websockets.connect(uri) as websocket:
                while True:
                    recev_data = await websocket.recv()
                    recev_data = json.loads(recev_data)
                    uid = recev_data["uid"]
                    action = recev_data["action"]

                    if action == "delete-deployment" or action == "restart-deployment" or action == "journal-deployment":
                        await self.applyDeploymentAction(uid, websocket, recev_data)

                    if action == "run-env":
                        running_minikube = await self.runEnv(uid, websocket, recev_data)
                        if running_minikube == True:
                            await self.watchPods(websocket, recev_data)


                    if action == "input-terminal":
                        if recev_data["input"] == "exit" or recev_data["input"] == "exit()" :
                            data_send_exit = self.sendOutput(self.cloneData( recev_data, { "output" : "", "action" : "output-terminal", "finish_output": "true" } ))
                            await websocket.send(data_send_exit)

                        await self.runCommand(recev_data["input"], websocket,  recev_data)

                    if action == "input-inside-container":
                        if recev_data["input"] == "exit" or recev_data["input"] == "exit()" :
                            data_send_exit = self.sendOutput(self.cloneData( recev_data, { "output" : "", "action" : "output-terminal", "finish_output": "true" } ))
                            await websocket.send(data_send_exit)

                        #command_container = "docker exec -it "+self.current["name"]+" " +str(recev_data["input"])
                        command_container = "docker run -it "+recev_data["context"]["name"]+" "+str(recev_data["input"])
                        command_container = command_container.replace("\n", "").replace("\n", "")
                        recev_data["workdir"] =  "<"+recev_data["context"]["name"]+"> # "
                        await self.runCommand( command_container, websocket,  recev_data)

                    if action == "run-container":

                        data_send_initial = self.sendOutput(self.cloneData( recev_data, { "output" : "Start Running the Environnement for Run the Container.", "action" : "output-terminal", "finish_output": "false" } ))
                        await websocket.send(data_send_initial)

                        data_send_start = self.sendOutput(self.cloneData( recev_data, { "output" : "Generate Files Config for Run the Container...", "action" : "output-terminal", "finish_output": "false" } ))
                        await websocket.send(data_send_start)

                        data_files = self.generateYamlFiles(recev_data)
                        await websocket.send(data_files)

                        #dict_data_files = json.loads(data_files)
                        await self.runContainer(websocket, recev_data)





    async def applyDeploymentAction(self, uid, websocket, data_init):
        action = data_init["action"]
        if action == "delete-deployment":
            slug = data_init["context"]["deployment_slug"]
            command = "kubectl delete -n default deployment  "+slug
            print(command)
            output_command = self.runCommandSync(command)
            print(output_command)
            print("------------+++")
        if action == "restart-deployment":
            slug = data_init["context"]["deployment_slug"]
            command_apply = "kubectl apply -f ./store/yaml/" + data_init["context"]["slug_project"] + "/" + data_init["context"]["slug_env"] + "/k8s/"+slug+".yaml"
            output_command = self.runCommandSync(command_apply)
            print(output_command)
            print("------------+++")

        if action == "journal-deployment":
            slug = data_init["context"]["deployment_slug"]
            command_apply = "kubectl apply -f ./store/yaml/" + data_init["context"]["slug_project"] + "/" + data_init["context"]["slug_env"] + "/k8s/"+slug+".yaml"
            output_command = self.runCommandSync(command_apply)
            print(output_command)
            print("------------+++")

    async def watchPods(self, websocket=None, recev_data=None):
        print("watch start")
        config.load_kube_config()
        v1 = client.CoreV1Api()
        v1.api_client.configuration.verify_ssl = False


        w = watch.Watch()
        ingress_apply = False
        for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=30):
            #try:

            ip_minikube = subprocess.run(["minikube ip"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ip_minikube = ip_minikube.stdout

            ip_minikube = ip_minikube.decode("utf-8")
            ip_minikube = str(ip_minikube)
            ip_minikube = ip_minikube.replace("\n", "")
            if ingress_apply == False:
                data_send_ip = self.sendOutput(self.cloneData(recev_data,  {"output": ip_minikube, "action": "output-ingress",  "finish_output": "true"}))
                await websocket.send(data_send_ip)
            ingress_apply = True

            if self.stop_watch_pods == True:
                w.stop()
            else:
                event_object = event['object'].to_dict()
                action = event["type"]
                if not event_object["metadata"]["generate_name"] == None and not event_object["metadata"]["generate_name"] == "None":
                    if 'component' in event_object["metadata"]["labels"]:
                        name = event_object["metadata"]["labels"]["component"]

                    else:
                        name = event_object["metadata"]["generate_name"]

                    if "name" in event_object["metadata"]:
                        name_hash = event_object["metadata"]["name"]
                    else:
                        name_hash = event_object["metadata"]["generate_name"]

                    hash_object = ""
                    if "pod-template-hash" in event_object["metadata"]["labels"]:
                        hash_object = event_object["metadata"]["labels"]["pod-template-hash"]

                    phase = event_object["status"]["phase"]
                    conditions = event_object["status"]["conditions"]
                    if not conditions == None:
                        l_conditions = len(conditions)
                        message_condition = conditions[l_conditions - 1]["message"]
                        reason_condition = conditions[l_conditions - 1]["reason"]
                        type_condition = conditions[l_conditions - 1]["type"]

                        result_event = {"name": name, "action": action, "name_hash": name_hash, "hash": hash_object,
                                        "phase": phase, "message": message_condition, "reason": reason_condition,
                                        "type": type_condition}
                        data_send_event = self.sendOutput(self.cloneData(recev_data,{"output": result_event, "action": "output-events", "finish_output": "false"}))
                        await websocket.send(data_send_event)

            #except:
            #print("Close")
            #w.stop()

        #w.stop()


    async def runEnv(self, uid, websocket, recev_data, waiting=False):
        if waiting == False:
            self.current = {"element": "environnement", "uid": uid}
            data_send_initial = self.sendOutput(self.cloneData(recev_data, {"output": "Start Running the Environnement for your project...", "action": "output-terminal","finish_output": "false"}))

            await websocket.send(data_send_initial)

            data_send_start = self.sendOutput(self.cloneData(recev_data,{"output": "Generate Files Config for Kubernetes Cluster...","action": "output-terminal", "finish_output": "false"}))
            await websocket.send(data_send_start)

            data_files = self.generateYamlFiles(recev_data)
            await websocket.send(data_files)

            data_send_start_minikube = self.sendOutput(self.cloneData(recev_data, {"output": "Start Minikube ...","action": "output-terminal","finish_output": "false"}))

            await websocket.send(data_send_start_minikube)
            commands_start_minikube = self.virtualbox.startMinikube(recev_data["context"]["project_name"], recev_data["context"]["env_name"])
            await self.runTaskCommandsSync(commands_start_minikube, websocket, recev_data, False)

        output_verify = self.verifyRunningMinikube()
        if len(output_verify.split("Running")) >= 3:
            result = True
            command_apply = "kubectl apply -f ./store/yaml/"+recev_data["context"]["slug_project"]+"/"+recev_data["context"]["slug_env"]+"/k8s"
            subprocess.run([command_apply], shell=True)
            return result
        else:
            time.sleep(3)
            self.runEnv(uid, websocket, recev_data, True)

    def verifyRunningMinikube(self):
        command_status = "minikube status"
        res = subprocess.run([command_status], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = str(res.stdout)
        return output

    def initCLI(self):
        self.TOKEN = self.getToken()
        uri = self.DOMAIN_WS + ":" + str(PORT) + "/connection-cli/"

        asyncio.get_event_loop().run_until_complete(self.connect(uri))
        #asyncio.get_event_loop().close()

        return self.TOKEN

    def getToken(self):
        credits_content = self.checkFileCredits()
        if credits_content == None:
            return self.createCredits("all", "default")
        else:
            return credits_content

    def generateCredits(self, token, name_space):
        url = self.DOMAIN+"/api/backend/get-cli-credits/"+token+"/"+name_space+"/"
        r = requests.get(url)
        data = r.json()
        return data

    def checkFileCredits(self):
        path_file = os.path.join(self.PATH_CREDITS, "credits.cre")
        try:
            f = open(path_file)
            result = f.readlines()
            f.close()
            return result
        except IOError:
            return None

    def createCredits(self, token, name_space):
        credits = self.generateCredits(token, name_space)
        path_file = os.path.join(self.PATH_CREDITS, "credits.cre")
        f = open(path_file, "a")
        f.write(credits["token"])
        f.close()
        return credits

    def createFiles(self, list, project_slug, env_slug, type_element="document"):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(BASE_DIR, 'store')
        base_dir = os.path.join(base_dir, 'yaml')
        base_dir = os.path.join(base_dir, project_slug)

        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

        Path(base_dir).mkdir(parents=True, exist_ok=True)
        base_dir = os.path.join(base_dir, env_slug)
        base_dir_k8s = os.path.join(base_dir, "k8s")

        Path(base_dir).mkdir(parents=True, exist_ok=True)
        Path(base_dir_k8s).mkdir(parents=True, exist_ok=True)

        os.system("chmod 777 -R "+base_dir)
        os.system("chmod 777 -R "+base_dir_k8s)

        for item in list:
            if "script" in item :
                path_file = os.path.join(base_dir, "deploy_"+item["script"]["type"]+".sh")
                with open(path_file, 'w') as file:
                    file.write(item["script"]["content"])
            if "dockerfile" in item:
                for dokfile in item["dockerfile"]:
                    path_dockerfile = os.path.join(base_dir, "Dockerfile_" + dokfile["uid"] + ".file")
                    with open(path_dockerfile, 'w') as file:
                        file.write(dokfile["content"])

            if "extension" in item:
                path_file = os.path.join(base_dir, item["slug"] + "." + item["extension"])
            else:
                path_file = os.path.join(base_dir_k8s, item["slug"] + ".yaml")

            with open(path_file, 'w') as file:
                file.write(item["document"])

    def generateYamlFiles(self, data_init):
        uid = data_init["uid"]
        url = self.DOMAIN+"/api/backend/generate-yaml-cli/"+uid+"/"
        r = requests.get(url)
        data = r.json()
        documents = data["documents"]
        self.variables = data["variables"]
        project_slug = data["project_slug"]
        env_slug = data["env_slug"]
        for variable in self.variables:
            if variable["secret"] == True or variable["secret"] == 'true':
                command_secret = "kubectl create secret generic "+variable["slug"]+" --from-literal="+variable["name"]+"="+variable["value"]
                try:
                    subprocess.run([command_secret], shell=True)
                except:
                    pass

        self.createFiles(documents, project_slug, env_slug, "document")
        subprocess.run(["chmod 777 -R ./store/yaml/"+project_slug+"/"], shell=True)
        subprocess.run(["chmod 777 -R ./store/yaml/"+project_slug+"/"+env_slug+"/"], shell=True)
        return self.sendOutput(self.cloneData( data_init, { "output" : "Files Generating with Success", "action" : "output-terminal", "finish_output": "false" } ))

    def sendOutput(self, data):
        '''
        data = {
            "action": action,
            "uid": uid,
            "output": output,
            "input": "",
            "output_errors" : errors,
            "workdir" : workdir,
            "finish_output" : finish_output,
            "extra_data" : extra_data,
            "context" : context_dict
        }
        '''
        if data["finish_output"] == "true" :
            data["context"]["status"] = "finished"

        data = json.dumps(data)
        return data