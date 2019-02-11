import sys, re
import itertools
from algo_def import flatten, Counter
from collections import OrderedDict

extract = []

def readit():

    # ****************************Add input file path here*****************************
   
    root="."

    # **************************Read data inputs*************************************

    FileData = root + "\\data.txt"
    with open(FileData) as f:
        data_seq1 = f.readlines()
    cnt = 0
    for line in data_seq1:
        cnt = cnt+1
    N = cnt-1
    dataItem = []
    for line in data_seq1:
        ItemList = re.sub(r'\D', " ", line).strip()
        dataItem.append(ItemList.split())
        
    cleanedSeqence = []
    cleanedSeqence = [list(set(list(item))) for item in dataItem]
    
    allItems = list(flatten(cleanedSeqence))
    countItems = Counter(allItems)
    MIS={}

    #******************************Read parameteres input***********************************

    parametersInFile = root+"\\para.txt"
    with open(parametersInFile) as f:
        parameters = f.readlines()
    for line in parameters:
        if (("MIS" or "mis") in line):
            key = (line[line.find("(") + 1:line.find(")")])
            key = int(key)
            value = float(line[line.find("=") + 1:].strip("\n"))
            MIS[key] = value

        elif(("SDC" or "sdc") in line):
            sdc = float(line[line.find("=") + 1:].strip("\n"))

    extract.append(data_seq1)
    extract.append(countItems)
    extract.append(N)
    extract.append(MIS)
    extract.append(sdc)

    return extract