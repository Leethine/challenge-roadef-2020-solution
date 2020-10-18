from RTE_solver import RTE_solver

sample = RTE_solver()
sample.loadjson("../samples/example2.json")

S = sample.treeSearchTmax()

print(S)

if sample.checkResource(S):
    print("Resources good")
else:
    print("Bad resources found")

if sample.checkExclusion(S):
    print("Exclusions valid")
else:
    print("Bad exclusions found")

#for i in range(29):
#    print(sample.genPermulation(i))

#print("Total {} possible permulations".format(sample._T ** sample._NINTERVENTIONS))

#print(sample.getmaxcomb())

#for idx in range(sample.getmaxcomb()):
    #solution = sample.greedySearch(idx)
    #if sample.checkValidity2(solution):
    #print("{} is generated".format(solution))
    
