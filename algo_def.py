import sys, re
import itertools
from collections import Counter
from collections import OrderedDict

################Flatten the list###########

def flatten(seq):
    for itemset in seq:
        if type(itemset) in (list, tuple):
            for item in flatten(itemset):
                yield item
        else:
            yield itemset


def makeDistinct(items):
    for cand in items:
        if "," in cand:
            no1 = int(cand[1:cand.find(",")])
            no2 = int(cand[cand.find(",") + 1:-1])
            # print "no1,no2",no1,no2
            if no1 >= no2:
                items.remove(cand)

    return items

def generate_F(C, MIS, count, num):
    # print"Inside Gen_f"
    C2 = []
    for c in C:
        items = re.findall(r'\d+', c)
        minitem = items[0]
        for item in items:
            if (MIS[item]) <= MIS[minitem]:
                minitem = item

        if (c in count) and (float(count[c]) / float(num)) >= MIS[minitem]:
            C2.append(c)
    return C2

def contains(c, s):
    temp = c
    s = s.replace(" ", "")
    counter = 0
    cseq = []
    sortedCandidates = []
    dseq = []
    flag = []

    #seq_track = {}

    # Splitting the candidate sequence into separate elements
    while temp != "":
        cseq.append(temp[temp.find("{") + 1:temp.find("}")].split(","))
        temp = temp.replace("{" + temp[temp.find("{") + 1:temp.find("}")] + "}", "", 1)
        counter = counter + 1

    temp = s

    # Splitting the data sequence into separate elements
    while temp != "":
        dseq.append(temp[temp.find("{") + 1:temp.find("}")].split(","))
        temp = temp.replace("{" + temp[temp.find("{") + 1:temp.find("}")] + "}", "", 1)

    flag=[0 for i in range(0, len(dseq))]

    sortedCandidates = [i for i in sorted(cseq, key=lambda i: len(i), reverse=True)]

    pattern = -1

    for item in cseq:

        for i in range(pattern + 1, len(dseq)):

            if (len(item) != len(set(item))) == False:

                if (set(item).issubset(set(dseq[i]))) and (flag[i] == 0):
                    pattern = i
                    flag[i] = 1
                    break

    return 1 if sum(flag) == counter else 0




