from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import json
import sys
import pandas
import Levenshtein as lDist

class Restaurant:

    # Constants
    STOP_WORDS = ["want", "would", "part"]

    # Attributes
    levenshteinDistance = 2
    foodTypes = []
    areaTypes = []
    priceRanges = []
    stopWords = []
    db = []
    bot = None
    results = pandas.DataFrame()
    preferenceProfile = {}

    # Constructor
    def __init__(self, bot):
        self.extractOntology()
        self.extractDB()
        self.stopWords = set(stopwords.words('english'))
        self.stopWords.update(self.STOP_WORDS)
        self.levenshteinDistance = bot.config["levenshteinDistance"]
        self.bot = bot

    # This funciton extracts the ontology form the json file.
    def extractOntology(self):

        ontologyFile = open("ontology_dstc2.json", "r")
        ontology = json.load(ontologyFile)

        self.foodTypes = ontology["informable"]["food"]
        self.areaTypes = ontology["informable"]["area"]
        self.priceRanges = ontology["informable"]["pricerange"]

    # This function extracts all the DB from the csv file.
    def extractDB(self):
        self.db = pandas.read_csv('restaurantinfo.csv')

    # This funciton clears the preferences in order to restart the conversation.
    def cleanPreferenceProfile(self):
        self.preferenceProfile = {}

    # This function filters the sentences in order to delete stop words.
    def filterWords(self, sentence):

        words = word_tokenize(sentence)

        filteredSentence = []
        for word in words:
            if word not in self.stopWords:
                filteredSentence.append(word)

        return filteredSentence

    # This function extracts the preferences using keyword maching.
    def extractPreferences(self, sentence):

        #Check whether a preference is specified literally
        words = self.filterWords(sentence)

        for word in words:
            if word in self.foodTypes:
                self.preferenceProfile["food"] = word
            elif word in self.areaTypes:
                self.preferenceProfile["area"] = word
            elif word in self.priceRanges:
                self.preferenceProfile["pricerange"] = word
            else:
                self.calculateLevenshtein(word)

    # This fucntion calculates levenshtein distance for a word in order to find similar words.
    def calculateLevenshtein(self, word):

        highest = sys.maxsize

        #Loop through each word. For each word, check for each category types
        #if there is a lowest distance that is also lower than 3.
        value = None

        for foodType in self.foodTypes:
            distance = lDist.distance(word, foodType)
            if distance <= self.levenshteinDistance and distance < highest:
                highest = distance
                category = "food"
                value = foodType

        for areaType in self.areaTypes:
            distance = lDist.distance(word, areaType)
            if distance <= self.levenshteinDistance and distance < highest:
                highest = distance
                category = "area"
                value = areaType

        for priceRange in self.priceRanges:
            distance = lDist.distance(word, priceRange)
            if distance <= self.levenshteinDistance and distance < highest:
                highest = distance
                category = "pricerange"
                value = priceRange

        if value != None:
            self.askForConfirmation(word, category, value)

    # This function asks if the levensthein prediction is correct to the user.
    def askForConfirmation(self, word, category, value):

        if (self.bot.config["checkLevenshtein"]):
            while True:
                self.bot.output("Did you mean " + value + " instead of " + word + "?")
                sentence, actCategory = self.bot.predictInput()
                if (actCategory == self.bot.categories.affirm):
                    self.preferenceProfile[category] = value
                    break;
                elif (actCategory == self.bot.categories.negate):
                    break;
                else:
                    self.bot.output("Please affirm or reject my question.")
        else:
            self.preferenceProfile[category] = value

    # This function finds the restaurant maching the preferences in the DB.
    def findRestaurant(self):

        self.results = pandas.DataFrame()
        for preference in self.preferenceProfile:
            if self.results.empty:
                self.results = self.db[self.db[preference] == self.preferenceProfile[preference]]
            else:
                self.results = self.results[self.results[preference] == self.preferenceProfile[preference]]
