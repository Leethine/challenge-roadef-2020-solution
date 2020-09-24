import json

class RTE_solver:

    def __init__(self):
        self._resources = dict()
        self._seasons = dict()
        self._interventions = dict()
        self._exclusions = dict()
        
        self._NRESOURCES = 0
        self._NINTERVENTIONS = 0
        self._list_resources = list()
        self._list_interventions = list()
        
        self._T = 0
        self._senariosNumber = []
        self._quantile = 0
        self._alpha = 0
        
    def loadjson(self, fpath):
        js = dict()
        with open(fpath, 'r') as f:
            js = json.load(f)
        
        self._resources = js["Resources"]
        self._NRESOURCES = len(self._resources)
        self._list_resources = list(self._resources.keys())
        self._seasons = js["Seasons"]
        self._interventions = js["Interventions"]
        self._NINTERVENTIONS = len(self._interventions)
        self._list_interventions = list(self._interventions.keys())
        self._exclusions = js["Exclusions"]
        
        self._T = js["T"]
        self._senariosNumber = js["Scenarios_number"]
        self._quantile = js["Quantile"]
        self._alpha = js["Alpha"]
        
    def genPermulation(self, n: int):
        pass
    
    def checkValidity(self, n : int):
        pass
        
