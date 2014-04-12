#!/usr/bin/env python
##
## ocr.py
##
## Made by xsyann
## Contact  <contact@xsyann.com>
##
## Started on  Fri Mar 28 15:09:44 2014 xsyann
## Last update Thu Apr  3 21:02:45 2014 xsyann
##

"""
Dataset pre-processing for OCR using OpenCV.

Authors:
        Nicolas PELICAN
        Yann KOETH
"""

import os
import string
import random
import numpy as np
import cv2

class Dataset(object):
    """Dataset of image files.
    Generate samples and responses arrays from images.
    """

    def __init__(self, folders):
        """Init the dataset from a folder dict of form
        {'label1': 'path/item1', 'label2': 'path/label2', ...}
        """
        self.samples = None
        self.responses = None
        self.maxPerClass = 170
        self.__folders = folders
        self.__classifications = self.__loadClassifications()

    def preprocess(self):
        items = self.__getItems()
        self.__stackSamples(items)

    def getResponse(self, index):
        return self.__classifications[index]

    @property
    def classificationCount(self):
        return len(self.__classifications)

    @property
    def sampleCount(self):
        sampleCount, size = self.samples.shape
        return sampleCount

    def __loadClassifications(self):
        classifications = []
        for label, folder in self.__folders.iteritems():
            if not label in classifications:
                classifications.append(label)
        return classifications

    def __stackSamples(self, items):
        """Create samples and responses arrays.
        """
        samples = []
        responses = []
        nClass = self.classificationCount
        for item in items:
            responses.append(self.__classifications.index(item.classification))
            samples.append(item.sample)
        self.samples = np.vstack(samples)
        self.responses = np.array(responses)

    def __getItems(self):
        """Create dataset items.
        """
        items = []
        for label, folder in self.__folders.iteritems():
            images = self.__getImages(folder)
            for i, image in enumerate(images):
                if i >= self.maxPerClass:
                    break
                item = DatasetItem()
                item.loadFromFile(image)
                item.classification = label
                items.append(item)
        # Shuffle items to have an heterogeneous array when we split
        # samples and tests
        random.shuffle(items)
        return items

    def __getImages(self, folder):
        """Returns a list of all images in folder.
        """
        imgExt = [".bmp", ".png"]
        images = []
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                filename, ext = os.path.splitext(file)
                if ext.lower() in imgExt:
                    images.append(os.path.join(folder, file))
        return images


class DatasetItem(object):
    """An item in the data set.
    Handle pre-processing of that item.
    """
    RESIZE = 16

    def __init__(self):
        self.input = None
        self.preprocessed = None
        self.classification = None

    def loadFromFile(self, filename):
        if not os.path.isfile(filename):
            raise OSError(2, 'File not found', filename)
        self.__load(filename)
        self.__preprocess()

    def loadFromImage(self, img):
        self.input = img
        self.__preprocess()

    @property
    def sample(self):
        sample = np.array(self.preprocessed)
        return sample.ravel().astype(np.float32)

    def __load(self, filename):
        self.input = cv2.imread(filename, cv2.CV_LOAD_IMAGE_COLOR)

    def __mergeContours(self, contours):
        """Merge all bounding boxes.
        Returns x, y, w, h.
        """
        x, y, x1, y1 = [], [], [], []
        for cnt in contours:
            pX, pY, pW, pH = cv2.boundingRect(cnt)
            x.append(pX)
            y.append(pY)
            x1.append(pX + pW)
            y1.append(pY + pH)
        bbX, bbY = min(x), min(y)
        bbW, bbH = max(x1) - bbX, max(y1) - bbY
        return bbX, bbY, bbW, bbH

    def __cropToFit(self, image):
        """Crop image to fit the bounding box.
        """
        clone = image.copy()
        contours, hierarchy = cv2.findContours(clone, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return image
        x, y, w, h = self.__mergeContours(contours)
        cv2.rectangle(self.input, (x, y), (x + w, y + h), (0, 0, 255), 1)
        return image[y:y+h, x:x+w]

    def __ratioResize(self, image):
        """Resize image to get an aspect ratio of 1:1 (square).
        """
        h, w = image.shape
        ratioSize = max(h, w)
        blank = np.zeros((ratioSize, ratioSize), np.uint8)
        x = (ratioSize - w) / 2.0
        y = (ratioSize - h ) / 2.0
        blank[y:y+h, x:x+w] = image
        return blank

    def __preprocess(self):
        """Pre-process image :
        - Convert To Grayscale
        - Gaussian Blur (remove noise)
        - Threshold (black and white image)
        - Crop to fit bounding box
        - Resize
        """
        gray = cv2.cvtColor(self.input, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)
        thresh = cv2.adaptiveThreshold(src=blur, maxValue=255,
                                       adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       thresholdType=cv2.THRESH_BINARY_INV,
                                       blockSize=11, C=2)
        cropped = self.__cropToFit(thresh)
        squared = self.__ratioResize(cropped)
        self.preprocessed = cv2.resize(squared, (self.RESIZE, self.RESIZE))

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description="Show the pre-processing step of OCR.")
    parser.add_argument("filename", help="File to pre-process")
    args = parser.parse_args()

    item = DatasetItem()
    try:
        item.loadFromFile(args.filename)
    except (OSError, cv2.error) as err:
        print err
        sys.exit(1)

    print __doc__

    cv2.imshow("Input", item.input)
    cv2.imshow("Pre-processed", item.preprocessed)
    cv2.moveWindow("Input", 200, 0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
