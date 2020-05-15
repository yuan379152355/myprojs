import sys
import os
import json
from checkpath import *

class OrderDirs(object):
    def __init__(self, file='order.txt'):
        self.file = file
        if not CheckifExists(self.file):
            raise Exception("no orderfile: ", file)

    def LoadOrder(self):
        f = open(self.file, 'r', encoding = 'utf-8')
        self.filelist = []

        while 1:
            line = f.readline()
            if not line:
                break
            line=line.strip('\n')
            self.filelist.append(line)

        f.close()