#!/usr/bin/env python
##
## ocr.py
##
## Made by xsyann
## Contact  <contact@xsyann.com>
##
## Started on  Fri Mar 28 15:09:44 2014 xsyann
## Last update Thu Apr  3 21:00:57 2014 xsyann
##

"""
Pattern recognition models for classification using OpenCV

Authors:
        Nicolas PELICAN
        Yann KOETH
"""

import os
import string
import random
import numpy as np
import cv2

class AbstractStatModel(object):

    def __init__(self, nClass):
        self.classificationCount = nClass

    def load(self, filename):
        if not os.path.isfile(filename):
            raise OSError(2, 'File not found', filename)
        self._model.load(filename)

    def save(self, filename):
        self._model.save(filename)

    def unrollResponses(self, responses):
        """Convert array of form [2, 3] to
        [0, 0, 1, 0, 0, 0 1]
        """
        sampleCount = len(responses)
        newResponses = np.zeros(sampleCount * self.classificationCount, np.int32)
        responsesIndexes = np.int32(responses + np.arange(sampleCount) * self.classificationCount)
        newResponses[responsesIndexes] = 1
        return newResponses

class ANN(AbstractStatModel):
    def __init__(self, nClass):
        super(ANN, self).__init__(nClass)
        self._model = cv2.ANN_MLP()

    def train(self, samples, responses):
        sampleCount, sampleSize = samples.shape
        newResponses = self.unrollResponses(responses).reshape(-1, self.classificationCount)

        layers = np.int32([sampleSize, 16, self.classificationCount])
        self._model.create(layers, cv2.ANN_MLP_SIGMOID_SYM, 1, 1)

        maxIter = 10000 # Maximum number of iterations
        epsilon = 0.0001 # Error threshold
        # Stop if maxIter or epsilon is reached
        condition = cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS
        criteria = (condition, maxIter, epsilon)

        params = {
            'term_crit': criteria,
            'train_method': cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP,
            'bp_dw_scale': 0.1, # Stength of the weight gradient term
            'bp_moment_scale': 0.1 # Strength of the momentum term
            }

        self._model.train(inputs=samples,
                  outputs=np.float32(newResponses),
                  sampleWeights=None,
                  params=params)

    def predict(self, samples):
        retval, outputs = self._model.predict(samples)
        return outputs.argmax(-1)

class KNearest(AbstractStatModel):
    def __init__(self, nClass):
        super(KNearest, self).__init__(nClass)
        self._model = cv2.KNearest()

    def train(self, samples, responses):
        self._model.train(samples, responses)

    def predict(self, samples):
        retval, results, neighborResponses, dists = self._model.find_nearest(samples, k=10)
        return results.ravel()
