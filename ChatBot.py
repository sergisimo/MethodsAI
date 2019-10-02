from MLClassifier import MLClassifier
from Restaurant import Restaurant

class ChatBot:

    class ActCategories:
        hello = "hello"
        inform = "inform"
        bye = "bye"
        reqmore = "reqmore"
        restart = "restart"
        thankyou = "thankyou"

    class BotSentences:
        welcome = "Welcome to the recommendation bot! How can I help you?"
        welcomeAgain = "Welcome again! What can I do for you?"
        bye = "Good bye! Thanks for using our recommendation system."
        noPreference = "Sorry, I don't see any preference in your sentence. Can you reformulate your request?"
        noRestaurant = "Sorry, there is no restaurant that matches your preferences."
        noMoreRestaurants = "Sorry, there is no more restaurants matching your preferences."
        thanks = "You are welcome! Can I help you with something else?"
        uknown = "Sorry, I don't understand whats your request. Can you reformulate your sentence?"

    classifier = MLClassifier()
    sentences = BotSentences()
    categories = ActCategories()
    restaurantDB = Restaurant()
    state = None

    def __init__(self):
        self.classifier.train()
        self.state = self.initialState

    def stateMachine(self, actCategory, sentence):
        return self.state(actCategory, sentence)

    def initialState(self, actCategory, sentence):

        if actCategory == self.categories.hello:
            print(self.sentences.welcomeAgain)
        elif actCategory == self.categories.inform:
            self.searchRestaurant(sentence)
            self.state = self.informState
        else:
            print(self.sentences.uknown)

    def informState(self, actCategory, sentence):

        if actCategory == self.categories.inform:
            self.searchRestaurant(sentence)
        if actCategory == self.categories.reqmore:
            self.printRestaurant(False)
        else:
            print(self.sentences.uknown)

    def searchRestaurant(self, sentence):
        self.restaurantDB.extractPreferences(sentence)
        if (len(self.restaurantDB.preferenceProfile) == 0):
            print(self.sentences.noPreference)
        else:
            self.restaurantDB.findRestaurant()
            self.printRestaurant(True)

    def printRestaurant(self, isFirst):
        if (self.restaurantDB.results.empty):
            if isFirst:
                print(self.sentences.noRestaurant)
            else:
                print(self.sentences.noMoreRestaurants)
        else:
            print("I found the restaurant", self.restaurantDB.results["restaurantname"].iloc[0])
            print("\tAddress: ", self.restaurantDB.results["addr"].iloc[0])
            print("\tPostcode: ", self.restaurantDB.results["postcode"].iloc[0])
            print("\tPhone: ", self.restaurantDB.results["phone"].iloc[0])
            self.restaurantDB.results = self.restaurantDB.results.drop(self.restaurantDB.results.index[0])

    def restart(self):
        self.state = self.initialState
        self.restaurantDB.cleanPreferenceProfile()

    def startConversation(self):

        print(self.sentences.welcome)

        while True:
            sentence = input()
            actCategory = self.classifier.predictSentence(sentence.lower())

            if (actCategory == self.categories.bye):
                break
            if (actCategory == self.categories.restart):
                print(self.sentences.welcome)
                self.restart()
            elif (actCategory == self.categories.thankyou):
                print(self.sentences.thanks)
                self.restart()
            else:
                self.stateMachine(actCategory, sentence.lower())

bot = ChatBot()
bot.startConversation()
