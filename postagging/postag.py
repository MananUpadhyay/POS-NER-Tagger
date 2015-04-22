import sys,os
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

        tagLine += " "+"prev:"+prevWord+" " +"cur:"+ curWord +" "+"wordshape:"+wrdShape+" "+ "suffix2:" +suffix2+" "+"suffix3:"+suffix3+" " + "next:"+nextWord
        outTagLine = tagLine
        out.append(outTagLine + "\n")

        # shift words;
        prevWord = curWord
        prevClass = preds

    return out

def posClassify(classes,wts,voco,testLine):
    global preds
    predict = []
    testList = formatPOSTestInput(testLine)
    for createdLine in testList:
        preds = pc.classify(classes,wts,voco,createdLine)
        predict.append(preds)
    
    return predict

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


if __name__ == '__main__':

    posModelFile = sys.argv[1]
    classes,wts,voco = pc.readModel(posModelFile)

    for line in sys.stdin:
        predList = posClassify(classes,wts,voco,line)
        writeOutput(predList,line)
