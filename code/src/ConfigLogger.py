import json
from src.Groundplan import Groundplan
from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion
from districtobjects.Waterbody import Waterbody
from districtobjects.Playground import Playground
import os


class ConfigLogger(object):
    FOLDER = "plans/"

    def __init__(self):
        pass

    def exists(self, key):
        return os.path.isfile(self.FOLDER + key)

    @staticmethod
    def serialize_plan(plan, metad):

        def minify(t):
            if t == "FamilyHome":
                return 'f'
            elif t == "Bungalow":
                return 'b'
            elif t == "Mansion":
                return 'm'

        config = [plan.NUMBER_OF_HOUSES, plan.PLAYGROUND, [], [], [], metad['deaths'], metad['mutations']]
        for i in plan.getResidences():  config[2].append([i.x, i.y, minify(i.getType()), i.flipped])
        for i in plan.getWaterbodies(): config[3].append([i.x, i.y, i.getWidth(), i.getHeight(), i.flipped])
        for i in plan.getPlaygrounds(): config[4].append([i.x, i.y, i.flipped])
        return config

    @staticmethod
    def deserialize_plan(d):
        plan = Groundplan(d[0], d[1])
        for i in d[2]:
            h = None
            if i[2] == "b":
                h = Bungalow(i[0], i[1])
            elif i[2] == "m":
                h = Mansion(i[0], i[1])
            elif i[2] == "f":
                h = FamilyHome(i[0], i[1])
            if i[3]: h = h.flip()
            plan.addResidence(h)
        for i in d[3]:
            wb = Waterbody(i[0], i[1], i[2], i[3])
            if i[4]: wb = wb.flip()
            plan.addWaterbody(wb)
        for i in d[4]:
            pg = Playground(i[0], i[1])
            if i[2]: pg = pg.flip()
            plan.addPlayground(pg)

        return plan

    @classmethod
    def appendToConfigLog(cls, key, plan, metad):
        with open(cls.FOLDER + key) as f: data = json.load(f)
        data['d'].append(ConfigLogger().serialize_plan(plan, metad))
        with open(cls.FOLDER + key, 'w') as f: json.dump(data, f)

    @classmethod
    def loadConfig(cls, key):
        with open(cls.FOLDER + key, 'r') as data:
            d = json.load(data)
            d = d['d']
            return ConfigLogger().deserialize_plan(d[len(d) - 1])

    @classmethod
    def createConfigLog(cls, key):
        with open(cls.FOLDER + key, 'w') as data: json.dump({'d': []}, data)
