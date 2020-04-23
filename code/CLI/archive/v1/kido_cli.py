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

    def __init__(self, **kwargs):
        self.DOMAIN_WS_IP = "ws://192.168.1.102:8002"
        self.loop = kwargs.get('loop', None) or asyncio.get_event_loop()
        self.virtualbox = VirtualBoxUtils()




    async def runCommand(self, command , websocket, data_init):
        processus = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in processus.stdout:
            line = line.decode("utf-8")
            line = str(line)
            line = line.replace("\n", "")
            data_send_initial = self.sendOutput(line, data_init["uid"], "output-terminal", [], "", "false")
            await websocket.send(data_send_initial)

        data_send_termine = self.sendOutput("", data_init["uid"], "output-terminal", [], "", "true")
        await websocket.send(data_send_termine)


    async def connect(self, uri):

            with concurrent.futures.ProcessPoolExecutor() as pool_exec:
                async with websockets.connect(uri) as websocket:
                    while True:
                        recev_data = await websocket.recv()
                        recev_data = json.loads(recev_data)
                        uid = recev_data["uid"]
                        action = recev_data["action"]
                        if action == "run-env":

                            data_send_initial = self.sendOutput("Start Running the Environnement for your project...", uid, "output-terminal", [], "false")
                            await websocket.send(data_send_initial)

                            await self.runCommand("apt-get install vim -y", websocket, recev_data)

                            '''
                            data_files = self.generateYamlFiles("environnement", uid)
                            await websocket.send(data_files)

                            data_send_vm = self.sendOutput(line, uid,  "output-terminal", [], "", "false")
                            await websocket.send(data_send_vm)

                            
                            data_send_vm = self.sendOutput("Create VM for The Environnement", uid,  "output-terminal", [], "", "false")
                            await websocket.send(data_send_vm)
                            self.virtualbox.installVbox()

                            data_send_kubectl = self.sendOutput("Install Kubectl", uid, "output-terminal", [], "", "false")
                            await websocket.send(data_send_kubectl)
                            self.virtualbox.installKubectl()

                            data_send_docker = self.sendOutput("Install Docker", uid, "output-terminal", [], "", "false")
                            await websocket.send(data_send_docker)
                            self.virtualbox.installDocker()

                            data_send_minikube = self.sendOutput("Install Minikube", uid, "output-terminal", [], "", "false")
                            await websocket.send(data_send_minikube)
                            self.virtualbox.installMinikube()

                            data_send_start_minikube = self.sendOutput("Start Minikube", uid, "output-terminal", [], "", "false")
                            await websocket.send(data_send_start_minikube)
                            output_minikube = self.virtualbox.startMinikube()

                            data_send_output_minikube = self.sendOutput(output_minikube["output"], uid, "output-terminal", output_minikube["errors"], "", "false")
                            await websocket.send(data_send_output_minikube)
                            



                            await websocket.send(data_send)
                            
                            '''

                        if action == "input-terminal":
                            data_send = self.runCommandTerminal(recev_data)
                            await websocket.send(data_send)

    def initCLI(self):
        self.TOKEN = self.getToken()
        uri = self.DOMAIN_WS + ":" + str(PORT) + "/connection-cli/"
        asyncio.get_event_loop().run_until_complete(self.connect(uri))
        asyncio.get_event_loop().close()

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
        return self.sendOutput("Files Generating with Success", uid, "output-terminal", [], "")

    def runCommandsYaml(self, uid, action):
        command_ls = ["ls"]
        result_command = command_line.run(command_ls[0])
        output = result_command["output"]
        output_errors = result_command["errors"]

        return self.sendOutput(output, uid, action, output_errors)


    def sendOutput(self, output, uid, action, errors, workdir="", finish_output="true"):
        data = {
            "action": action,
            "uid": uid,
            "output": output,
            "input": "",
            "output_errors" : errors,
            "workdir" : workdir,
            "finish_output" : finish_output
        }
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



