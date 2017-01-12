
import json
from src.Groundplan import Groundplan
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from districtobjects.Playground import Playground

class ConfigLogger(object):

    def __init__(self):
        pass

    def serialize_plan(self,plan):
        print plan
        config = {'num_houses':plan.numberOfHouses(),'playground':plan.PLAYGROUND,'residences':[],'waterbodies':[],'playgrounds':[]}
        for i in plan.getResidences():
            config['residences'].append({'x':i.x,'y':i.y,'type':i.getType()})
        for i in plan.getWaterbodies():
            config['waterbodies'].append({'x':i.x,'y':i.y,'w':i.getWidth(),'h':i.getHeight()})
        for i in plan.getPlaygrounds():
            config['playgrounds'].append({'x':i.x,'y':i.y})
        return config

    def deserialize_plan(self,d):
        plan = Groundplan(d['num_houses'],d['playground'])
        for i in d['residences']:
            h = None
            print i['type'] == "FamilyHome"
            if i['type'] == "Bungalow": h = Bungalow(i['x'],i['y'])
            elif i['type'] == "Mansion": h = Mansion(i['x'],i['y'])
            elif i['type'] == "FamilyHome": h = FamilyHome(i['x'],i['y'])
            print h
            plan.addResidence(h)
        for i in d['waterbodies']:
            plan.addWaterbody(Waterbody(i['x'],i['y'],i['w'],i['h']))
        for i in d['playgrounds']:
            plan.addPlayground(Playground(i['x'],i['y']))
        print plan.getWidth()
        return plan

    @classmethod
    def appendToConfigLog(self, key, plan):
        with open(key) as f:
            data = json.load(f)
        data['d'].append(ConfigLogger().serialize_plan(plan))
        with open(key, 'w') as f:
            json.dump(data, f)

    @classmethod
    def loadConfig(self, key):
        with open(key, 'r') as data:
            d = json.load(data)
            print data
            d = d['d']
            return ConfigLogger().deserialize_plan(d[len(d) - 1])
            #return [len(d) - 1, ConfigLogger().deserialize_plan(d[len(d) - 1])]

    @classmethod
    def createConfigLog(cls, key):
        with open(key, 'w') as data:
            json.dump({'d':[]}, data)