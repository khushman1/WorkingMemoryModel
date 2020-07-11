def minStrong(array):
    open = 0
    queue = []
    visited = []
    scores = []
    sets = []
    currentCluster = []
    currentScore = 0
    done = False
    while(done==False):
        # print ("open: "+ str(open))
        # print(queue)
        # print(visited)
        # print("---")
        for i in range(0,len(array)): #for each node
            if i!=open and array[open][i]!=0:
                #print ("here")
                currentScore += array[open][i]
                if i not in currentCluster:
                    currentCluster.append(i)
                if i not in visited and i not in queue:
                    queue.append(i)
        visited.append(open)
        if queue!=[]:
            open = queue[0]
            queue.pop(0)
        elif len(visited) == len(array):
                done=True
                scores.append(currentScore)
                sets.append(currentCluster)
        else: #moving to the new cluster
            flag = False
            index = 0
            scores.append(currentScore)
            sets.append(currentCluster)
            currentScore = 0
            currentCluster = []
            while flag == False and index<len(array):
                if index not in visited:
                    open = index
                    flag = True
                index += 1

            if flag == False:
                done = True

    #finding the maximum score
    max = 0
    maxIndex = 0
    for i in range(0,len(scores)):
        if scores[i]>max:
            max = scores[i]
            maxIndex = i
    # print("the score: "+str(max) )

#    min = 100
#    for n in sets[maxIndex]:
#        # print("the set members: "+str(n))
#        if n<min:
#            min = n

    return sets[maxIndex]

#print(minStrong([ [0,3,2,0,0] , [3,0,1,0,0] , [2,1,0,0,0] , [0,0,0,0,1] , [0,0,0,1,0]]))
