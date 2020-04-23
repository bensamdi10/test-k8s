import os
from utils.command import CommandLine
from threading import Timer

command_line = CommandLine()

class VirtualBoxUtils:


    def install(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        vbox_api_dir = os.path.join(BASE_DIR, 'vbox')
        vbox_api_dir = os.path.join(vbox_api_dir, 'installer')
        timer = Timer(0.2, self.runIstall, args=[vbox_api_dir])
        timer.start()


    def runIstall(self, path_install):
        #command_line.runIn("cd " + path_install+" && python vboxapisetup.py install")
        self.init()

