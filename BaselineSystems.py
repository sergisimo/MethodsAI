import numpy as np
import os
import random

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

def ruleBasedClassifier(sentence):

    keywords = {"affirm":["yes", "yeah", "yea"],
                "confirm":["is it", "does it"],
                "bye": ["bye"],
                "deny":["no", "do not", "dont"],
                "hello":["hi", "hello"],
                "inform":["any", "dont care", "do not care", "doesnt matter", "does not matter","south",
                "north","east","west","centre", "center", "expensive", "moderately","moderate","cheap",
                "creative", "christmas","halal", "vegetarian","indian","cantonese","american","persian",
                "european","chinese","sea food","spanish","portuguese","italian","mediterranean","gastropub",
                "steak","bistro","british","japanese","danish","lebanese","caribbean","thai","asian","welsh",
                "french","australian","brazilian","irish","english","polynesian","corsica","vietnamese","turkish",
                "mexican","moroccan"],
                "negate":["no"],
                "repeat":["repeat"],
                "requalts": ["what about","how about","else","anything","different"],
                "reqmore":["more"],
                "request":["address","area","location","type", "type of food","price","phone","phonenumber","telephone","post code", "postcode"],
                "restart":["start over", "restart"],
                "ack" : ["okay"],
                "thankyou":["thank you", "thanks"],
                "null": ["noise", "unintelligible"]}

    #Loops through the categories and checks whether a the keyword is in the sentence
    for category in keywords:
        for keyword in keywords[category]:
            if keyword in sentence:
                return category

    return None

def testRuleBasedClassifier(testData):

    total = 0
    amountRight = 0
    for actCategory in testData:
        total += len(testData[actCategory])
        for sentence in testData[actCategory]:
            category = ruleBasedClassifier(sentence)
            if category == actCategory:
                amountRight += 1

    proportion = (amountRight / total) * 100
    print("Rule Based -> Accuracy = ", proportion, "%")

def manualRuleBasedClassifier():

    while True:
        print("Rule Based Classifier\n")
        print("Write the next sentence (exit for skiping to proporion based): ")
        sentence = input()
        if (sentence == 'exit'):
            break
        print("The category of your sentence is: ", ruleBasedClassifier(sentence.lower()))

def calculateProportions(trainingData):

    total = 0
    proportions = {}

    for actCategory in trainingData:
        total += len(trainingData[actCategory])

    for actCategory in trainingData:
        proportions[actCategory] = len(trainingData[actCategory]) * 100 / total

    return proportions


def proportionalBasedClassifier(proportions):
    return random.choices(list(proportions.keys()), list(proportions.values()))

def testProportionalBasedClassifier(testData, proportions):

    total = 0
    amountRight = 0
    for actCategory in testData:
        total += len(testData[actCategory])
        for sentence in testData[actCategory]:
            category = proportionalBasedClassifier(proportions)
            if category[0] == actCategory:
                amountRight += 1

    proportion = (amountRight / total) * 100
    print("Proportion Based -> Accuracy = ", proportion, "%")

def manualProportionalBasedClassifier(proportions):

    while True:
        print("Proportion Based Classifier\n")
        print("Write the next sentence (exit to exit program): ")
        sentence = input()
        if (sentence == 'exit'):
            break
        print("The category of your sentence is: ", proportionalBasedClassifier(proportions)[0])

trainingData, testData = createDataSets()
testRuleBasedClassifier(testData)
manualRuleBasedClassifier()
proportions = calculateProportions(trainingData)
testProportionalBasedClassifier(testData, proportions)
manualProportionalBasedClassifier(proportions)
