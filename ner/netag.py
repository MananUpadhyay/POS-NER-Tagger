import sys,os
sys.path.insert(1,os.path.join(sys.path[0],'..'))
import percepclassify as pc

def formatNERTestInput(inLine):
    out = []
    tr = inLine.split()
    splitLength = len(tr)
    prevWord = "^bos$"

    for i in range(splitLength):
        tagLine = ""
        outTagLine = ""
        curWord = str(tr[i])
        if i == splitLength -1:
            nextWord = "^eos$"
        else:
            nextWord = str(tr[i+1])

        tagLine += " " + "prev:" + prevWord + " " +"cur:"+ curWord +" "+ "next:"+nextWord
        outTagLine = tagLine
        out.append(outTagLine + "\n")

        # shift words;
        prevWord = curWord

    return out

def nerClassify(classes,wts,voco,testLine):
    predict = []
    testList = formatNERTestInput(testLine)
    for createdLine in testList:
        preds = pc.classify(classes,wts,voco,createdLine)
        predict.append(preds)
        
    return predict

def writeOutput(prList,inLine):
    inList = inLine.split()
    if len(inList) != len(prList):
        print("GOGOGOGOGO")

    printLine = ""
    for idx in range(len(inList)):
        wwrd = str(inList[idx]) + "/" + str(prList[idx])+" "
        printLine += wwrd
    sys.stdout.flush()
    print(printLine)


if __name__ == '__main__':
    sys.path.insert(1,os.path.join(sys.path[0],'..'))

    nerModelFile = sys.argv[1]
    classes,wts,voco = pc.readModel(nerModelFile)

    for line in sys.stdin:
        predList = nerClassify(classes,wts,voco,line)
        writeOutput(predList,line)


