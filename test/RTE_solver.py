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
        
    def loadjson(self, fpath: str):
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
        self._senarios_number = js["Scenarios_number"]
        self._quantile = js["Quantile"]
        self._alpha = js["Alpha"]
    
    def _decimal2t(self, n: int, t: int):
        """
        Convert decimal number to t-system
        for generating permutations  
        """
        l = []
        while n != 0:
            l.append(int( n % t) )
            n = int(n / t)
        return l
            
    def genPermutation(self, n: int):
        """
        Generate permutation according to n, an integer.
        Permutations are generated according to a specific order.
        The format of permutation is:
        index: [intv1, intv2, .... , intv_n] 
        value: [t_st1, t_st2, .... , t_stn ]
        """
        # number of permutations
        npermutation = self._T ** self._NINTERVENTIONS
        if n >= npermutation:
            raise ValueError("n = {} exceeds the total number of permutations!".format(n))
        
        perm = []
        l = self._decimal2t(n, self._T)
        # append zero for short numbers, i.e. 11 => 011
        if len(l) < self._NINTERVENTIONS:
            for i in range(self._NINTERVENTIONS - len(l)):
                l.append(0)
        #print(l)
        #print("total number of perm: {}".format(npermutation))
        
        # python counts from zero, but we count from 1
        for i in l:
            perm.append(i+1)

        return perm
    
    def checkValidity(self, n: int):
        """
        Ckeck validity of a certain permutation.
        According to three criterias.
        Given the serial number of permulation.
        """
    
        perm = self.genPermutation(n)
        # Criteria 1: t_st before tmax
        #print(perm) #debug
        for i in range(self._NINTERVENTIONS):
            if perm[i] > int(self._interventions[self._list_interventions[i]]["tmax"]):
                #print('no') # debugmsg
                return False
        
        # Criteria 2: exclution
        if len(self._exclusions) == 0:
        # if no exclusion is listed
            pass
        else:
            for key in self._exclusions.keys():
                # current exclusion
                exc = self._exclusions[key]
                
                # intervention's index in _list_interventions
                intv1 = self._list_interventions.index(exc[0])
                intv2 = self._list_interventions.index(exc[1])
                
                # search the start time for interventions
                t1_st = perm[intv1]
                t2_st = perm[intv2]
                season = exc[2]
                # two interventions in the same season and same time
                if ( t1_st in self._seasons[season] \
                    or str(t1_st) in self._seasons[season] ) \
                    and ( t2_st in self._seasons[season] \
                    or str(t2_st) in self._seasons[season] ) \
                    and t1_st == t2_st:
                    # TODO Verify if the exclusion is on season or time_st
                    #print('No') # debugmsg
                    return False
        
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
                
                for i in range(self._NINTERVENTIONS):
                    interv = self._list_interventions[i]
                    if t + 1 == perm[i]: 
                        
                        try:
                            # First try to find the resource consumption according to c
                            # if this intervention does not require resource c, then pass
                            wl = self._interventions[interv]["workload"][c]
                            
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
