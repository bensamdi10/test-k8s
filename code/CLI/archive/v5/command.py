import os
import subprocess
import click
import sys
import asyncio

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

    def run(self, command, workdir="", callback=None):
        click.echo(callback)
        cd_output = ""
        if command.find("cd ") > -1 :
            new_dir = os.path.join(self.BASE_DIR, command.split("cd ")[1])
            with cd(new_dir):
                processus = subprocess.run("ls", check=True,shell=True,  stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
                cd_output = command.split("cd ")[1]
        else:
            new_dir = os.path.join(self.BASE_DIR, workdir)
            with cd(new_dir):
                processus = subprocess.Popen([command], shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if not callback == None:
                    for line in processus.stdout:
                        asyncio.run(callback(line))


        output = processus.stdout
        errors = processus.stderr
        return { "output" :  output, "errors" : errors, "code" : processus.returncode, "cd_output" : cd_output }

    def runM(self, command):
        processus = subprocess.run(command, check=True,shell=True,  stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
        output = processus.stdout
        errors = processus.stderr
        return { "output" :  output, "output_strip" : processus.stdout.strip(), "errors" : errors }

    def runIn(self, command):
        result = os.system(command)
        click.echo(dir(result))
        click.echo(result.from_bytes())
        click.echo("----------")