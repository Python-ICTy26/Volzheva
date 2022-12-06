from __future__ import division
import csv
import string
from collections import defaultdict
from math import log


class WordProperties(object):
    def __init__(self, counter_: int, probability_: float):
        self.counter = counter_
        self.probability = probability_

    def __repr__(self):
        return "{0}(counter: {1}, probability: {2})".format(self.__class__.__name__, self.counter, self.probability)


"""word_stats = {
    # word -> [ham, spam]
    # word -> [positive, possible, negative]
    'this':     [WordProperties(10, 0.2), WordProperties(20, 0.3)],
    'apple':    [WordProperties(12, 0.25), WordProperties(234, 0.3)],
}"""



class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.word_stats = {}
        self.hum_probability = 0
        self.spam_probability = 0

    def fit(self, words, labels):
        ix = 0
        """ Fit Naive Bayes classifier according to X, y."""
        #записываем количество
        for word in words:
            for each_word in list(word.split()):
                if each_word not in self.word_stats:
                    self.word_stats[each_word] = [WordProperties(0, 0), WordProperties(0, 0)]
                if labels[ix] == "ham":
                    self.word_stats[each_word][0].counter += 1
                if labels[ix] == "spam":
                    self.word_stats[each_word][1].counter += 1
            ix += 1
        #считаем вероятность
        len_vector = len(self.word_stats)
        for each in self.word_stats:
            self.word_stats[each][0].probability = (self.word_stats[each][0].counter + self.alpha)/(self.word_stats[each][0].counter + self.word_stats[each][1].counter + len_vector * self.alpha)
            self.word_stats[each][1].probability = (self.word_stats[each][1].counter + self.alpha)/(self.word_stats[each][0].counter + self.word_stats[each][1].counter + len_vector * self.alpha)
        #считаем общую вероятность
        spam_counter = 0
        ham_counter = 0
        for i in labels:
            if i == "spam":
                spam_counter += 1
            if i == "ham":
                ham_counter += 1
        self.hum_probability = ham_counter / len(labels)
        self.spam_probability = spam_counter / len(labels)
        return self.word_stats

    def predict(self, words):
        result = []
        """ Perform classification on an array of test vectors X. """
        for word in words:
            words_probability_ham = self.hum_probability
            words_probability_spam = self.spam_probability
            for each_word in list(word.split()):
                if each_word in self.word_stats:
                    words_probability_ham += self.word_stats[each_word][0].probability
                    words_probability_spam += self.word_stats[each_word][1].probability
            if words_probability_ham > words_probability_spam:
                result.append("ham")
            else:
                result.append("spam")

        return result

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predictions = self.predict(X_test)
        count = 0
        for i in range(len(predictions)):
            if predictions[i] == y_test[i]:
                count += 1

        return count / len(predictions)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


with open("c:\\Programming\\PROGRAMMING\\Volzheva\\homework06\\data\\SMSSpamCollection", encoding='utf-8') as f:
    data = list(csv.reader(f, delimiter="\t"))

X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X = [clean(x).lower() for x in X]
X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

model = NaiveBayesClassifier(1)
model.fit(X_train, y_train)
print(model.predict(X_test))
print("-----------")
print(y_test)
print(model.score(X_test, y_test))
