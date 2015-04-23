import sys,os
sys.path.insert(1,os.path.join(sys.path[0],'..'))
import perceplearn as learn

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

def formatNER(train):
    tr = open(train,'r',encoding='iso-8859-1')
    out = []

    for line in tr:
        splitLine = line.split()
        splitLength = len(splitLine)
        prevWord = "^bos$"
        prevClass = "^cla$$"
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
            suffix2 = getSuffix(curWord,2)
            suffix3 = getSuffix(curWord,3)
            wrdShape = getWordShape(curWord)

            # handle next;
            if (i  == splitLength - 1):
                nextWord = "^eos$"
            else:
                nextPair = splitLine[i+1].split("/")
                nextWord = str(nextPair[0]) + "/" +str(nextPair[1])

            # create outTagLine and write;
            tagLine += " "+"prev:"+prevWord+" "+"prevClass:" +prevClass+" " +"cur:"+ curWord +" "+"wordshape:"+wrdShape+" "+ "suffix2:" +suffix2+" "+"suffix3:"+suffix3+" " + "next:"+nextWord
            outTagLine = classLabel + tagLine
            out.append(outTagLine + "\n")

            # shift words;
            prevWord = curWord
            prevClass = classLabel

    tr.close()
    return out

def nerLearn(ner_formatted_trainList,ner_model_file):
    ALPHA = 1.0
    EPOCH = 10
    trainNERList = ner_formatted_trainList

    vocabulary,classes,trainSize = learn.createVocabulary(trainNERList)

    nerWeights = learn.initWeights(vocabulary,classes)
    nerCache = learn.initWeights(vocabulary,classes)
    ner_avg_weights = learn.initWeights(vocabulary,classes)

    nerModel = learn.learn(vocabulary,nerWeights,nerCache,ner_avg_weights,trainNERList,trainSize,ALPHA,EPOCH)

    learn.writeModel(nerModel,vocabulary,ner_model_file)

if __name__ == '__main__':
    sys.path.insert(1,os.path.join(sys.path[0],'..'))
    ner_train = sys.argv[1]
    nerModelFile = sys.argv[2]

    formattedList = formatNER(ner_train)
    nerLearn(formattedList,nerModelFile)
