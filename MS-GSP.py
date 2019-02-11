import sys, re
import itertools
from collections import OrderedDict
from collections import Counter
from algo_def import contains, generate_F, makeDistinct
from MScandidate_gen_SPM import CandGen, gspTypejoin, confirmOrder, filterSeq, \
    lengthSeq, sizeSeq, checkFirstItemIsLesser, checkLastItemIsLesser, \
    prune, checkmintem, get_positions, level2candgen
from fileRead import readit


def MSGSP():

    #***********************************Declaration of variables**********************************
    MIS = {}  # stores MIS values of all the items
    count = {}  # Stores count of all the items
    L = []  # Seed to generate C[2] and F[1]
    k = 1  # main counter variable
    candidateList = []
    M = []  # Stores all the items in ascending order of their MIS
    F = {}  # dictionary to store frequent Itemsets of all lengths


    #********************************Extract input data from fileRead ******************************
    extract = readit()
    data_seq = extract[0]
    countItems = extract[1]
    N = extract[2]
    MIS = extract[3]
    sdc = extract[4]

    # ***********************************Sorting MIS*******************************
    [M.append(i) for i in sorted(MIS, key=MIS.get, reverse=False)] #sorting   
    [M.remove(item) for item in M if str(item) not in countItems]  #remove invalid entires

    # ENDS HERE

    # ************************************Init_PASS**********************************
    iCounter = 0
    L.append(M[0])
    nextItems = [item  for item in M[iCounter + 1:] if(float(countItems.get(str(item))) / float(N) >= (MIS.get(M[0])))]
    for item in nextItems:
        L.append(item)
    # ENDS HERE

    # *************************************Generating F-one*******************************
    f1=[item for item in L if ((float(countItems.get(str(item)))) / float(N) >= MIS.get(item))]
    # print "List of F1 itemsets:"
    F[k] = ["{" + str(item) + "}" for item in f1]
    # ENDS HERE

    k = k + 1

    # *************************** Converting L & MIS lists  into String format*********************
    for i in range(0, len(L)):
        L[i] = str(L[i])
    for key, value in MIS.items():
        del MIS[key]
        MIS[str(key)] = value
    # ENDS HERE

    # *************************************Main loop************************************
    while (F[k - 1]):
        # print "Value of K is", k
        if k == 2:
            # Call candidate generation 2
            candidateList = level2candgen(L, MIS, countItems, N, sdc)
            # print "Potential candidate 2 list",candidateList
            candidateList = makeDistinct(candidateList)
            # print "Updated candidate 2 list",candidateList

        else:
            # call candidate-k generation
            candidateList = CandGen(F[k - 1], MIS, k, sdc, N, countItems)

        # ************To check the presence of generated sequence 'C'  in the data sequence 'S'************

        for line in data_seq:
            trans = line[line.find("<") + 1:line.find(">")]
            # trans=trans.replace(" ","")
            for candidateItem in candidateList:

                check = contains(candidateItem, trans)

                # Count the presence of candidate in a transaction and store it in count
                if (check == 1):
                    if candidateItem not in count:
                        count[candidateItem] = 1
                    else:
                        count[candidateItem] = count[candidateItem] + 1
        F[k] = generate_F(candidateList, MIS, count, N)
        k = k + 1
    # ****************************Main Loop Ends Here******************************************************

    # ******************************Printing the generated sequential patterns**********************************
    log = open("output.txt","w+")
    
    i = 1
    while (len(F) != i):

        log.write("\n"+ "Number of "+ str(i) + " length Sequential patterns: "+ str(len(F.get(i))) + "\n")
       
        [log.write("Pattern: <"+ str(item) + ">  Count: "+str(countItems.get(item[item.find("{") + 1:item.find("}")]))  + "\n") for item in F.get(i)] if(i==1) else (
            [log.write("Pattern: <"+ str(item) + ">  Count: "+ str(count.get(item))  + "\n") for item in F.get(i)])
       
        log.write("\n"+ "******************************************************"  + "\n")
        log.write("                      " + "\n")
        i = i + 1

    #log.write("\n"+ "*************COMPLETED********************" + "\n")

    log.close()

    #print("****************Done!************************")

if __name__ == '__main__': MSGSP()
