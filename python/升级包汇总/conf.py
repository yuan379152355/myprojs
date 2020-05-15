import sys
import os
import json
from checkpath import *

class JsonConf(object):
    def __init__(self, file='conf.json'):
        self.file = file
        if not CheckifExists(self.file):
            raise Exception("no conf file: ", file)

    def LoadJson(self):
        f = open(self.file, 'r', encoding = 'utf-8')
        self.dict = json.loads(f.read())
        f.close()