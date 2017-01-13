
import json
from src.Groundplan import Groundplan
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from districtobjects.Playground import Playground

class ConfigLogger(object):

    FOLDER = "plans/"

    def __init__(self):
        pass

    def exists(self,key):
        try:
            with open(self.FOLDER+key, 'r') as data:return True
        except Exception:return False

    def serialize_plan(self,plan,metad):

        def minify(t):
            if t == "FamilyHome": return 'f'
            elif t == "Bungalow": return 'b'
            elif t == "Mansion": return 'm'

        config = [plan.numberOfHouses(),plan.PLAYGROUND,[],[],[],metad['deaths'],metad['mutations']]
        for i in plan.getResidences():  config[2].append([i.x,i.y,minify(i.getType())])
        for i in plan.getWaterbodies(): config[3].append([i.x,i.y,i.getWidth(),i.getHeight()])
        for i in plan.getPlaygrounds(): config[4].append([i.x,i.y])
        return config

    def deserialize_plan(self,d):
        plan = Groundplan(d[0],d[1])
        for i in d[2]:
            h = None
            if i[2] == "b": h = Bungalow(i[0],i[1])
            elif i[2] == "m": h = Mansion(i[0],i[1])
            elif i[2] == "f": h = FamilyHome(i[0],i[1])
            plan.addResidence(h)
        for i in d[3]:plan.addWaterbody(Waterbody(i[0],i[1],i[2],i[3]))
        for i in d[4]:plan.addPlayground(Playground(i[0],i[1]))

        return plan

    @classmethod
    def appendToConfigLog(self, key, plan, metad):
        with open(self.FOLDER+key) as f: data = json.load(f)
        data['d'].append(ConfigLogger().serialize_plan(plan,metad))
        with open(self.FOLDER+key, 'w') as f:json.dump(data, f)

    @classmethod
    def loadConfig(self, key):
        with open(self.FOLDER+key, 'r') as data:
            d = json.load(data)
            d = d['d']
            return ConfigLogger().deserialize_plan(d[len(d) - 1])

    @classmethod
    def createConfigLog(self, key):
        with open(self.FOLDER+key, 'w') as data:json.dump({'d':[]}, data)