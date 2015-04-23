import sys,os
sys.path.insert(1,os.path.join(sys.path[0],'..'))
import perceplearn as learn,random

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

def formatPOS(train):
    tr = open(train,'r')
    out = []

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
            curWord = str(curPair[0])
            suffix2 = getSuffix(curWord,2)
            suffix3 = getSuffix(curWord,3)
            wrdShape = getWordShape(curWord)

            # handle next;
            if (i  == splitLength - 1):
                nextWord = "^eos$"
            else:
                nextPair = splitLine[i+1].split("/")
                nextWord = str(nextPair[0])

            # create outTagLine and write;
            tagLine += " "+"prev:"+prevWord+ " "+"prevClass:" +prevClass+" "+"cur:"+ curWord +" "+"wordshape:"+wrdShape+" "+ "suffix2:" +suffix2+" "+"suffix3:"+suffix3+" " + "next:"+nextWord
            # tagLine += " "+"prev:"+prevWord+ " "+"prevClass:"+prevClass+" "+"cur:"+ curWord +" "+"wordshape:"+wrdShape+" "+ "next:"+nextWord

            outTagLine = curClassLabel + tagLine
            out.append(outTagLine + "\n")

            # shift words;
            prevWord = curWord
            prevClass = curClassLabel

    tr.close()
    return out

def posLearn(pos_format_trainList,pos_model_file):
    ALPHA = 1.0
    EPOCH = 5
    trainPOSList = pos_format_trainList
    random.shuffle(trainPOSList)

    vocabulary,classes,trainSize = learn.createVocabulary(trainPOSList)

    posWeights = learn.initWeights(vocabulary,classes)
    posCache = learn.initWeights(vocabulary,classes)
    pos_avg_weights = learn.initWeights(vocabulary,classes)

    posModel = learn.learn(vocabulary,posWeights,posCache,pos_avg_weights,trainPOSList,trainSize,ALPHA,EPOCH)

    learn.writeModel(posModel,vocabulary,pos_model_file)


if __name__ == '__main__':
    
    pos_train = sys.argv[1]
    posModelFile = sys.argv[2]

    formattedList = formatPOS(pos_train)
    posLearn(formattedList,posModelFile)
