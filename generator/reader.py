#!/usr/bin/env python
##
## reader.py for OCR
## 
## Made by xsyann
## Contact  <contact@xsyann.com>
## 
## Started on  Fri Mar 28 15:09:44 2014 xsyann
## Last update Thu Apr  3 20:51:41 2014 xsyann
##

"""
Read a scanned dataset.


Authors:
        Nicolas PELICAN
        Yann KOETH

Keys:
        UP    - Increase boxes size
        DOWN  - Decrease boxes
        SPACE - Write Dataset
"""

import sys
import os
import string
import numpy as np
import itertools
import cv2
import ocr
import common
from cv2 import cv

class DatasetReader:
    
    TEMPLATE = "template.bmp"
    CLASS_COUNT = 95
    MARGIN = 5
    PREVIEW_HEIGHT = 850
    FINAL_SIZE = 50

    KEY_ESC = 27
    KEY_UP = 0
    KEY_DOWN = 1
    
    def __init__(self, filename, dryRun):

        if not os.path.isfile(filename):
            raise OSError(2, 'File not found', filename)

        self.__userMargin = 0
        self.__dryRun = dryRun
        cv2.namedWindow("Dataset Reader")
        templatePath = os.path.join(os.path.dirname(__file__), self.TEMPLATE)
        self.__template = cv2.imread(templatePath)
        self.__img = cv2.imread(filename)
        h, w = self.__img.shape[0], self.__img.shape[1]
        self.__template = cv2.resize(self.__template, (w, h))

    def getData(self, index):
        data = (string.lowercase + string.uppercase +
                string.digits + string.punctuation + ' ')
        return data[index]

    def createDataset(self, prefix):
        self.__prefix = prefix
        gray = cv2.cvtColor(self.__template, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours.reverse()
        contours = contours[1:self.CLASS_COUNT + 1]
        self.__contours = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.__contours.append((x, y, w, h))
        self.__drawPreview()
        self.__loop()

    def __calculateContours(self):
        contours = []
        margin = self.MARGIN + self.__userMargin
        for x, y, w, h in self.__contours:
            x, y = x + margin, y + margin
            w, h = w - margin * 2, h - margin * 2
            contours.append((x, y, w, h))
        return contours

    def __drawPreview(self):
        preview = self.__img.copy()
        contours = self.__calculateContours()
        h, w = preview.shape[:2]
        factor = 1.0 / (float(h) / self.PREVIEW_HEIGHT)
        preview = cv2.resize(preview, (0, 0), fx=factor, fy=factor)
        for x, y, w, h in contours:
            x, y, w, h = tuple([int(factor * i) for i in (x, y, w, h)])
            cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 50, 255), 1)
        cv2.imshow("Dataset Reader", preview)

    def __loop(self):
        while True:
            k = cv2.waitKey(0) & 0xFF
            if k == self.KEY_ESC or k == ord('q'):
                break
            elif k == ord(' '):
                self.__createFiles()
                break
            elif k == self.KEY_UP:
                self.__userMargin -= 1
                self.__drawPreview()
            elif k == self.KEY_DOWN:
                self.__userMargin += 1
                self.__drawPreview()

    def __createFiles(self):
        folders = ocr.OCR.generateFolderList(ocr.OCR.DIGITS |
                                             ocr.OCR.LETTERS |
                                             ocr.OCR.SYMBOLS)
        contours = self.__calculateContours()
        for i, cnt in enumerate(contours):
            x, y, w, h = cnt
            folder = folders[self.getData(i)]
            path = common.generateFilename(folder, self.__prefix, ".bmp")
            item = self.__img[y:y+h, x:x+w]
            item = cv2.resize(item, (self.FINAL_SIZE, self.FINAL_SIZE))
            cv2.imshow("Dataset " + self.getData(i), item)
            if i >= 1:
                cv2.destroyWindow("Dataset " + self.getData(i - 1))
            if not self.__dryRun:
                print "Write " + path
                cv2.imwrite(path, item)
            else:
                print "Preview " + path

        

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description='Read a scanned dataset.')
    parser.add_argument("filename", help='The file to read')
    parser.add_argument("-p", "--prefix", help='Add a prefix to the filenames')
    parser.add_argument("--dry-run", action="store_true", help='Run without writing files')
    args = parser.parse_args()

    try:
        dr = DatasetReader(args.filename, args.dry_run)
    except (OSError, cv2.error) as err:
        print err
        sys.exit(1)

    print __doc__

    dr.createDataset(args.prefix)
    cv2.destroyAllWindows()
