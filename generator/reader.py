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
        RIGHT - Increase image size
        LEFT  - Decrease image size
        w     - Move up
        a     - Move left
        s     - Move down
        d     - Move right
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
    MARGIN_STEP = 1
    PREVIEW_HEIGHT = 850
    FINAL_SIZE = 50
    RESIZE_STEP = 0.01
    MOVE_STEP = 5

    KEY_ESC = 27
    KEY_UP = 0
    KEY_DOWN = 1
    KEY_LEFT = 2
    KEY_RIGHT = 3

    def __init__(self, filename, dryRun):

        if not os.path.isfile(filename):
            raise OSError(2, 'File not found', filename)

        self.__userMargin = 0
        self.__resizeFactor = 1.0
        self.__dryRun = dryRun
        self.__offset = (0, 0)
        cv2.namedWindow("Dataset Reader")
        templatePath = os.path.join(os.path.dirname(__file__), self.TEMPLATE)
        self.__template = cv2.imread(templatePath)
        self.__img = cv2.imread(filename)
        h, w = self.__img.shape[:2]
        tH, tW = self.__template.shape[:2]
        factor = 1.0 / (((tW / float(w)) + (tH / float(h))) / 2.0)
        self.__template = cv2.resize(self.__template, (0, 0), fx=factor, fy=factor)

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

    def __getContours(self):
        contours = []
        margin = self.MARGIN + self.__userMargin
        for x, y, w, h in self.__contours:
            x, y = x + margin, y + margin
            w, h = w - margin * 2, h - margin * 2
            contours.append((x, y, w, h))
        return contours

    def __mergeImages(self, frame, content, offset):
        """Merge content into frame with offset.
        """
        frameH, frameW = frame.shape[:2]
        contentH, contentW = content.shape[:2]
        x, y = (frameW - contentW) / 2 + offset[0], (frameH - contentH) / 2 + offset[1]
        if x > frameW or y > frameH or x < -contentW or y < -contentH:
            return frame
        frameX, frameY = max(min(x, frameW), 0), max(min(y, frameH), 0)
        contentX, contentY = -min(0, x), -min(0, y)
        sizeX, sizeY = contentW, contentH
        if x < 0:
            sizeX = contentW + x
        if x + contentW > frameW:
            sizeX = frameW - x
        if y < 0:
            sizeY = contentH + y
        if y + contentH > frameH:
            sizeY = frameH - y
        frame[frameY:frameY+sizeY, frameX:frameX+sizeX] = content[contentY:contentY+sizeY, contentX:contentX+sizeX]
        return frame

    def __getPreviewImage(self, preview, resize=True):
        h, w = preview.shape[:2]
        # User resize
        resizeFactor = self.__resizeFactor
        preview = cv2.resize(preview, (0, 0), fx=resizeFactor, fy=resizeFactor)
        # Frame
        frame = np.zeros((h, w, 3), np.uint8)
        frame[:h,:w] = (255, 255, 255)
        frame = self.__mergeImages(frame, preview, self.__offset)
        # Resize To Fit Screen
        if resize:
            factor = 1.0 / (float(h) / self.PREVIEW_HEIGHT)
            frame = cv2.resize(frame, (0, 0), fx=factor, fy=factor)
        return frame

    def __drawPreview(self):
        preview = self.__getPreviewImage(self.__img.copy())
        contours = self.__getContours()
        h, w = self.__img.shape[:2]
        factor = 1.0 / (float(h) / self.PREVIEW_HEIGHT)
        for x, y, w, h in contours:
            # Resize contours to preview size
            x, y, w, h = tuple([int(i * factor) for i in (x, y, w, h)])
            cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 50, 255), 1)
        cv2.imshow("Dataset Reader", preview)

    def __move(self, k):
        if k == ord('a'):
            x, y = self.__offset
            self.__offset = (x - self.MOVE_STEP, y)
            self.__drawPreview()
        elif k == ord('d'):
            x, y = self.__offset
            self.__offset = (x + self.MOVE_STEP, y)
            self.__drawPreview()
        elif k == ord('w'):
            x, y = self.__offset
            self.__offset = (x, y - self.MOVE_STEP)
            self.__drawPreview()
        elif k == ord('s'):
            x, y = self.__offset
            self.__offset = (x, y + self.MOVE_STEP)
            self.__drawPreview()

    def __resize(self, k):
        if k == self.KEY_UP:
            self.__userMargin -= self.MARGIN_STEP
            self.__drawPreview()
        elif k == self.KEY_DOWN:
            self.__userMargin += self.MARGIN_STEP
            self.__drawPreview()
        elif k == self.KEY_LEFT:
            self.__resizeFactor -= self.RESIZE_STEP
            self.__resizeFactor = max(self.__resizeFactor, 0.1)
            self.__drawPreview()
        elif k == self.KEY_RIGHT:
            self.__resizeFactor += self.RESIZE_STEP
            self.__resizeFactor = min(self.__resizeFactor, 1)
            self.__drawPreview()

    def __loop(self):
        while True:
            k = cv2.waitKey(0) & 0xFF
            if k == self.KEY_ESC or k == ord('q'):
                break
            elif k == ord(' '):
                self.__createFiles()
                break
            self.__move(k)
            self.__resize(k)

    def __createFiles(self):
        folders = ocr.OCR.generateFolderList(ocr.OCR.DIGITS |
                                             ocr.OCR.LETTERS |
                                             ocr.OCR.SYMBOLS)
        preview = self.__getPreviewImage(self.__img.copy(), resize=False)
        contours = self.__getContours()
        for i, cnt in enumerate(contours):
            x, y, w, h = cnt
            folder = folders[self.getData(i)]
            path = common.generateFilename(folder, self.__prefix, ".bmp")
            item = preview[y:y+h, x:x+w]
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
