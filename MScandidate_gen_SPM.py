from collections import OrderedDict
import sys, re
import itertools
from collections import Counter

def level2candgen(L, MIS, countItems, N, sdc):
    # print "SDC",sdc
    C = []
    # print "L:",L
    for l in range(0, len(L)):

        C.append("{" + L[l] + "}" + "{" + L[l] + "}")

        for h in range(l + 1, len(L)):
            if (h != l):

                if (countItems[L[h]] / float(N) >= MIS[L[l]] and abs(
                        (countItems[L[h]] / float(N)) - (countItems[L[l]] / float(N))) <= sdc):
                    C.append("{" + L[l] + "," + L[h] + "}")
                    C.append("{" + L[l] + "}" + "{" + L[h] + "}")
                    C.append("{" + L[h] + "," + L[l] + "}")
                    C.append("{" + L[h] + "}" + "{" + L[l] + "}")

    return C

def CandGen(fkth, MIS, k, sdc, N, countItems):
    
    candList = []
    fKsplit = [(seq.replace("<", "")).replace(">", "") for seq in fkth]
    for s1Seq in fKsplit:
        s1 = s1Seq
        

        for s2Seq in fKsplit:

            s2 = s2Seq
            

            listS1 = filterSeq(s1)
            listS2 = filterSeq(s2)
            
            if (checkFirstItemIsLesser(listS1, MIS) == 1):

                MISlastSeq2 = float(MIS.get(listS2[-1]))
                MISfirstSeq1 = float(MIS.get(listS1[0]))
                secItemS1sdc = listS1[1]
                lastItemS2sdc = listS2[-1]

                lastItemS1 = listS1[-1]
                lastItemS2 = listS2[-1]

                del listS1[1]
                del listS2[-1]

                if ((','.join(listS1) == ','.join(listS2)) and (MISlastSeq2 > MISfirstSeq1) and (
                        abs((countItems[secItemS1sdc] / float(N)) - (countItems[lastItemS2sdc] / float(N))) <= sdc)):
                    lastElemS2 = "{" + lastItemS2 + "}"

                    if (s2.rfind(lastElemS2) == (len(s2) - len(lastElemS2))):
                        withLastElemS1 = s1 + lastElemS2
                        candList.append(withLastElemS1)
                        if ((lengthSeq(s1) == 2) and (sizeSeq(s1) == 2) and (int(lastItemS2) > int(lastItemS1))):
                            lastElemItemS1 = s1[:len(s1) - 1] + ',' + lastItemS2 + s1[len(s1) - 1:]
                            candList.append(lastElemItemS1)


                    elif (((lengthSeq(s1) == 2 and sizeSeq(s1) == 1) and (int(lastItemS2) > int(lastItemS1))) or (
                            lengthSeq(s1) > 2)):
                        ItemtoLastElemS1 = s1[:len(s1) - 1] + ',' + lastItemS2 + s1[len(s1) - 1:]
                        candList.append(ItemtoLastElemS1)

            elif (checkLastItemIsLesser(listS2, MIS) == 1):

                MISlastSeq2 = float(MIS.get(listS2[-1]))
                MISfirstSeq1 = float(MIS.get(listS1[0]))
                firstItemS1 = listS1[0]
                firstItemS2 = listS2[0]

                firstS1itemsdc = listS1[0]
                secLastS2itemsdc = listS2[-2]
                del listS1[0]
                del listS2[-2]

                if ((','.join(listS1) == ','.join(listS2)) and (MISlastSeq2 < MISfirstSeq1) and (abs(
                        (countItems[firstS1itemsdc] / float(N)) - (countItems[secLastS2itemsdc] / float(N))) <= sdc)):
                    firstElemS1 = "{" + firstItemS1 + "}"
                    
                    if (s1.find(firstElemS1) == 0):
                        withFirstElemS2 = firstElemS1 + s2
                        candList.append(withFirstElemS2)
                        if ((lengthSeq(s2) == 2) and (sizeSeq(s2) == 2) and (int(firstItemS1) < int(firstItemS2))):
                            firstElemItemS2 = s2[:1] + firstItemS1 + ',' + s2[1:]
                            candList.append(firstElemItemS2)

                    elif (((lengthSeq(s2) == 2 and sizeSeq(s2) == 1) and (int(firstItemS2) > int(firstItemS1))) or (
                            lengthSeq(s2) > 2)):
                        ItemtoFirstElemS2 = s2[:1] + firstItemS1 + ',' + s2[1:]
                        candList.append(ItemtoFirstElemS2)

            else:
                candList.append((gspTypejoin(s1, s2, sdc, N, countItems)))
                candList = list(set(candList))
    if '' in candList:
        candList.remove('')

    for itemValue in candList:
        if (prune(itemValue, fKsplit, MIS, k)) == 0:
            candList.remove(itemValue)

    if '' in candList:
        candList.remove('')

    candList = list(OrderedDict.fromkeys(candList))

    return candList

def gspTypejoin(s1, s2, sdc, N, countItems):
    c = ""
    s1_l = re.findall(r'\d+', s1)
    s2_l = re.findall(r'\d+', s2)
    firstS1sdc = s1_l[0]
    del s1_l[0]
    last_item = s2_l[len(s2_l) - 1]
    del s2_l[len(s2_l) - 1]
    if (s1_l == s2_l) and (abs((countItems[firstS1sdc] / float(N)) - (countItems[last_item] / float(N))) <= sdc):
        if "," in s2[s2.rfind('{', 0, len(s2)) + 1:s2.rfind('}', 0, len(s2))]:
            c = s1[0:len(s1) - 1] + "," + last_item + "}"
        else:
            c = s1 + "{" + last_item + "}"

    return c

def confirmOrder(c, s):
    cand = re.findall(r'\d+', c)
    trans = re.findall(r'\d+', s)
    for i in range(1, len(cand)):
        if (trans.index(cand[i]) < trans.index(cand[i - 1])):
            if ((len(trans) - trans[::-1].index(cand[i]) - 1) < (len(trans) - trans[::-1].index(cand[i - 1]) - 1)):
                return 0
    return 1


#### Excluding characters except digits
def filterSeq(seq):
    ItemList = re.sub(r'\D', " ", seq).strip()
    return ItemList.split()

def lengthSeq(S):
    ItemList = re.sub(r'\D', " ", S).strip()
    ListItems = ItemList.split()
    return len(ListItems)

def sizeSeq(S):
    count = S.count('{')
    if (count != S.count('}')):
        return 0
    return count

def checkFirstItemIsLesser(S, MIS):
    firstItem = S[0]
    MISFirstItem = float(MIS.get(firstItem))

    for items in S[1:]:
        if (float(MIS.get(items)) <= MISFirstItem):
            return 0

    return 1

def checkLastItemIsLesser(S, MIS):
    lastItem = S[-1]
    MISLastItem = float(MIS.get(lastItem))

    for items in S[:-1]:
        if (float(MIS.get(items)) <= MISLastItem):
            return 0

    return 1

def prune(candi, FK_1, MIS, k):
    # FK_1={}
    L = []
    pattern = {}
    minitems = []
    cseq = []
    temp = candi
    while temp != "":
        cseq.append(temp[temp.find("{") + 1:temp.find("}")].split(","))
        temp = temp.replace("{" + temp[temp.find("{") + 1:temp.find("}")] + "}", "", 1)

    I = re.findall(r'\d+', candi)
    X = []

    for i in range(0, len(I)):
        X.append(int(I[i]))
        pattern[I[i]] = -1

    min_value = min([(MIS[x], x) for x in MIS])[0]
    for key in MIS.keys():
        if MIS[key] == min_value:
            minitems.append(int(key))

    prev_pat = -1

    L = list(itertools.combinations(X, k - 1))

    sub = ""

    for i in range(0, len(L)):

        sub = ""
        prev_pat = -1
        for j in range(0, len(L[i])):

            if pattern[str(L[i][j])] == -1:
                pat = list(get_positions(cseq, str(L[i][j])))
                pattern[str(L[i][j])] = pat[0][0]
                current_pat = pat[0][0]

            else:
                pat = list(get_positions(cseq[prev_pat + 1:], str(L[i][j])))
                if len(pat) != 0:
                    pattern[str(L[i][j])] = pat[0][0] + prev_pat + 1
                    current_pat = pat[0][0] + prev_pat + 1

            sub = (sub + "{" + str(L[i][j]) + "}") if (current_pat != prev_pat) else (sub[:-1] + "," + str(L[i][j]) + "}")

            prev_pat = current_pat

        if sub in FK_1:
            return 1
        else:
            return(0 if checkmintem(sub, minitems) == 1 else 1)
            

def checkmintem(seq, minitems):
    items = re.findall(r'\d+', seq)

    for i in range(0, len(items)):
        if int(items[i]) in minitems:
            return 1

    return 0

def get_positions(xs, item):
    if isinstance(xs, list):
        for i, it in enumerate(xs):
            for pos in get_positions(it, item):
                yield (i,) + pos
    elif xs == item:
        yield ()

