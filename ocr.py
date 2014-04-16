#!/usr/bin/env python
##
## ocr.py
##
## Made by xsyann
## Contact  <contact@xsyann.com>
##
## Started on  Fri Mar 28 15:09:44 2014 xsyann
## Last update Fri Apr  4 21:34:32 2014 xsyann
##

"""
Optical Character Recognition using
OpenCV Artificial Neural Network.

Authors:
        Nicolas PELICAN
        Yann KOETH
"""

import os
import string
import numpy as np
import cv2
import dataset
import models as mod
import common
from analyzer import Analyzer

class OCR(object):

    MODEL_ANN = 0
    MODEL_KNEAREST = 1
    LETTERS = 1
    DIGITS = 2
    SYMBOLS = 4

    def saveModel(self, filename):
        self.__model.save(filename)

    def loadModel(self, filename, type=MODEL_ANN, flags=DIGITS):
        folders = OCR.generateFolderList(flags=flags)
        self.__dataset = dataset.Dataset(folders)
        self.__model = self.__initModel(type)
        self.__model.load(filename)

    def trainModel(self, type=MODEL_ANN, flags=DIGITS, trainRatio=.5, maxPerClass=100, verbose=True):
        folders = OCR.generateFolderList(flags=flags)
        self.__dataset = dataset.Dataset(folders)
        self.__dataset.maxPerClass = maxPerClass
        self.__dataset.preprocess(trainRatio)
        self.__model = self.__initModel(type)
        self.__trainModel(verbose=verbose, trainRatio=trainRatio)

    def charFromImage(self, image):
        item = dataset.DatasetItem()
        item.loadFromImage(image)
        return self.__charFromDatasetItem(item)

    def charFromFile(self, filename):
        item = dataset.DatasetItem()
        item.loadFromFile(filename)
        return self.__charFromDatasetItem(item)

    def __charFromDatasetItem(self, item):
        sample = np.array([item.sample])
        response = self.__dataset.getResponse(int(self.__model.predict(sample)[0]))
        return response

    def __trainModel(self, verbose=False, trainRatio=.5):
        if verbose:
            analyzer = Analyzer(self.__model, self.__dataset, trainRatio)
            analyzer.start()
        if self.__dataset.trainSampleCount > 0:
            self.__model.train(self.__dataset.trainSamples, self.__dataset.trainResponses)
        if verbose:
            analyzer.stop()
            analyzer.analyze()
            print analyzer

    def __initModel(self, type):
        """Instanciate the choosen model.
        Be sure that MODEL constants are in the same order
        as the models array.
        """
        models = [mod.ANN, mod.KNearest]
        Model = models[type]
        return Model(self.__dataset.classificationCount)

    @staticmethod
    def generateFolderList(flags):
        """Returns a dictionnary containing the label
        and the folder path of each classification.
        {'a': 'a_small', '0': num_0, '|': 'sym_pipe', ...}
        """
        folder = os.path.join(os.path.dirname(__file__), "dataset")
        small = "_small"
        num = "num_"
        sym = "sym_"

        symbols = {'&': 'amper', '\'': 'apos', '@': 'arob', '`': 'bquote',
                   '\\': 'bslash', '^': 'caret', ':': 'colon', ',': 'comma',
                   '$': 'dollar', '=': 'equal', '!': 'exclmark', '>': 'gthan',
                   '-': 'hyphen', '{': 'lcbracket', '(': 'lparen',
                   '[': 'lsqbracket', '<': 'lthan', '#': 'num', '%': 'pcent',
                   '|': 'pipe', '+': 'plus', '.': 'point', '?': 'questmark',
                   '"': 'quotmark', '}': 'rcbracket', ')': 'rparen',
                   ']': 'rsqbracket', ';': 'scolon', '/': 'slash', '*': 'star',
                   '~': 'tilde', '_': 'under', ' ': 'space' }

        folderList = {}

        if flags & OCR.LETTERS:
            for letter in list(string.ascii_lowercase):
                folderList[letter.upper()] = os.path.join(folder, letter)
                folderList[letter] = os.path.join(folder, letter + small)

        if flags & OCR.DIGITS:
            for digit in list(string.digits):
                folderList[digit] = os.path.join(folder, num + digit)

        if flags & OCR.SYMBOLS:
            for symbol in list(string.punctuation + ' '):
                if symbol in symbols:
                    folderList[symbol] = os.path.join(folder, sym + symbols[symbol])
        return folderList

def restricted_float(x):
    fx = float(x)
    if fx < 0.0 or fx > 1.0:
        raise argparse.ArgumentTypeError("%s not in range [0.0, 1.0]" % x)
    return fx

def check_negative(x):
    ix = int(x)
    if ix < 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % x)
    return ix

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description='Train classification model.')
    parser.add_argument('-l', dest='letters', action='store_true', help='Train to recognize letters')
    parser.add_argument('-s', dest='symbols', action='store_true', help='Train to recognize symbols')
    parser.add_argument('-d', dest='digits', action='store_true', help='Train to recognize digits')
    parser.add_argument("-t", "--train-ratio", type=restricted_float, default=.5)
    parser.add_argument("-m", "--max-per-class", type=check_negative, default=400)
    args = parser.parse_args()

    flags = 0
    if args.letters:
        flags |= OCR.LETTERS
    if args.digits:
        flags |= OCR.DIGITS
    if args.symbols:
        flags |= OCR.SYMBOLS
    if not flags:
        parser.print_help()
        sys.exit(0)

    print __doc__

    ocr = OCR()
    modelType = OCR.MODEL_ANN
    ocr.trainModel(modelType, flags, args.train_ratio, args.max_per_class)
    if args.train_ratio > 0:
        ocr.saveModel(common.generateModelFilename(args, modelType))
