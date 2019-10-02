from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

import numpy as np

class MLClassifier:

    vocabulary = []
    classifier = None

    # Function that extracts the data for training the classifier
    def createDataSetsForML(self):

        utterancesFile = open("utterances.txt", "r")

        X = []
        Y = []
        for line in utterancesFile:
            line = line.split(" ", 1)
            X.append(line[1].strip())
            Y.append(line[0])

        return X, Y

    # Function that vectorizes a sentence according to the bag of words.
    def predictSentence(self, sentence):

        iterable = []
        iterable.append(sentence)

        vectorizer = CountVectorizer(vocabulary=self.vocabulary)
        vector = vectorizer.fit_transform(iterable)
        self.vocabulary = vectorizer.vocabulary_

        categories = self.classifier.predict(vector.toarray().reshape(1, -1))

        return categories[0]

    # Function for transforming the sentences in a bag of words.
    def tokenizeData(self, X):

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(X)
        self.vocabulary = vectorizer.vocabulary_

        return X.toarray()

    # Function that trains the classifier.
    def train(self):
        # Create data and vectorize it.
        X, Y = self.createDataSetsForML()
        X = self.tokenizeData(X)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15)

        # Creates the Decision tree classifier, trains it and tests it.
        self.classifier = DecisionTreeClassifier(random_state=0)
        self.classifier.fit(X_train, Y_train)
        print("Accuracy: ", self.classifier.score(X_test, Y_test) * 100 , "%")
