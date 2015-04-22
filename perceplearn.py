import sys,random

def generateRandom(sptr):
    t = open(sptr,'r')

    ll = []
    for line in t.readlines():
        ll.append(str(line))
    t.close()

    random.shuffle(ll)

    rList = []
    for i in range(len(ll)):
        rList.append(ll[i])

    random.shuffle(rList)
    return rList

def createVocabulary(rfile):
    vocab = set()
    classes = set()
    trainSize = 0

    # f = open(rfile,'r')
    f = rfile
   
    for line in f:
        line = line.strip("\n")
        spl = line.split()
        # make vocabulary
        for word in spl[1:]:
            if word not in vocab:
                # if word.isalpha():
                vocab.add(word)
                

        # find number of classes
        clss = str(spl[0])
        if clss not in classes:
            classes.add(clss)
        trainSize += 1

    # f.close()
    # vocab.add("$$$")  # add unknown word
    return vocab, classes, trainSize


def initWeights(vocab,classes):
    wts = {}
    for cls2 in classes:
        w = {}
        for word in vocab:
            w[word] = 0.000
        
        if(len(w) != len(vocab)):
            print("initWeights")

        wts[cls2] = w
    return wts

def createFeature(lline,vocab):
    lt = lline.split()
    featSet = {}

    for ww in lt[1:]:
        if ww in vocab:
            if ww not in featSet.keys():
                featSet[ww] = 0
            featSet[ww] += 1
        # else:
        #     wrd = "$$$"
        #     if wrd not in featSet.keys():
        #         featSet[wrd] = 0
            
        #     featSet[wrd] +=  1
    return featSet

def calculateActivation(ft,wt):
    maxClass = ""
    maxDot = -2147483648
        
    for clsa in wt.keys():
        wcc = wt[clsa]
        dot = 0
        for wrd4 in ft.keys():
            fv = ft[wrd4]
            # fv = 1
            wv = wcc[wrd4]
            dot += (fv * wv)
        
        # print("dot: "+str(dot)+clsa)

        if dot > maxDot:
            maxDot = dot
            maxClass = clsa

    return maxClass


def finalAvgWeights(og,cv,aw,cc,epoch):
    avgg_weights = aw
    factor = epoch/cc

    for cls1 in og.keys():
        wc = og[cls1]
        cache = cv[cls1]

        for wrd3 in wc.keys():
            cache[wrd3] /= cc
            avgg_weights[cls1][wrd3] = float(wc[wrd3] - cache[wrd3])

    return avgg_weights


def learn(vocabulary,w,cw,awt,trainFile,trSize,alpha,epoch):
    # f = open(trainFile,'r')
    f = trainFile
    c = 1
    for e in range(epoch):
        for line1 in f:
            lst = line1.split()
            y = str(lst[0])
            feat = createFeature(line1,vocabulary)
            z = calculateActivation(feat,w)
            # z,y are String tags
            if z != y:
                # update z,y wts;
                wz = w[z]
                wy = w[y]
                cachez = cw[z]
                cachey = cw[y]
                for wrd1 in feat.keys():
                    fwt = feat[wrd1]
                    # fwt = 1
                    wz[wrd1] -= (fwt)
                    wy[wrd1] += (fwt)
                    cachez[wrd1] -= (c * fwt)
                    cachey[wrd1] += (c * fwt)
                # w[z] = wz
                # w[y] = wy
                # ==============================================>>
                # update z,y cached;
                # wwz = w[z]
                # cachez = cw[z]
                # wwy = w[y]
                # cachey = cw[y]
                # for wrd2 in vocabulary:
                #     cachez[wrd2] -= (c * wwz[wrd2])
                #     cachey[wrd2] += (c * wwy[wrd2])
                # w[z] = wz
                # w[y] = wy
                #=================================================||
                
            c += 1
    resModel = finalAvgWeights(w,cw,awt,c,epoch)
    # f.close()
    return resModel

def writeModel(model,vocabulary,modelFile):
    m = open(modelFile,'w')
    m.write("WEIGHTS" + " " + str(len(model))+"\n")
    
    for cls in model.keys():
        wts = model[cls]
        wtString = ""
        for w in wts.keys():
            wtString += " " + str(w) + "->" +str(wts[w])
        m.write(cls + wtString + "\n")

    m.close()


if __name__ == '__main__':
    EPOCH = 1
    ALPHA = 1

    spam_train = sys.argv[1]
    modelFile = sys.argv[2]

    trainList = generateRandom(spam_train)

    vocabulary,classes,trainSize = createVocabulary(trainList)

    weights = initWeights(vocabulary,classes)
    cacheWeights = initWeights(vocabulary,classes)
    avg_weights = initWeights(vocabulary,classes)


    model = learn(vocabulary,weights,cacheWeights,avg_weights,trainList,trainSize,ALPHA,EPOCH)

    writeModel(model,vocabulary,modelFile)
    