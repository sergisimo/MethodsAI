import os
import json 
import glob
import random

def printConvo(userData, systemData):
    print("session id:", userData["session-id"])

    print(userData["task-information"]["goal"]["text"])

    temp = 0
    for speach in systemData["turns"]:
        print("system:", speach["output"]["transcript"])
        print("user:", userData["turns"][temp]["transcription"])
        temp += 1

def writeConvo(userData, systemData, file):
    file.write("session id: %s\n" % userData["session-id"])

    file.write("%s\n" % userData["task-information"]["goal"]["text"])

    temp = 0
    for speach in systemData["turns"]:
        file.write("system: %s\n" %  speach["output"]["transcript"])
        file.write("user: %s\n" % userData["turns"][temp]["transcription"])
        temp += 1
    
    file.write("\n\n")

def writeFile(waiting):
    if waiting is False:
        file = open("convo.txt", "w+")
    
    userFiles = glob.glob('**/label.json', recursive=True)
    systemFiles = glob.glob('**/log.json', recursive=True)
    i = 0
    for userFile in userFiles:
        with open(userFile) as f:
            userData = json.load(f)
        with open(systemFiles[i]) as f:
            systemData = json.load(f)
        i += 1
        if waiting is True :
            printConvo(userData, systemData)
            input('press Enter to display another chat both conversation')
        else: 
            writeConvo(userData, systemData, file)

    if waiting is False: 
        file.close()

def RuleBasedBaseline():
    
    #all the keywords
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
                "null": ["noise", "unintelligible"],}

    #opens the list of utterances (will have to be changed to the dictionary)
    utterances = open("C:\\Users\\Amir Pliev\\Documents\\Python\\MethodsinAI\\MethodsAI\\utterances.txt")
    writingFile = open("C:\\Users\\Amir Pliev\\Documents\\Python\\MethodsinAI\\MethodsAI\\RuleBasedResult.txt", "w")

    #Counters in order to calculate the accuracy
    amountRight = 0
    total = 0

    #Loop through the file
    for line in utterances:
        total = total +1

        #Splits the sentence, removes the category
        fullsentence = line
        sentence = fullsentence.split(" ", 1)[1]
        actCategory = fullsentence.split(" ", 1)[0]
        sentence = sentence.lower()
        
        #Loops through the categories and checks whether a the keyword is in the sentence
        for category in keywords:
            for keyword in keywords[category]:
                if keyword in sentence:
                    string = category + " " + sentence
                    writingFile.write(string)

                    #Counts for the proportion
                    if category == actCategory:
                        amountRight = amountRight +1
                    # else:
                    #     print("Sentence: ", sentence)
                    #     print("What it is: ", actCategory)
                    #     print("What we thought: ", category)
                    #     print("-----------------")

    proportion = (amountRight/total)*100
    print("Accuracy = ", proportion, "%")
    utterances.close()
    writingFile.close()

def ProportionalBaseline():

    categories = {"ack":0,
                "affirm":0,
                "bye":0,
                "confirm":0,
                "deny":0,
                "hello":0,
                "inform":0,
                "negate":0,
                "null":0,
                "repeat":0,
                "requalts":0,
                "reqmore":0,
                "request":0,
                "restart":0,
                "thankyou":0}


    #opens the list of utterances (will have to be changed to the dictionary)
    utterances = open("C:\\Users\\Amir Pliev\\Documents\\Python\\MethodsinAI\\MethodsAI\\utterances.txt")
    writingFile = open("C:\\Users\\Amir Pliev\\Documents\\Python\\MethodsinAI\\MethodsAI\\ProportionalResults.txt", "w")
    total = 0

    #Loop through the file and get the proportions
    for line in utterances:
        total += 1
        fullsentence = line
        cat = fullsentence.split(" ", 1)[0]

        for category in categories:
            if category == cat:
                categories[category] += 1
    
    utterances.close()
    newList = []

    #Creates list according to above distribution
    for cat in categories:
        for i in range(categories[cat]):
            newList.append(cat)
    
    utterances = open("C:\\Users\\Amir Pliev\\Documents\\Python\\MethodsinAI\\MethodsAI\\utterances.txt")
    amountRight = 0

    #Loop through file and assign
    for line in utterances:

        #Splits the sentence, splits the category from the sentence
        fullsentence = line
        sentence = fullsentence.split(" ", 1)[1]
        actCategory = fullsentence.split(" ", 1)[0]
        sentence = sentence.lower()

        #Assigns a random category
        assignedCategory = random.choice(newList)
        writingFile.write(assignedCategory + " " + sentence)

        #Keeps track of the correct guesses
        if assignedCategory == actCategory:
            amountRight += 1
        
    #Calculate and print the accuracy and close the files
    proportion = (amountRight/total)*100
    print("Accuracy is: ", proportion, "%")
    utterances.close()
    writingFile.close()

RuleBasedBaseline()
ProportionalBaseline()
