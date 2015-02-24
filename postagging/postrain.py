import sys,os
sys.path.insert(1,os.path.join(sys.path[0],'..'))
import perceplearn as learn,random

def formatPOS(train):
    tr = open(train,'r')
    out = []

    for line in tr:
        splitLine = line.split()
        splitLength = len(splitLine)
        prevWord = "^bos$"
        curWord = ""
        nextWord = ""
        classLabel = ""

        for i in range(splitLength):
            tagLine = ""
            outTagLine = ""
            # handle cur;
            curPair = splitLine[i].split("/")
            classLabel = str(curPair[1])
            curWord = str(curPair[0])

            # handle next;
            if (i  == splitLength - 1):
                nextWord = "^eos$"
            else:
                nextPair = splitLine[i+1].split("/")
                nextWord = str(nextPair[0])

            # create outTagLine and write;
            tagLine += " " + "prev:" + prevWord + " " +"cur:"+ curWord +" "+ "next:"+nextWord
            outTagLine = classLabel + tagLine
            out.append(outTagLine + "\n")

            # shift words;
            prevWord = curWord

    tr.close()
    return out

def posLearn(pos_format_trainList,pos_model_file):
    ALPHA = 1.0
    EPOCH = 1
    trainPOSList = pos_format_trainList
    random.shuffle(trainPOSList)

    vocabulary,classes,trainSize = learn.createVocabulary(trainPOSList)

    posWeights = learn.initWeights(vocabulary,classes)
    posCache = learn.initWeights(vocabulary,classes)

    posModel = learn.learn(vocabulary,posWeights,posCache,trainPOSList,trainSize,ALPHA,EPOCH)

    learn.writeModel(posModel,vocabulary,pos_model_file)


if __name__ == '__main__':
    
    pos_train = sys.argv[1]
    posModelFile = sys.argv[2]

    formattedList = formatPOS(pos_train)
    posLearn(formattedList,posModelFile)
