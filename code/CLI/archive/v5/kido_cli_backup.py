# coding: utf-8
import asyncio
import websockets
import os
import requests
import json
import concurrent.futures
from pathlib import Path
import subprocess
import click
from utils.command import CommandLine

from utils.virtualbox_utils import VirtualBoxUtils

import shutil

NUMBER_PEER = 5
PORT = 8002



command_line = CommandLine()


class KidoCLI:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH_CREDITS = os.path.join(BASE_DIR, "store")
    DOMAIN = "http://192.168.1.102:8002"
    DOMAIN_WS = "ws://192.168.1.102"
    TOKEN = ""
    variables = []
    socket = ""
    current = {}

    def __init__(self, **kwargs):
        self.DOMAIN_WS_IP = "ws://192.168.1.102:8002"
        self.loop = kwargs.get('loop', None) or asyncio.get_event_loop()
        self.virtualbox = VirtualBoxUtils()

    async def runCommand(self, command , websocket, data_init, finish="true", workdir="", context={}):
        #subprocess.check_call([command], stderr=subprocess.PIPE)
        processus = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



        for line in processus.stdout:
            line = line.decode("utf-8")
            line = str(line)
            line = line.replace("\n", "")
            data_send_initial = self.sendOutput(line, data_init["uid"], "output-terminal", [], "", "false",  context)
            await websocket.send(data_send_initial)

        output, error = processus.communicate()

        if processus.returncode != 0:
            return_code = str(processus.returncode)
            message_error = str(return_code) + " "+str(error)
            data_send_termine = self.sendOutput(message_error, data_init["uid"], "output-terminal", [], workdir, "true", context)
            await websocket.send(data_send_termine)

            return False

        data_send_termine = self.sendOutput("", data_init["uid"], "output-terminal", [], workdir, finish)
        await websocket.send(data_send_termine)

    async def runTaskCommands(self, list_commands, websocket, data_init, message_termine="", finish="true", context={}):
        pass_all = True
        for command in list_commands:
            result = await self.runCommand(command, websocket, data_init, finish, context)
            if result == False:
                pass_all = False
                break
        if pass_all == True:
            data_send_termine = self.sendOutput(message_termine, data_init["uid"], "output-terminal", [], "", "true", context)
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


    def runCommandSync(self, command, data_init, finish, context):
        processus = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = processus.communicate()
        data_send_termine = ""
        if processus.returncode != 0:
            return_code = str(processus.returncode)
            data_send_termine = str(return_code) + " " + str(error)
        return data_send_termine

    async def runTaskCommandsSync(self, list_commands, websocket, data_init, finish="true", context):
        for command in list_commands:
            click.echo(command)
            message_termine = self.runCommandSync(command, data_init, finish)
            click.echo(message_termine)
            data_send_termine = self.sendOutput(message_termine, data_init["uid"], "output-terminal", [], "", "true", context)
            await websocket.send(data_send_termine)

    async def runContainer(self, uid, websocket, data_init, extra_data):
        path = "./store/yaml/"+extra_data["project"]+"/"+extra_data["env"]+"/code"
        path_file = "./store/yaml/" + extra_data["project"] + "/" + extra_data["env"]
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(BASE_DIR, 'store')
        base_dir = os.path.join(base_dir, 'yaml')
        base_dir = os.path.join(base_dir, extra_data["project"])
        base_dir = os.path.join(base_dir, extra_data["env"])


        base_dir = os.path.join(base_dir, "code")
        Path(base_dir).mkdir(parents=True, exist_ok=True)
        os.system("chmod 777 -R store/yaml/" + extra_data["project"] + "/")


        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        # for running the commands inside the container like the terminal normal : docker exec -it plateforme_container ls
        commands_container = self.virtualbox.runContainer(data_init, path, path_file)
        await self.runTaskCommandsSync(commands_container, websocket, data_init, "false" )

        extra_data["action"] = "run-inside-container"
        extra_data["name"] = self.current["name"]
        self.current["action"] = "run-inside-container"
        data_send_message = self.sendOutput("Image of Container "+data_init['extra_data']['name'],  data_init["uid"], "run-inside-container", [], "<"+self.current["name"]+"> # ", "true", extra_data)
        await websocket.send(data_send_message)



    async def connect(self, uri):
            async with websockets.connect(uri) as websocket:
                while True:
                    recev_data = await websocket.recv()
                    recev_data = json.loads(recev_data)
                    uid = recev_data["uid"]
                    action = recev_data["action"]
                    context = recev_data["context"]



                    if action == "run-env":
                        self.current = { "element" : "environnement", "uid" : uid }

                        data_send_initial = self.sendOutput("Start Running the Environnement for your project...", uid, "output-terminal", [], "", "false", "", context)
                        await websocket.send(data_send_initial)

                        data_send_start = self.sendOutput("Generate Files Config for Kubernetes Cluster...", uid, "output-terminal", [], "","false", "", context)
                        await websocket.send(data_send_start)

                        data_files = self.generateYamlFiles("environnement", uid)
                        await websocket.send(data_files)

                        data_send_start_minikube = self.sendOutput("Start Minikube", uid, "output-terminal", [], "", "false", "", context)
                        await websocket.send(data_send_start_minikube)
                        commands_start_minikube = self.virtualbox.startMinikube()
                        await self.runTaskCommands(commands_start_minikube, websocket, recev_data, "Minikube Started", "true", "", context)

                    if action == "input-terminal":
                        if recev_data["input"] == "exit" or recev_data["input"] == "exit()" :
                            data_send_exit = self.sendOutput("", uid, "output-terminal", [], "", "true")
                            await websocket.send(data_send_exit)

                        await self.runCommand(recev_data["input"], websocket,  recev_data, "", "true")

                    if action == "input-inside-container":
                        if recev_data["input"] == "exit" or recev_data["input"] == "exit()" :
                            data_send_exit = self.sendOutput("", uid, "output-terminal", [], "", "true", "", context)
                            await websocket.send(data_send_exit)

                        #command_container = "docker exec -it "+self.current["name"]+" " +str(recev_data["input"])
                        command_container = "docker run -it "+self.current["name"]+" "+str(recev_data["input"])
                        command_container = command_container.replace("\n", "").replace("\n", "")
                        click.echo(command_container)
                        await self.runCommand( command_container, websocket,  recev_data, "true", "<"+self.current["name"]+"> # ", context)

                    if action == "run-container":

                        data_send_initial = self.sendOutput("Start Running the Environnement for Run the COntainer.", uid, "output-terminal", [], "", "false")
                        await websocket.send(data_send_initial)

                        data_send_start = self.sendOutput("Generate Files Config for Run the Container...", uid, "output-terminal", [], "", "false")
                        await websocket.send(data_send_start)

                        data_files = self.generateYamlFiles("environnement", uid)
                        await websocket.send(data_files)

                        dict_data_files = json.loads(data_files)
                        self.current = {"element": "container", "uid": recev_data['extra_data']['uid'], "name" : recev_data['extra_data']['name']}
                        await self.runContainer(uid, websocket, recev_data, dict_data_files["extra_data"])


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

    def generateYamlFiles(self, element, uid):
        url = self.DOMAIN+"/api/backend/generate-yaml-cli/"+uid+"/"
        r = requests.get(url)
        data = r.json()
        documents = data["documents"]
        self.variables = data["variables"]
        project_slug = data["project_slug"]
        env_slug = data["env_slug"]
        self.createFiles(documents, project_slug, env_slug, "document")
        return self.sendOutput("Files Generating with Success", uid, "output-terminal", [], "", "false", {"env" : env_slug, "project" : project_slug} )

    def runCommandsYaml(self, uid, action):
        command_ls = ["ls"]
        result_command = command_line.run(command_ls[0])
        output = result_command["output"]
        output_errors = result_command["errors"]

        return self.sendOutput(output, uid, action, output_errors)

    def sendOutput(self, output, uid, action, errors, workdir="", finish_output="true", extra_data={}, context_dict={}):
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

        if finish_output == "true" :
            context_dict["status"] = "finished"
        data = json.dumps(data)
        return data

    def runCommandTerminal(self, data):
        uid = data["uid"]
        command = str(data["input"])
        result_command = command_line.run(command, data["workdir"])
        output = result_command["output_strip"]
        output_errors = result_command["errors"]
        output_cd = result_command["cd_output"]
        if output_cd == "":
            return self.sendOutput(output, uid, "output-terminal", output_errors, output_cd)
        else:
            return self.sendOutput(output, uid, "change-dir", output_errors, output_cd)



