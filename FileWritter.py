import os
import json
import glob

# This function prints the conversation on the terminal.
def printConvo(userData, systemData):
    print("session id:", userData["session-id"])

    print(userData["task-information"]["goal"]["text"])

    temp = 0
    for speach in systemData["turns"]:
        print("system:", speach["output"]["transcript"])
        print("user:", userData["turns"][temp]["transcription"])
        temp += 1

# This function writes data into the conversation and the utterances file.
def writeFiles(userData, systemData, conversationsFile, utterancesFile):

    conversationsFile.write("session id: %s\n" % userData["session-id"])
    conversationsFile.write("%s\n" % userData["task-information"]["goal"]["text"])

    temp = 0
    for speach in systemData["turns"]:

        dialogAct = userData["turns"][temp]["semantics"]["cam"]
        utteranceContent = userData["turns"][temp]["transcription"]

        conversationsFile.write("system: %s\n" %  speach["output"]["transcript"])
        conversationsFile.write("user: %s\n" % utteranceContent)
        utterancesFile.write("%s %s\n" % (dialogAct.split("(")[0], utteranceContent.lower()))

        temp += 1

    conversationsFile.write("\n\n")

# This function reads all the data and processes it.
def writeFile(waiting):
    if waiting is False:
        conversationsFile = open("convo.txt", "w+")
        utterancesFile = open("utterances.txt", "w+")

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
            writeFiles(userData, systemData, conversationsFile, utterancesFile)

    if waiting is False:
        conversationsFile.close()
        utterancesFile.close()

writeFile(False)
