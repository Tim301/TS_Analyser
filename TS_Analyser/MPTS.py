import os
import TS_Module as tools

class MPTS:
    def __init__(self,pathfile):
        self.path = pathfile
        self.name = os.path.basename(self.path)
        self.json = tools.getInfo(self.path)
        self.nb_channels = len(self.json['programs'])
        self.tsid = tools.ts_id(self.json,self.nb_channels)
        self.map = tools.mapinfo(self.json)