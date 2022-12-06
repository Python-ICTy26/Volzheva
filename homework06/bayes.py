from __future__ import division
import csv
import string


class WordProperties(object):
    def __init__(self, counter_: int, probability_: float):
        self.counter = counter_
        self.probability = probability_

    def __repr__(self):
        return "{0}(counter: {1}, probability: {2})".format(self.__class__.__name__, self.counter, self.probability)


"""word_stats = {
    # word -> [good, maybe, never]
    'this':     [WordProperties(10, 0.2), WordProperties(20, 0.3)],
    'apple':    [WordProperties(12, 0.25), WordProperties(234, 0.3)],
}"""


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.word_stats = {}
        self.good_probability = 0
        self.maybe_probability = 0
        self.never_probability = 0

    def fit(self, words, labels):
        ix = 0
        """ Fit Naive Bayes classifier according to X, y."""
        #записываем количество
        for word in words:
            for each_word in list(word.split()):
                if each_word not in self.word_stats:
                    self.word_stats[each_word] = [WordProperties(0, 0), WordProperties(0, 0), WordProperties(0, 0)]
                if labels[ix] == "good":
                    self.word_stats[each_word][0].counter += 1
                if labels[ix] == "maybe":
                    self.word_stats[each_word][1].counter += 1
                if labels[ix] == "never":
                    self.word_stats[each_word][2].counter += 1
            ix += 1
        #считаем вероятность
        len_vector = len(self.word_stats)
        for each in self.word_stats:
            len_vector_word = self.word_stats[each][0].counter + self.word_stats[each][1].counter + self.word_stats[each][2].counter
            self.word_stats[each][0].probability = (self.word_stats[each][0].counter + self.alpha) / (
                    len_vector_word + len_vector * self.alpha)
            self.word_stats[each][1].probability = (self.word_stats[each][1].counter + self.alpha) / (
                    len_vector_word + len_vector * self.alpha)
            self.word_stats[each][2].probability = (self.word_stats[each][2].counter + self.alpha) / (
                    len_vector_word + len_vector * self.alpha)
        #считаем общую вероятность
        good_counter = 0
        maybe_counter = 0
        never_counter = 0
        for i in labels:
            if i == "never":
                never_counter += 1
            if i == "maybe":
                maybe_counter += 1
            if i == "good":
                good_counter += 1
        self.good_probability = good_counter / len(labels)
        self.maybe_probability = maybe_counter / len(labels)
        self.never_probability = never_counter / len(labels)
        return self.word_stats

    def predict(self, words):
        result = []
        """ Perform classification on an array of test vectors X. """
        for word in words:
            words_probability_good = self.good_probability
            words_probability_maybe = self.maybe_probability
            words_probability_never = self.never_probability
            for each_word in list(word.split()):
                if each_word in self.word_stats:
                    words_probability_good = self.word_stats[each_word][0].probability
                    words_probability_maybe = self.word_stats[each_word][1].probability
                    words_probability_never = self.word_stats[each_word][2].probability
            max_probability = max(words_probability_good, words_probability_maybe, words_probability_never)
            if max_probability == words_probability_good:
                result.append("good")
            elif max_probability == words_probability_maybe:
                result.append("maybe")
            elif max_probability == words_probability_never:
                result.append("never")
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


