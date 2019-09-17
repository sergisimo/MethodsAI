
import os
import json 
import glob

asdf

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

writeFile(True)