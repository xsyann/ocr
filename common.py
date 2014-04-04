#!/usr/bin/env python
##
## common.py for OCR
## 
## Made by xsyann
## Contact  <contact@xsyann.com>
## 
## Started on  Fri Mar 28 15:09:44 2014 xsyann
## Last update Thu Apr  3 20:59:18 2014 xsyann
##

import os
import numpy as np
import cv2

def generateModelFilename(args, type):
    """Generate a model filename depending on flags."""
    opt = []
    if args.letters:
        opt.append('l')
    if args.symbols:
        opt.append('s')
    if args.digits:
        opt.append('d')
    opt.sort()
    return "models/model_{0}_{1}.yml".format(type, ''.join(opt))

def generateFilename(folder, prefix, ext):
    """Generate a filename in folder.
    folder/prefix-folder.0.ext
    """
    filename = os.path.basename(os.path.normpath(folder))
    if prefix:
        filename = "{0}-{1}".format(prefix, filename)
    path = getIncrementedFilename(os.path.join(folder, filename), ext)
    return path

def getIncrementedFilename(filename, ext):
    i = 0
    while os.path.isfile("{0}.{1}{2}".format(filename, i, ext)):
        i += 1
    return "{0}.{1}{2}".format(filename, i, ext)

class Brush(object):

    WINDOW_SIZE = 100

    def __init__(self, windowName):
        h, w = self.WINDOW_SIZE, self.WINDOW_SIZE
        self.__img = np.zeros((h, w, 3), np.uint8) 
        self.__img[:,:] = (255, 255, 255)
        self.__brushSize = 15
        self.windowName = windowName
        self.color = (0, 0, 0)
        self.show()

    def show(self):
        self.__img[:,:] = (255, 255, 255)
        pos = self.WINDOW_SIZE / 2
        cv2.line(self.__img, (pos, pos), (pos, pos), self.color, self.__brushSize)
        cv2.imshow(self.windowName, self.__img)

    @property
    def brushSize(self):
        return self.__brushSize

    @brushSize.setter
    def brushSize(self, brushSize):
        if 1 <= int(brushSize) <= self.WINDOW_SIZE:
            self.__brushSize = int(brushSize)
            self.show()

class Sketcher:
    def __init__(self, windowName, dest, brush):
        self.__prevPt = None
        self.__windowName = windowName
        self.__dest = dest
        self.__brush = brush
        self.__dirty = False
        self.show()
        cv2.setMouseCallback(self.__windowName, self.onMouse)

    @property
    def sketch(self):
        return self.__dest

    def show(self):
        cv2.imshow(self.__windowName, self.__dest)

    def reset(self):
        self.__dest[:,:] = (255, 255, 255) 

    def onMouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__prevPt = pt
        if self.__prevPt and flags & cv2.EVENT_FLAG_LBUTTON:
            cv2.line(self.__dest, self.__prevPt, pt, self.__brush.color, self.__brush.brushSize)
            self.__dirty = True
            self.__prevPt = pt
            self.show()
        else:
            self.prevPt = None
