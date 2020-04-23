
import subprocess
import json
class KubernetesUtils:


    def trim(self, str):
        str = str.lstrip()
        str = str.rstrip()
        str = str.strip()
        return str

    def processusLine(self, line):
        split_space = line.split(" ")
        words = []
        next_word = ""
        for index, wrd in enumerate(split_space):
            if index < len(split_space)-1:
                next_word = split_space[index+1]
            if not wrd == "" and not wrd == " " and not next_word == "":
                words.append(wrd)

        return words



    def getEvents(self):
        command = "kubectl get events -o json"
        processus = subprocess.run([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = processus.stdout
        output = json.loads(output)
        result = {}
        for item in output["items"]:
            involved_object = item["involvedObject"]
            message = item["message"]
            reason = item["reason"]
            type = item["type"]
            if involved_object["kind"] == "Ingress" or involved_object["kind"] == "Pod" or involved_object["kind"] == "Deployment" :
                if reason == "FailedScheduling" or reason == "CREATE" or reason == "Failed":
                    result[involved_object["name"]] = { "reason" : reason, "message" : message, type : type, "kind" : involved_object["kind"] }

        print(result)



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
        if kind == "events":
            command = "kubectl get events"

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
        print(line)
        print(headers)
        print("------------------------------")
        object = {}
        for index, item in enumerate(line):
            object[headers[index]] = item

        return object