from MLClassifier import MLClassifier
from Restaurant import Restaurant
from BaselineSystems import ruleBasedClassifier
import speech_recognition as sr
import json

class ChatBot:

    # Class Constants
    class ActCategories:
        hello = "hello"
        inform = "inform"
        bye = "bye"
        reqmore = "reqmore"
        restart = "restart"
        thankyou = "thankyou"
        affirm = "affirm"
        negate = "negate"

    class BotSentences:
        welcome = "Welcome to the recommendation bot! How can I help you?"
        welcomeAgain = "Welcome again! What can I do for you?"
        bye = "Good bye! Thanks for using our recommendation system."
        noPreference = "Sorry, I don't see any preference in your sentence. Can you reformulate your request?"
        morePreferences = "Would you like to specify more preferences?"
        morePreferencesUknown = "Please affirm, reject or tell me your preferences."
        noRestaurant = "Sorry, there is no restaurant that matches your preferences."
        noMoreRestaurants = "Sorry, there is no more restaurants matching your preferences."
        thanks = "You are welcome! Can I help you with something else?"
        uknown = "Sorry, I don't understand whats your request. Can you reformulate your sentence?"
        restartNotAllowed = "Sorry the conversation cannot be restarted. Please restart the program to use our services again."
        maxUtterancesReached = "The number of awnsers per conversations is limited to {}."
        restartProgram = "Please restart the program to use our services again."

    # Attributes
    classifier = MLClassifier()
    sentences = BotSentences()
    categories = ActCategories()
    utteranceCounter = 0
    errorCounter = 0
    restaurantDB = None
    config = None
    state = None

    # Constructor
    def __init__(self):
        self.classifier.train()
        self.state = self.initialState
        configFile = open("config.json", "r")
        self.config = json.load(configFile)
        self.restaurantDB = Restaurant(self)

    # This function executes the actual state of the bot.
    def stateMachine(self, actCategory, sentence):
        return self.state(actCategory, sentence)

    # This function implements the initial state.
    def initialState(self, actCategory, sentence):

        if actCategory == self.categories.hello:
            self.output(self.sentences.welcomeAgain)
        elif actCategory == self.categories.inform:
            self.searchRestaurant(sentence)
            self.state = self.informState
        else:
            self.errorCounter += 1
            self.output(self.sentences.uknown)

    # This function implements the inform state.
    def informState(self, actCategory, sentence):

        if actCategory == self.categories.inform:
            self.searchRestaurant(sentence)
        if actCategory == self.categories.reqmore:
            self.printRestaurant(False)
        else:
            self.errorCounter += 1
            self.output(self.sentences.uknown)

    # This function searches a restaurant depending on the preferences.
    def searchRestaurant(self, sentence):
        self.restaurantDB.extractPreferences(sentence)
        if (len(self.restaurantDB.preferenceProfile) == 0):
            self.output(self.sentences.noPreference)
        elif (len(self.restaurantDB.preferenceProfile) < 3):
            while len(self.restaurantDB.preferenceProfile) < 3:
                if (self.askForMorePreferences()):
                    break
            self.restaurantDB.findRestaurant()
            self.printRestaurant(True)
        else:
            self.restaurantDB.findRestaurant()
            self.printRestaurant(True)

    def askForMorePreferences(self):
        self.output(self.sentences.morePreferences)
        while True:
            sentence, actCategory = self.predictInput()
            if (actCategory == self.categories.affirm):
                self.output("Tell me!")
            elif (actCategory == self.categories.negate):
                return True
            elif (actCategory == self.categories.inform):
                self.restaurantDB.extractPreferences(sentence)
                break
            else:
                self.errorCounter += 1
                self.output(self.sentences.morePreferencesUknown)

        return False

    # This function prints a restaurant information.
    def printRestaurant(self, isFirst):
        if (self.restaurantDB.results.empty):
            if isFirst:
                self.output(self.sentences.noRestaurant)
            else:
                self.output(self.sentences.noMoreRestaurants)
        else:
            self.output("I found the restaurant " + self.restaurantDB.results["restaurantname"].iloc[0])
            self.output("\tAddress: " + self.restaurantDB.results["addr"].iloc[0])
            self.output("\tPhone: " + self.restaurantDB.results["phone"].iloc[0])
            self.restaurantDB.results = self.restaurantDB.results.drop(self.restaurantDB.results.index[0])

    # This function controls if the conversation has to be restarted.
    def restart(self):
        if (self.config["allowRestart"]):
            self.output(self.sentences.welcome)
            self.state = self.initialState
            self.restaurantDB.cleanPreferenceProfile()
            self.utteranceCounter = 0
            self.errorCounter = 0
            return False

        self.output(self.sentences.restartNotAllowed)
        return True

    # This function prints the bot sentences depending on the configuration.
    def output(self, output):
        if (self.config["outputCaps"]):
            print(output.upper())
        else:
            print(output)

    # This function gets the input of the user and predicts its category.
    def predictInput(self):
         sentence = self.userInput()
         self.utteranceCounter += 1
         if (self.config["inputLowerCase"]):
             sentence = sentence.lower()

         if (self.config["machingLearningClassifier"]):
             return sentence, self.classifier.predictSentence(sentence)

         return sentence, ruleBasedClassifier(sentence)

    def userInput(self):

        if (self.config["speechRecognition"]):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Recording...")
                audio = r.listen(source)
                print("Recorded!")

            try:
                sentence = r.recognize_google(audio)
                print ("User speech -> ", sentence)
                return sentence
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return ""
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""

        return input()

    # This function controls the amount of utterances.
    def checkLimit(self):
        if (self.config["utterancesLimit"] > 0 and self.utteranceCounter >= self.config["utterancesLimit"]):
            self.output(self.sentences.maxUtterancesReached.format(self.config["utterancesLimit"]))
            if (self.config["utterancesLimitRestart"]):
                if (self.restart()):
                    return True
            else:
                self.output(self.sentences.restartProgram)
                return True

        return False

    # This function starts the conversation and controls the conversation.
    def startConversation(self):

        self.output(self.sentences.welcome)

        while True:

            sentence, actCategory = self.predictInput()

            if (actCategory == self.categories.bye):
                self.output(self.sentences.bye)
                break
            elif (actCategory == self.categories.restart):
                if (self.restart()):
                    break
            elif (actCategory == self.categories.thankyou):
                self.output(self.sentences.thanks)
                self.restart()
            else:
                self.stateMachine(actCategory, sentence)

            if (self.checkLimit()):
                break

        print("The error rate is:", (self.errorCounter / self.utteranceCounter) * 100, "%")

bot = ChatBot()
bot.startConversation()
