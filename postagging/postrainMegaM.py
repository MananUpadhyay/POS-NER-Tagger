import sys,os,subprocess
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
            tagLine += " "+"prev:"+prevWord+ " "+"cur:"+ curWord +" "+"wordShape:" + wrdShape+ " "+ "suffix2:" +suffix2+" "+"suffix3:"+suffix3+" " + "next:"+nextWord
            outTagLine = curClassLabel + tagLine
            out.append(outTagLine + "\n")

            # shift words;
            prevWord = curWord
            prevClass = curClassLabel

    tr.close()
    return out

# def posLearn(pos_format_trainList,pos_model_file):
#     ALPHA = 1.0
#     EPOCH = 1
#     trainPOSList = pos_format_trainList
#     random.shuffle(trainPOSList)

#     vocabulary,classes,trainSize = learn.createVocabulary(trainPOSList)

#     posWeights = learn.initWeights(vocabulary,classes)
#     posCache = learn.initWeights(vocabulary,classes)

#     posModel = learn.learn(vocabulary,posWeights,posCache,trainPOSList,trainSize,ALPHA,EPOCH)

#     learn.writeModel(posModel,vocabulary,pos_model_file)

def posMegamLearn(pos_format_file,pos_model_file,megamPath):
    # megamPath = "./megam_0.92/./megam"
    megamString = megamPath + " -nc -maxi 10 multitron " + pos_format_file + " > " + pos_model_file
    p = subprocess.Popen(megamString,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0]



if __name__ == '__main__':
    
    pos_train = sys.argv[1]
    posModelFile = sys.argv[2]
    megamPath = sys.argv[3]

    formattedList = formatPOS(pos_train)
    # write to file;
    formattedFile = "./formattedTrainFile.txt"
    fmt = open(formattedFile,'w')
    for item in formattedList:
        fmt.write(str(item))
    fmt.close()

    # posLearn(formattedList,posModelFile)
    posMegamLearn(formattedFile,posModelFile,megamPath)

    os.remove(formattedFile)
