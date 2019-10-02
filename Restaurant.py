from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import json
import sys
import pandas
import Levenshtein as lDist

class Restaurant:

    MAX_DISTANCE = 2
    STOP_WORDS = ["want", "would", "part"]

    foodTypes = []
    areaTypes = []
    priceRanges = []
    stopWords = []
    db = []
    results = pandas.DataFrame()

    preferenceProfile = {}

    def __init__(self):
        self.extractOntology()
        self.extractDB()
        self.stopWords = set(stopwords.words('english'))
        self.stopWords.update(self.STOP_WORDS)

    def extractOntology(self):

        ontologyFile = open("ontology_dstc2.json", "r")
        ontology = json.load(ontologyFile)

        self.foodTypes = ontology["informable"]["food"]
        self.areaTypes = ontology["informable"]["area"]
        self.priceRanges = ontology["informable"]["pricerange"]

    def extractDB(self):
        self.db = pandas.read_csv('restaurantinfo.csv')

    def cleanPreferenceProfile(self):
        self.preferenceProfile = {}

    def filterWords(self, sentence):

        words = word_tokenize(sentence)

        filteredSentence = []
        for word in words:
            if word not in self.stopWords:
                filteredSentence.append(word)

        return filteredSentence

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

    def calculateLevenshtein(self, word):

        highest = sys.maxsize

        #Loop through each word. For each word, check for each category types
        #if there is a lowest distance that is also lower than 3.
        value = None

        for foodType in self.foodTypes:
            distance = lDist.distance(word, foodType)
            if distance <= self.MAX_DISTANCE and distance < highest:
                highest = distance
                category = "food"
                value = foodType

        for areaType in self.areaTypes:
            distance = lDist.distance(word, areaType)
            if distance <= self.MAX_DISTANCE and distance < highest:
                highest = distance
                category = "area"
                #print(word, "--", areaType, "--", distance)
                value = areaType

        for priceRange in self.priceRanges:
            distance = lDist.distance(word, priceRange)
            if distance <= self.MAX_DISTANCE and distance < highest:
                highest = distance
                category = "pricerange"
                value = priceRange

        if value != None:
            self.preferenceProfile[category] = value

    def findRestaurant(self):

        self.results = pandas.DataFrame()
        for preference in self.preferenceProfile:
            if self.results.empty:
                self.results = self.db[self.db[preference] == self.preferenceProfile[preference]]
            else:
                self.results = self.results[self.results[preference] == self.preferenceProfile[preference]]
