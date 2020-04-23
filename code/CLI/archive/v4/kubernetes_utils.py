import time
from kubernetes import client, config
import subprocess

class KubernetesUtils:

    def __init__(self):
        config.load_kube_config()

    def trim(self, str):
        str = str.lstrip()
        str = str.rstrip()
        str = str.strip()
        return str

    def processusLine(self, line):
        split_space = line.split(" ")
        words = []
        for wrd in split_space:
            if not wrd == "" and not wrd == " ":
                words.append(wrd)

        return words




    def getKindObject(self, kind):
        command = ""
        if kind == "deployment":
            command = "kubectl get deployment"
        if kind == "pvc":
            command = "kubectl get pvc"
        if kind == "job":
            command = "kubectl get jobs"
        if kind == "pod":
            command = "kubectl get pods"
        if kind == "ingress":
            command = "kubectl get ingress"
        if kind == "secret":
            command = "kubectl get secret"

        processus = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        object_result = {"header": [], "rows": []}
        for index, line in enumerate(processus.stdout):
            line = line.decode("utf-8")
            line = str(line)
            line = line.replace("\n", "")
            line_new = self.processusLine(line)
            if index == 0:
                object_result["header"] = line_new
            else:
                object_line = self.createLineObject(line_new, object_result["header"])
                object_result["rows"].append(object_line)

        print(object_result["rows"])



    def createLineObject(self, line, headers):
        object = {}
        for index, item in enumerate(line):
            object[headers[index]] = item

        return object



    def getDeployments(self):
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        print(dir(v1))
        ret = v1.list_deployment_for_all_namespaces(watch=False)
        deployments = ret.items

        return deployments

    def getPods(self):
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        pods_containers = []
        index = 0
        for i in ret.items:
            dict_pod = i.to_dict()
            conditions = dict_pod["status"]["conditions"]
            l_cond = len(conditions)
            object_pod = {
                "index": index,
                "name": dict_pod["name"],
                "status_message": conditions[l_cond - 1]["message"],
                "reason": conditions[l_cond - 1]["reason"],
                "phase": dict_pod["status"]["phase"],
                "ip": i.status.pod_ip,
                "name_space": i.metadata.namespace,
                "name_pod": i.metadata.name
            }
            pods_containers.append(object_pod)
            index +=1

        return pods_containers
        '''
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        '''