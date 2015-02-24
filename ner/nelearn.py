import sys,os
sys.path.insert(1,os.path.join(sys.path[0],'..'))
import perceplearn as learn

def formatNER(train):
    tr = open(train,'r',encoding='utf-8', errors='ignore')
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
            classLabel = str(curPair[2])
            curWord = str(curPair[0]) + "/" +str(curPair[1])

            # handle next;
            if (i  == splitLength - 1):
                nextWord = "^eos$"
            else:
                nextPair = splitLine[i+1].split("/")
                nextWord = str(nextPair[0]) + "/" +str(nextPair[1])

            # create outTagLine and write;
            tagLine += " " + "prev:" + prevWord + " " +"cur:"+ curWord +" "+ "next:"+nextWord
            outTagLine = classLabel + tagLine
            out.append(outTagLine + "\n")

            # shift words;
            prevWord = curWord

    tr.close()
    return out

def nerLearn(ner_formatted_trainList,ner_model_file):
    ALPHA = 1.0
    EPOCH = 1
    trainNERList = ner_formatted_trainList

    vocabulary,classes,trainSize = learn.createVocabulary(trainNERList)

    nerWeights = learn.initWeights(vocabulary,classes)
    nerCache = learn.initWeights(vocabulary,classes)

    nerModel = learn.learn(vocabulary,nerWeights,nerCache,trainNERList,trainSize,ALPHA,EPOCH)

    learn.writeModel(nerModel,vocabulary,ner_model_file)

if __name__ == '__main__':
    sys.path.insert(1,os.path.join(sys.path[0],'..'))
    ner_train = sys.argv[1]
    nerModelFile = sys.argv[2]

    formattedList = formatNER(ner_train)
    nerLearn(formattedList,nerModelFile)
