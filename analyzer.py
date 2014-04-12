##
## analyzer.py
##
## Made by xsyann
## Contact  <contact@xsyann.com>
##
## Started on  Wed Apr  2 14:52:28 2014 xsyann
## Last update Fri Apr  4 19:01:25 2014 xsyann
##

"""
Optical Character Recognition Analyzer.

Authors:
        Nicolas PELICAN
        Yann KOETH
"""

import timeit
import numpy as np
from collections import Counter
from collections import defaultdict

class Analyzer(object):
    def __init__(self, model, dataset, trainRatio):
        self.__model = model
        self.__dataset = dataset
        self.__trainRatio = trainRatio
        self.__start = 0
        self.__elapsed = 0
        self.trainMedian = 0
        self.trainMean = 0
        self.trainMAD = 0
        self.trainVar = 0
        self.trainStd = 0
        self.trainVarCoeff = 0

    def start(self):
        self.__start = timeit.default_timer()

    def stop(self):
        self.__elapsed = timeit.default_timer() - self.__start

    def __str__(self):
        res = "\tTrain samples\t\tTest samples"
        for label, ((tTrain, nTrain, pTrain), (tTest, nTest, pTest)) in sorted(self.classifications.items()):
            res += "\n  {0}:\t{1} / {2}\t({3} %)\t  -  {4} / {5}\t({6} %)".format(label,
                                                                                  tTrain, nTrain, pTrain,
                                                                                  tTest, nTest, pTest)
        res += "\n\n  Best recognized in train set : %s (%d %%)\n" % self.maxTrain
        res += "  Worst recognized in train set : %s (%d %%)\n" % self.minTrain
        res += "\n  Best recognized in test set : %s (%d %%)\n" % self.maxTest
        res += "  Worst recognized in test set : %s (%d %%)\n" % self.minTest
        res += '\n ------------------\n'
        res += '| Training samples |\n'
        res += ' ------------------\n'
        res += "  Mean : %d\n" % self.trainMean
        res += "  Median : %d\n" % self.trainMedian
        res += "  Median absolute deviation : %.2f\n" % self.trainMAD
        # res += "Variance : %2.f\n" % self.trainVar
        res += "  Standard deviation : %.2f\n" % self.trainStd
        res += "  Coefficient of variation : %.2f %%\n" % self.trainVarCoeff

        res += '\nTrain set: %d samples | Test set: %d samples\n' % (self.trainCount, self.testCount)
        res += 'Training time: %.4f s\n' % self.__elapsed
        res += '\nTrain accuracy: %.2f %% | Test accuracy %.2f %%\n' % (self.trainRate * 100, self.testRate * 100)
        return res

    def __mapDict(self, dict, func):
        res = func(dict, key=dict.get)
        return (res, dict[res])

    def analyze(self):
        """Analyze dataset repartition and model performance.
        """
        self.trainCount = int(self.__dataset.sampleCount * self.__trainRatio)
        self.testCount = self.__dataset.sampleCount - self.trainCount
        samples, responses = self.__dataset.samples, self.__dataset.responses
        trainSamples, trainResponses = samples[:self.trainCount], responses[:self.trainCount]
        testSamples, testResponses = samples[self.trainCount:], responses[self.trainCount:]

        truthTableTrain, self.trainRate = (defaultdict(int), 0)
        truthTableTest, self.testRate = (defaultdict(int), 0)

        if 0 < self.__trainRatio:
            truthTableTrain, self.trainRate = self.__analyzePredict(trainSamples, trainResponses)
        if 0 < self.__trainRatio < 1:
            truthTableTest, self.testRate = self.__analyzePredict(testSamples, testResponses)
        countTrain = Counter([self.__dataset.getResponse(i) for i in trainResponses])
        countTest = Counter([self.__dataset.getResponse(i) for i in testResponses])

        # Create a dict { label1: (train, test), label2: ... }
        # where train = (wellPredicted, total, percentage)
        # and test  = (wellPredicted, total, percentage)
        trainPercents, testPercents = {}, {}
        self.classifications = {}
        for k in list(set(countTrain.keys()) | set(countTest.keys())):
            trainPercents[k] = int(truthTableTrain[k] / float(countTrain[k]) * 100) if countTrain[k] > 0 else 100
            testPercents[k] = int(truthTableTest[k] / float(countTest[k]) * 100) if countTest[k] > 0 else 100
            self.classifications[k] = ((truthTableTrain[k], countTrain[k], trainPercents[k]),
                                  (truthTableTest[k], countTest[k], testPercents[k]))

        self.minTrain, self.maxTrain = self.__mapDict(trainPercents, min), self.__mapDict(trainPercents, max)
        self.minTest, self.maxTest = self.__mapDict(testPercents, min), self.__mapDict(testPercents, max)

        self.__analyzeTrainingSamples([v for k, v in countTrain.iteritems()])

    def __analyzeTrainingSamples(self, trainingSamples):
        """Analyze training samples distribution.
        """
        if trainingSamples:
            self.trainMedian = np.median(trainingSamples)
            self.trainMean = np.mean(trainingSamples)
            self.trainMAD = np.median(np.absolute(trainingSamples - self.trainMedian))
            self.trainVar = np.var(trainingSamples)
            self.trainStd = np.std(trainingSamples)
            if np.mean(trainingSamples) > 0:
                self.trainVarCoeff = (self.trainStd / self.trainMean * 100)

    def __analyzePredict(self, samples, responses):
        """Analyze the rate of true predictions.
        """
        predict = self.__model.predict(samples)
        trueTable = (predict == responses)
        truePredict = Counter([self.__dataset.getResponse(c) for i, c in enumerate(predict) if trueTable[i]])
        rate = np.mean(predict == responses)
        return truePredict, rate
