from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

import numpy as np

def createDataSets():
    utterancesFile = open("utterances.txt", "r")
    utterancesData = {}
    for line in utterancesFile:
        line = line.split(" ", 1)
        if line[0] not in utterancesData:
            utterancesData[line[0]] = []
        utterancesData[line[0]].append(line[1].strip())

    trainingData = {}
    testData = {}
    for dialogType in utterancesData:
        splitted = np.split(utterancesData[dialogType], [int(len(utterancesData[dialogType]) * 0.85)])
        trainingData[dialogType] = splitted[0].tolist()
        testData[dialogType] = splitted[1].tolist()

    utterancesFile.close()

    return trainingData, testData

def tokenizeData(trainingData, testData):

    X = []
    Y = []
    vectorizer = CountVectorizer()

    for dialogType in trainingData:
        for sentence in trainingData[dialogType]:
            X.append(sentence)
            Y.append(dialogType)

    for dialogType in testData:
        for sentence in testData[dialogType]:
            X.append(sentence)
            Y.append(dialogType)

    X = vectorizer.fit_transform(X)

    return X.toarray(), Y,

trainingData, testData = createDataSets()
X, Y = tokenizeData(trainingData, testData)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15)

clf = DecisionTreeClassifier(random_state=0)
clf = clf.fit(X_train, Y_train)
print("Decision Tree Classifier -> Accuracy: ", clf.score(X_test, Y_test) * 100 , "%")
