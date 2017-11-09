import heapq


keywordFiles = []
for i in range(1,217):
        #fileName1 = "/scratch2/navudai/bostonfiles/file"+`i`+".txt"
        #tweetFiles.append(fileName1)
        fileName2 = "/scratch2/navudai/boston/dynamicDegree/deg"+`i`+".txt"
        keywordFiles.append(fileName2)

filewrite = open('/scratch2/navudai/boston/results/boston_dynamicDeg.txt','w') 
for i in range(0,len(keywordFiles)):
	filewrite.write(str(i+1))
	filewrite.write("\n")
	U = dict()
        keywordRead = open(keywordFiles[i], 'r')
        for line in keywordRead:
                line = line.strip()
                keyword, temp, weight  = line.partition(' ')
                U[keyword] = float(weight)
	numberOfElements = 20;
	keywordList = heapq.nlargest(numberOfElements, U, key = U.get)
	for j in range(0, len(keywordList)):
		filewrite.write(keywordList[j])
		filewrite.write(" ")
		filewrite.write(str(U[keywordList[j]]))
		filewrite.write("\n")
	print i
