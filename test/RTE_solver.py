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
        
        #self._unassigned_interventions = list()
        #self._S = list()
        
        self._T = 0
        self._senariosNumber = []
        self._quantile = 0
        self._alpha = 0
        
        self._list_tmax = {}
        
    def loadjson(self, fpath: str):
        js = dict()
        with open(fpath, 'r') as f:
            js = json.load(f)
        
        self._resources = js["Resources"]
        self._NRESOURCES = len(self._resources)
        self._list_resources = list(self._resources.keys())
        self._seasons = js["Seasons"]
        self._interventions = js["Interventions"]
        
        #self._unassigned_interventions = self._interventions
        
        self._NINTERVENTIONS = len(self._interventions)
        self._list_interventions = list(self._interventions.keys())
        self._exclusions = js["Exclusions"]
        
        self._T = js["T"]
        self._senarios_number = js["Scenarios_number"]
        self._quantile = js["Quantile"]
        self._alpha = js["Alpha"]
    
    
    def getListTmax(self):
        """
        Fill the list_tmax[]
        
        """
        self._list_tmax = {}
        
        for intv in self._list_interventions:
            self._list_tmax[intv] = self._interventions[intv]["tmax"]
    
            
    def treeSearchTmax(self):
        """
        Find the solution according to Tmax
        """
        
        #TODO Test
        
        S = {}
        S2 = self._list_interventions
        
        self.getListTmax()
        dof = self._list_tmax
        
        # sort dictionary (degree of freedom)
        dof = {k: v for k, v in sorted(dof.items(), key=lambda item: item[1])}
        
        S = {}
        #for intv in self._list_interventions:
        #    tree[intv] = 1
        
        nodes = list(dof.keys())
        idx = 0
        n_begin = 1
        
        while(True):
            # get the intervention name for the current node
            intv = nodes[idx]
            # reset validity to default (false)
            isValidNode = False
            
            print("Looping for {} within range [{}, {}]".format(intv, n_begin, dof[intv]))
            for t_st in range(n_begin, int(dof[intv])+1):
                S[intv] = t_st
                
                # check validity
                if ( self.checkTmax(S) \
                    and self.checkExclusion(S) \
                    and self.checkResource(S) ):
                    print("Temporary solution found at t_st = {}".format(t_st))
                    # if ok, move to the next node
                    idx = idx + 1
                    # and reset the n_begin for the next node
                    n_begin = 1
                    # and set the validity flag
                    isValidNode = True
                    break
                else:
                    # if not valid, delete this item
                    S.pop(intv)
            
            if not isValidNode:
                # if the whole node is not valid, go back to parent node
                print("No valid solution found for this branch...\nGoing back.")
                idx = idx - 1
                n_begin = n_begin + 1
            
            if idx >= len(dof):
                break
                
        return S
                
                
        
    def checkTmax(self, S):
        # Criteria 1: t_st before tmax
        
        ##for i in self._list_interventions:
        for i in S.keys():
            if S[i] > int(self._interventions[i]["tmax"]):
                #print('no') # debugmsg
                return False
        return True
        
    def checkExclusion(self, S):
        # Criteria 2: exclusion
        if len(self._exclusions) == 0:
        # if no exclusion is listed
            pass
        else:
            for key in self._exclusions.keys():
                # current exclusion
                exc = self._exclusions[key]
                    
                # intervention's index in _list_interventions
                intv1 = exc[0]
                intv2 = exc[1]
                season = exc[2]
                
                # for the local checker
                if not (intv1 in S and intv2 in S):
                    break 
                    
                # search the start time for interventions
                t1_st = S[intv1]
                t2_st = S[intv2]
                
                # two interventions in the same season and same time
                if ( (t1_st in self._seasons[season] \
                    or str(t1_st) in self._seasons[season] ) \
                    and ( t2_st in self._seasons[season] \
                    or str(t2_st) in self._seasons[season] ) \
                    and t1_st == t2_st ):
                    # TODO Verify if the exclusion is on season or time_st
                    #print('No') # debugmsg
                    return False
        return True
        
    def checkResource(self, S):
        # Criteria 3 : resources within range
        for c in self._list_resources:
        # for each resources, traverse each time period
        
            for t in range(self._T):
                # max consumption of c on time t
                max_t = self._resources[c]['max'][t]
                # min consumption of c on time t
                min_t = self._resources[c]['min'][t]
                
                # resource consumption
                res = 0
                
                ##for intv in self._list_interventions:
                for intv in S.keys():
                    if t + 1 == S[intv]: 
                        
                        try:
                            # First try to find the resource consumption according to c
                            # if this intervention does not require resource c, then pass
                            wl = self._interventions[intv]["workload"][c]
                            
                            # Then try to find the consumption according to t_st
                            # if this intervention did not list the complete t_st, then pass
                            # I struggle with the name, but it refers to
                            # the part like this {'1': 31, '2': 21, '3': 14, ....}
                            vector123 = wl[str(t+1)] 
                            # t+1 since t start from 0 here
                            vector123 = dict(sorted(vector123.items()))
                            # make the vector in order (in case it's not)
                            
                            # add up resource consumption for each intervention
                            res += int(vector123[str(t+1)])
                        except:
                            pass
                            
                if res < min_t or res > max_t:
                    #print('Noo') # debugmsg
                    return False
        return True

