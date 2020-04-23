# coding: utf-8
import asyncio
import websockets
import os
import requests
import json
import concurrent.futures
from pathlib import Path
from datetime import datetime
import click
from utils.command import CommandLine

NUMBER_PEER = 5
PORT = 8004
async def connect(uri, action="connect", data={}):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool_exec:
        async with websockets.connect(uri) as websocket:
            while True:
                #await websocket.send({ "token" : "1578977897" })
                recev_data = await websocket.recv()
                recev_data = json.loads(recev_data)
                loop.run_in_executor(pool_exec, convertData, recev_data)


async def sendData(uri, data, ):
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)



command_line = CommandLine()
class KidoCLI:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH_CREDITS = os.path.join(BASE_DIR, "store")
    DOMAIN = "http://localhost:8004"
    DOMAIN_WS = "ws://localhost"
    TOKEN = ""
    variables = []
    socket = ""


    def __init__(self, **kwargs):
        self.DOMAIN_WS_IP = "ws://192.168.1.102:8004"
        self.loop = kwargs.get('loop', None) or asyncio.get_event_loop()


    async def connect(self, uri):
            loop = asyncio.get_event_loop()
            with concurrent.futures.ProcessPoolExecutor() as pool_exec:
                async with websockets.connect(uri) as websocket:
                    while True:
                        #await websocket.send('{"uid": "uid", "action": "none", "input": "", "output": [], "output_errors": []})
                        recev_data = await websocket.recv()
                        recev_data = json.loads(recev_data)
                        uid = recev_data["uid"]
                        action = recev_data["action"]
                        if action == "run-env":
                            data_send = self.generateYamlFiles("environnement", uid)
                            await websocket.send(data_send)

                        if action == "input-terminal":
                            data_send = self.runCommandTerminal(recev_data)
                            click.echo(data_send)
                            click.echo("-----------------------------------------------------")
                            await websocket.send(data_send)

                        #loop.run_in_executor(pool_exec, convertData, recev_data)




    def initCLI(self):
        self.TOKEN = self.getToken()

        #task = self.loop.create_task(self.foo(uri))
        uri = self.DOMAIN_WS + ":" + str(PORT) + "/connection-cli/"
        asyncio.get_event_loop().run_until_complete(self.connect(uri))


        #asyncio.get_event_loop().run_until_complete(connect(uri, self.TOKEN))
        #asyncio.get_event_loop().run_forever()



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

            #default_storage.save(path_file, ContentFile())

    def generateYamlFiles(self, element, uid):
        url = self.DOMAIN+"/api/backend/generate-yaml-cli/"+uid+"/"
        r = requests.get(url)
        data = r.json()
        documents = data["documents"]
        self.variables = data["variables"]
        project_slug = data["project_slug"]
        env_slug = data["env_slug"]
        #self.createFiles(documents, project_slug, env_slug, "document")
        self.runCommandsYaml(uid, "output-terminal")

    def runCommandsYaml(self, uid, action):
        command_list = ["Start Running the Environnement ..."]
        self.sendOutput(command_list, uid, action, [])

        command_ls = ["ls"]
        result_command = command_line.run(command_ls[0])
        output = result_command["output"]
        output_errors = result_command["errors"]

        return self.sendOutput(output, uid, action, output_errors)


    def sendOutput(self, output, uid, action, errors, workdir=""):
        #uri = self.DOMAIN_WS + ":" + str(PORT) + "/connection-cli/"
        data = {
            "action": action,
            "uid": uid,
            "output": output,
            "input": "",
            "output_errors" : errors,
            "workdir" : workdir
        }
        data = json.dumps(data)
        return data
        #self.sendData(data)
        #asyncio.get_event_loop().run_until_complete(self.sendData(data))
        #asyncio.get_event_loop().run_until_complete(sendData(uri, data))

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


def convertData(recev_data) :
    print("------")
    now = datetime.now()
    uid = recev_data["uid"]
    action = recev_data["action"]
    click.echo(recev_data)
    kido_cli = KidoCLI()
    if action == "run-env":
        kido_cli.generateYamlFiles("environnement", uid)
    if action == "input-terminal":
        kido_cli.runCommandTerminal(recev_data)
        click.echo(datetime.now() - now)
        click.echo("+++++++++++++++++++++++++")





