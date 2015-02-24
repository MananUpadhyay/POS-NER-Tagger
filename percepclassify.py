import sys,perceplearn as learn

def readModel(modelFile):

    m = open(modelFile,'r')
    classes = set()
    weights = {}
    vocabulary = set()

    li = m.readline()
    lind = li.split()
    if lind[0] == "WEIGHTS":
        c = 0
        while c != int(lind[1]):
            line = m.readline()
            lst = line.split()

            if lst[0] not in classes:
                classes.add(str(lst[0]))

            if lst[0] not in weights.keys():
                weights[str(lst[0])] = {}

            for wt in lst[1:]:
                wc = wt.split("->")
                if wc[0] not in vocabulary:
                    vocabulary.add(str(wc[0]))

                wtClass = weights[str(lst[0])]
                if wc[0] not in wtClass:
                    wtClass[str(wc[0])] = float(wc[1])

            c += 1
    m.close()

    return classes,weights,vocabulary


def classify(classes,weights,vocabulary,testLine):
    # classify each Line;
    predict = []
    t = testLine.split()
    cls = str(t[0])
    lin = testLine
    feat = learn.createFeature(lin,vocabulary)
    predClass = learn.calculateActivation(feat,weights)
    predict.append(str(predClass))

    return predClass


if __name__== '__main__':

    modelFile = sys.argv[1]

    classes,weights,vocabulary = readModel(modelFile)
    
    for line in sys.stdin:
        prediction = classify(classes,weights,vocabulary,str(line))
        sys.stdout.flush()
        print(prediction)

    