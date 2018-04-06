a = {'q':1,'w':2}
p = {}
p[a] = 3




for i in range(numSamples):
            weight = 1
            for v in bayesNet.linearizeVariables():
                f = bayesNet.getCPT(v)
                f = f.specializeVariableDomains(vDD)
                if v in evidenceDict.keys():
                    for ad in f.getAllPossibleAssignmentDicts():
                    weight = weight * f.getProbability(vDD)
                else:
                    sample.update(sampleFromFactor(f, sample))
            newFactor.setProbability(sample, newFactor.getProbability(sample) + weight)
            
            sample = evidenceDict.copy()