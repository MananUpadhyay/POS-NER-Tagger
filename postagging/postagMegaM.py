import sys,os,subprocess
sys.path.insert(1,os.path.join(sys.path[0],'..'))
import percepclassify as pc

preds = "^cla$$"

def getSuffix(word,type):
    wlen = len(word)
    return word[wlen-type:wlen]

def getWordShape(word):
    shape = ""
    for c in word:
        if c.isupper():
            shape += "A"
        elif c.islower():
            shape += "a"
        elif c.isdigit():
            shape += "d"
        else:
            shape += c
    return shape



def formatPOSTestInput(inLine):
    global preds
    out = []
    tr = inLine.split()
    splitLength = len(tr)
    prevWord = "^bos$"
    
    for i in range(splitLength):
        tagLine = ""
        outTagLine = ""
        prevClass = preds
        
        curWord = str(tr[i])
        suffix2 = getSuffix(curWord,2)
        suffix3 = getSuffix(curWord,3)
        wrdShape = getWordShape(curWord)
        
        if i == splitLength -1:
            nextWord = "^eos$"
        else:
            nextWord = str(tr[i+1])

        if tagLine == "":
            tagLine += "prev:"+prevWord+" " +"cur:"+ curWord +" "+ "wordShape:" + wrdShape+ " "+"suffix2:" +suffix2+" "+"suffix3:"+suffix3+" " + "next:"+nextWord
        else:    
            tagLine += " "+"prev:"+prevWord+" " +"cur:"+ curWord +" "+"wordShape:" + wrdShape+ " "+ "suffix2:" +suffix2+" "+"suffix3:"+suffix3+" " + "next:"+nextWord
        
        outTagLine = tagLine
        out.append(outTagLine)

        # shift words;
        prevWord = curWord
        prevClass = preds

    return out

def formatPOSTestInputMegam(train,outile):
    outFile = open(outile,'w')
    tr = open(train,'r')
    out = []
    actualLabelsList = []

    for line in tr:
        splitLine = line.split()
        splitLength = len(splitLine)
        prevWord = "^bos$"
        prevClass = "^cla$$"
        curWord = ""
        nextWord = ""
        curClassLabel = ""
        suffix2 = ""
        suffix3 = ""

        for i in range(splitLength):
            tagLine = ""
            outTagLine = ""
            # handle cur;
            curPair = splitLine[i].split("/")
            curClassLabel = str(curPair[1])
            actualLabelsList.append(str(curClassLabel))
            curWord = str(curPair[0])
            suffix2 = getSuffix(curWord,2)
            suffix3 = getSuffix(curWord,3)

            # handle next;
            if (i  == splitLength - 1):
                nextWord = "^eos$"
            else:
                nextPair = splitLine[i+1].split("/")
                nextWord = str(nextPair[0])

            # create outTagLine and write;
            tagLine += " "+"prev:"+prevWord+ " "+"cur:"+ curWord +" "+ "suffix2:" +suffix2+" "+"suffix3:"+suffix3+" " + "next:"+nextWord
            outTagLine = "TEST" + tagLine
            out.append(outTagLine + "\n")
            outFile.write(outTagLine + "\n")

            # shift words;
            prevWord = curWord
            prevClass = curClassLabel

    tr.close()
    outFile.close()
    return out,actualLabelsList


def posClassify(posModelFile,formattedFile,testLinesList,megamPath):
    global preds

    fm = open(formattedFile,'w')
    testList = []
    for testLine in testLinesList:
        testList = formatPOSTestInput(testLine)
        # write to file;
        for titem in testList:
            fm.write(str(titem) + "\n")
    fm.close()

    predict = posMegamClassify(posModelFile,formattedFile,megamPath)

    return predict


def posMegamClassify(modelFile,formatFile,megamPath):
    predTagList = []
    # megamPath = "./megam_0.92/./megam"
    megamString = megamString = megamPath+" -nc -maxi 20 -predict " + modelFile + " multitron " + formatFile

    pstdout = subprocess.Popen(megamString,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0]
    pstdout = pstdout.decode('utf-8')

    # get the tags from STDOUT;
    reconList = pstdout.split("\n")
    for reline in reconList:
        predTag = reline.split("\t")[0]
        predTagList.append(str(predTag))

    return predTagList


def writeOutput(prList,inLine):
    inList = inLine.split()
    
    # if len(inList) != len(prList):
    #     print("GOGOGOGOGO")

    printLine = ""
    for idx in range(len(inList)):
        wwrd = str(inList[idx]) + "/" + str(prList[idx])+" "
        printLine += wwrd
    sys.stdout.flush()
    print(printLine)


def writeOutputNew(prList,inTList):
    
    c = 0
    for intline in inTList:
        printLine = ""
        inOgList = intline.split()
        for ogwrd in inOgList:
            outwrd = str(ogwrd) + "/" + str(prList[c]) + " "
            printLine += outwrd
            c += 1
        sys.stdout.flush()
        print(printLine)






def calculateAccuracy(acList,oFile):
    of = open(oFile,'r')
    predList = []

    for olin in of:
        clss = olin.split("\t")[0]
        predList.append(str(clss))

    if(len(predList) != len(acList)):
        print("NOoooooo")

    correct = 0
    incorrect = 0
    for i in range(len(predList)):
        if predList[i] == acList[i]:
            correct += 1
        else:
            incorrect += 1

    accuracy = correct / (correct + incorrect)
    return accuracy


def reconstructOutput(outMegamFile,posTestFile):
    of = open(outMegamFile,'r')
    predList = []

    for olin in of:
        clss = olin.split("\t")[0]
        predList.append(str(clss))
    of.close()

    i = 0
    resultFile = open("./resultFile.txt",'w')
    ptf = open(posTestFile,'r')
    for pline in ptf:
        pList = pline.split()
        outPrintLine = ""
        for witm in pList:
            if outPrintLine == "":
                outPrintLine += (str(witm) + "/" + str(predList[i]))
            else:
                outPrintLine += (" " + str(witm) + "/" + str(predList[i]))
            i += 1
        resultFile.write(outPrintLine + "\n")
    ptf.close()
    resultFile.close()





if __name__ == '__main__':

    posModelFile = sys.argv[1]
    megamPath = sys.argv[2]

    fmtTestFile = "./fmt.megam.test.txt"
    
    inputLinesList = []
    for line in sys.stdin:
        inputLinesList.append(line)

    predList = posClassify(posModelFile,fmtTestFile,inputLinesList,megamPath)
    writeOutputNew(predList,inputLinesList)
    
    os.remove(fmtTestFile)