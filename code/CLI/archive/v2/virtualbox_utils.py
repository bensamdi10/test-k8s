import os
from utils.command import CommandLine
from threading import Timer

command_line = CommandLine()

class VirtualBoxUtils:


    def runContainer(self, data, path, path_file):
        commands = []
        source = data['extra_data']['source']
        name = data['extra_data']['name']
        if len(name.split("/")) > 1 :
            name_container = name+"_container"
        else:
            name.split("/")[1] + "_container"
        uid = data['extra_data']['uid']
        commands.append("git clone "+source +" "+path)

        commands.append("docker build -t "+name+" -f "+path_file+"/Dockerfile_"+uid+".file "+path_file)
        #commands.append("docker run -it "+name)

        return commands

    def installVbox(self):

        commands = []
        commands.append("apt update")
        commands.append("apt upgrade")
        commands.append("wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add -")
        commands.append("wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -")
        commands.append('add-apt-repository "deb http://download.virtualbox.org/virtualbox/debian bionic contrib"')
        commands.append('apt install virtualbox-6.0')
        return commands


    def installKubectl(self):
        commands = []
        commands.append("curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl")
        commands.append('chmod +x ./kubectl')
        commands.append('mv ./kubectl /usr/local/bin/kubectl')
        commands.append('kubectl version --client')
        return commands

    def installMinikube(self):
        commands = []
        commands.append('curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
          && chmod +x minikube')
        commands.append("mkdir -p /usr/local/bin/")
        commands.append("install minikube /usr/local/bin/")
        commands.append("apt-get install conntrack")
        return commands


    def installDocker(self):
        commands = []
        commands.append('apt-get install  curl apt-transport-https ca-certificates software-properties-common -y')
        commands.append("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
        commands.append('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
        commands.append("apt update -y")
        commands.append("apt install docker-ce -y")
        return commands

    def startMinikube(self):
        commands = []
        commands.append("minikube addons enable ingress")
        commands.append("minikube start --driver=none")
        return commands




