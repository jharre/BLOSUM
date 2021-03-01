import sys


hashOriginal = {}
hashClusters = {}
hashNewick = {}
codeHash = {}

data = None
codes = []
numOTU = None
distmatrix = []
temp = None

MAXDIST, smallest, smallestI, smallestJ = None, None, None, None
#print("Enter the name of the distance matrix file: \n")
fileinput = input("Enter the name of the distance matrix file: \n")
#fileinput.rstrip('\n')
#try:
infile1 = open(fileinput, "r+")
#except:
#    print("error opening input file 1\n")
#    exit()

with infile1:
    data = infile1.readline()
    numOTU = int(data.strip("\n"))
    data = infile1.readline()
    codes = data.rstrip("\n").split()

    for i in range(numOTU):
        codeHash[codes[i]] = i
        hashNewick[codes[i]] = codes[i]

        hashOriginal[codes[i]] = {codes[i]}

        for line in infile1:
            line = line.rstrip("\n").split()
            distmatrix.append(line)


print("\n    ")
print(codes)
print('\n')
for i in range(numOTU):
    print(codes[i] + ': ')
    hashClusters[codes[i]] = []
    for j in range(numOTU):
        print(distmatrix[i][j])
        hashClusters[codes[i]].append({codes[j]: distmatrix[i][j]})
    print('\n')

MAXDIST = 999999
numClusters = numOTU
while numClusters > 2:
    arrayClusters = hashClusters.keys()
    arrayRvalues = []
    for i in range(numClusters):
        temp = 0
        for j in range(numClusters):
            try:
                temp = temp + int(hashClusters[arrayClusters[i]][i][arrayClusters[j]])
            except KeyError:
                print("")
        arrayRvalues.append(temp / (numClusters - 2))
    print('R values\n')
    for i in range(numClusters):
        print(str(arrayClusters[i]) + " " + str(arrayRvalues[i]) + " ")
    print("\n")

    smallest = MAXDIST
    smallestI = 0
    smallestJ = 0
    print("TD matrix: \n")
    for i in range(numClusters - 1):
        for j in range(1, numClusters):
            try:
                tempTD = int(hashClusters[arrayClusters[i]][j][arrayClusters[j]]) - arrayRvalues[i] - arrayRvalues[j]
                print("TD" + str(arrayClusters[i]) + str(arrayClusters[j]) + "=" + str(tempTD) + "  ")
                if tempTD < smallest:
                    smallest = tempTD
                    smallestI = i
                    smallestJ = j
            except KeyError:
                print("")    

    clusterI = arrayClusters[smallestI]
    clusterJ = arrayClusters[smallestJ]
    merge = str(clusterI) + str(clusterJ)

    try:
        branch1 = (int(hashClusters[clusterJ][smallestI][clusterI]) + arrayRvalues[smallestI] - arrayRvalues[smallestJ]) / 2
        branch2 = (int(hashClusters[clusterJ][smallestI][clusterI]) + arrayRvalues[smallestI] - arrayRvalues[smallestJ]) / 2
        print("Merging Clusters: " + clusterI + " and " + clusterJ + "\n")
        print("Distance between " + clusterI + "and ancestral node = " + str(branch1))
        print("Distance between " + clusterJ + "and ancestral node = " + str(branch2))
    except KeyError:
        print("")
   

    for i in range(numClusters):
        if arrayClusters[i] != clusterI and arrayClusters[i] != clusterJ:
            try:
                d1 = hashClusters[arrayClusters[i]][i][clusterI]
                d2 = hashClusters[arrayClusters[i]][i][clusterJ]
                hashClusters[merge] = {arrayClusters[i]: d1 + d2 - hashClusters[clusterI][clusterJ]}
                hashClusters[arrayClusters[i]].append({merge: hashClusters[merge][arrayClusters[i]]})
            except KeyError:
                print("")

    hashNewick[merge] = "(" + hashNewick[clusterI] + "," + hashNewick[clusterJ] + ")"
    for i in range(numClusters):
        try:
            del hashClusters[clusterI]
            del hashClusters[clusterJ]
        except KeyError:
            print("")
    del hashNewick[clusterI]
    del hashNewick[clusterJ]

    arrayClusters = hashClusters.keys()
    numClusters = numClusters - 2

print("Distance between remaining clusters: ")
print(hashClusters)
print("\n")
print(hashNewick)
try:
    print(str(hashClusters[arrayClusters[0]][0][arrayClusters[1]]) + " " + str(hashClusters[arrayClusters[1]][1][arrayClusters[0]]))

    print("\nNewick format: ")
    for j in range(numClusters):
        print(hashNewick[arrayClusters[j]])
except KeyError:
    print("")