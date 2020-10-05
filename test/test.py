from RTE_solver import RTE_solver

sample = RTE_solver()
sample.loadjson("../samples/example2.json")

#for i in range(29):
#    print(sample.genPermulation(i))

#print("Total {} possible permulations".format(sample._T ** sample._NINTERVENTIONS))

idx = 0
while (1):
    try:
        isvalid = sample.checkValidity(idx)
        if isvalid:
            solution = sample.greedySearch(idx)
            print("{} is generated".format(solution))
        idx += 1
    except:
        break
