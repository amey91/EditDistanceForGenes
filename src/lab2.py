import networkx as nx, math, sys
'''
Created on Mar 18, 2014

@author: Amey
'''
from operator import indexOf, index

mainList = [] # maintains leist of genes
probabilities = [] # maintains optimal probabilities
solutions = [] # maintains path

       
# false means no overlap 
# true means overlap detected
def overlaps(gene, geneList):
    if len(geneList) == 0:
        return False
    '''
    for index,item in enumerate(geneList):
        if gene[0] > geneList[index][0] and gene[0] < geneList[index][1]:
            return True
        if gene[1] > geneList[index][0] and gene[1] < geneList[index][1]:
            return True
        if gene[0] < geneList[index][0] and gene[1] > geneList[index][1]:
            return True
    '''
    for index, item in enumerate(geneList):
        #if start overlaps
        if gene[0] >= mainList[index][0] and gene[0] <= mainList[index][1]:
                return True
        #if end overlaps
        if gene[1] >= mainList[index][0] and gene[1] <= mainList[index][1]:
                return True
        #if it encapsulates
        if gene[0] <= mainList[index][0] and gene[1] >= mainList[index][1]:
                return True
        
        #if mainList item begin overlaps
        if mainList[index][0] >= gene[0] and mainList[index][0] <= gene[1]:
                return True
        #if mainList item  end overlaps
        if mainList[index][1] >= gene[0] and mainList[index][1] <=  gene[1]:
                return True
        #if mainList item encapsulates
        if mainList[index][0] <= gene[0] and mainList[index][1] >= gene[1]:
                return True
    return False

def overlap_trivial(gene1, gene2):
    '''
    for index,item in enumerate(geneList):
        if gene[0] > geneList[index][0] and gene[0] < geneList[index][1]:
            return True
        if gene[1] > geneList[index][0] and gene[1] < geneList[index][1]:
            return True
        if gene[0] < geneList[index][0] and gene[1] > geneList[index][1]:
            return True
    '''
    if gene1[0] == gene2[0] or gene1[0] == gene2[1]:
        return True
    if gene1[1] == gene2[0] or gene1[1] == gene2[1]:
        return True
    #if start overlaps
    if gene1[0] >= gene2[0] and gene1[0] <= gene2[1]:
            return True
    #if end overlaps
    if gene1[1] >= gene2[0] and gene1[1] <= gene2[1]:
            return True
    #if it encapsulates
    if gene1[0] <= gene2[0] and gene1[1] >= gene2[1]:
            return True
        
    #if start overlaps
    if gene2[0] >= gene1[0] and gene2[0] <= gene1[1]:
            return True
    #if end overlaps
    if gene2[1] >= gene1[0] and gene2[1] <= gene1[1]:
            return True
    #if it encapsulates
    if gene2[0] <= gene1[0] and gene2[1] >= gene1[1]:
            return True
    return False



def bubbleSort(unsortedList):
    length = len(unsortedList) - 1
    isSorted = False

    while not isSorted:
        isSorted = True
        for i in range(length):
            if unsortedList[i] > unsortedList[i+1]:
                isSorted = False
                #flip maiList
                temp = unsortedList[i]
                unsortedList[i] = unsortedList[i+1] 
                unsortedList[i+1] = temp
                #flip flip list
                temp = flip[i]
                flip[i] = flip[i+1] 
                flip[i+1] = temp

def printResult():
    maxProbIndex = 0
    #print "mainList ->  ", mainList
    for index,item in enumerate(mainList):
        #get max probability from entire list
        if probabilities[index]>probabilities[maxProbIndex]:
            maxProbIndex = index   
        if flip[index] == 1:
            pass
            #if the start and ends have been flipped, then restore original configuration
            
            flip[index] = 0
            temp = mainList[index][0]
            mainList[index][0] = mainList[index][1]
            mainList[index][1] = temp
    
            
    print "Sum Probability: ", probabilities[maxProbIndex]
    for i,val in enumerate(solutions[maxProbIndex]):
        print "Include:"," ".join(str(e) for e in mainList[val])


#main()
if __name__ == '__main__':
    # filename= sys.argv[1]
    input = []
    inputFile = sys.argv[1]
    [input.append(line.strip()) for line in open(inputFile)]

    # flip start and end if start> end 
    flip = []
    for index, x in enumerate(input):
        # first split into 3 parts
        mainList.append( x.split() )
        mainList[index][0] = int(mainList[index][0])
        mainList[index][1] = int(mainList[index][1])
        mainList[index][2] = float(mainList[index][2])
        solutions.append([])
        probabilities.append(00.00)
        if int(mainList[index][0]) > int(mainList[index][1]):
            flip.append(1)
            temp = mainList[index][0]
            mainList[index][0] = mainList[index][1]
            mainList[index][1] = temp
        else:
            flip.append(0)
            
    #sort list 
    
    bubbleSort(mainList) #mainList should not change after this
    
    for index,item in enumerate(mainList):
        if index == 0:
            #base case of 1 element
            solutions[index].append(index)
            probabilities[index] = mainList[index][2]
        else:
            temp = index-1
            while temp>=0:
                # check whether the current index and the previous index overlap
                # if they do not overlap
                
                #if (not overlaps(mainList[index],solutions[temp])) and (not overlap_trivial(mainList[index],mainList[temp])):
                if (not overlap_trivial(mainList[index],mainList[temp])):
                    #if they do not overlap and sum of probabilities is greater, then include current element in the list
                    if probabilities[index]<(mainList[index][2]+probabilities[temp]): 
                        probabilities[index] = probabilities[temp] + mainList[index][2]    
                        #erase previous solution
                        solutions[index]=[]
                        #add previous optimal solutions in current solution
                        for k in solutions[temp]:
                            solutions[index].append(k)
                            
                        #also include yourself in the solution 
                        solutions[index].append(index)
                #if they overlap
                else:
                    #if last element, then everything overlaps with current index
                    if temp==0:
                        solutions[index].append(index)
                        probabilities[index] = mainList[index][2]
                        #print "okay", temp, index
                        break;
                    #if they overlap, assign max value of current and prev
                    if(probabilities[temp] > probabilities[index]):
                        probabilities[index] = probabilities[temp]
                        solutions[index]=solutions[temp]
                temp = temp-1
                    
    
    printResult()
 
 
    
''' SAMPLE OUTPUT:
Sum Probability: 1.48412714911
Include: 74 98 0.500890065124
Include: 67 14 0.983237083985
'''