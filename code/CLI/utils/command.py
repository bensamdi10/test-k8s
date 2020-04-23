import os
import subprocess
import click


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class CommandLine:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def run(self, command, workdir=""):
        #output = subprocess.run([command])
        #processus = subprocess.Popen([command], stdout=subprocess.PIPE, universal_newlines=True)
        cd_output = ""
        if command.find("cd ") > -1 :
            new_dir = os.path.join(self.BASE_DIR, command.split("cd ")[1])
            with cd(new_dir):
                processus = subprocess.run("ls", check=True,shell=True,  stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
                cd_output = command.split("cd ")[1]
        else:
            new_dir = os.path.join(self.BASE_DIR, workdir)
            with cd(new_dir):
                processus = subprocess.run([command], check=True,shell=True,  stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)

        output = processus.stdout
        errors = processus.stderr
        click.echo(errors)
        #print("The exit code was: %d" % list_files.returncode)

        return { "output" :  output, "output_strip" : processus.stdout.strip(), "errors" : errors, "code" : processus.returncode, "cd_output" : cd_output }

    def runM(self, command):
        #output = subprocess.run([command])
        #processus = subprocess.Popen([command], stdout=subprocess.PIPE, universal_newlines=True)

        processus = subprocess.run(command, check=True,shell=True,  stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)

        output = processus.stdout
        errors = processus.stderr


        click.echo(processus.stdout.strip())

        #print("The exit code was: %d" % list_files.returncode)

        return { "output" :  output, "output_strip" : processus.stdout.strip(), "errors" : errors }
    def runIn(self, command):
        os.system(command)

    def getOutput(self):
        print("output")

    def setCommand(self, command):
        print(command)