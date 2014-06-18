#!/usr/bin/env python
##
## creator.py for OCR
##
## Made by xsyann
## Contact  <contact@xsyann.com>
##
## Started on  Fri Mar 28 15:09:44 2014 xsyann
## Last update Thu Apr  3 20:44:34 2014 xsyann
##

"""
OCR Dataset Creator.

Authors:
        Nicolas PELICAN
        Yann KOETH

Keys:
        Any Key - Write file
        DEL     - Remove the last written file
        RET     - Reset
        UP      - Increase brush size
        DOWN    - Decrease brush size
        ESC     - Exit
"""

import sys
import os
import string
import numpy as np
import cv2
import common
from ocr import OCR
from common import Sketcher, Brush

class DatasetCreator:

    ESC = 27
    DEL = 127
    RET = 13
    KEY_UP = 0
    KEY_DOWN = 1
    EXT = ".bmp"
    FINAL_SIZE = 50

    def __init__(self, prefix, dryRun):
        h, w = 300, 300
        img = np.zeros((h, w, 3), np.uint8)
        img[:,:] = (255, 255, 255)
        self.brush = Brush("Brush")
        self.sketcher = Sketcher("Dataset Creator", img, self.brush)
        self.__folders = OCR.generateFolderList(OCR.DIGITS | OCR.LETTERS | OCR.SYMBOLS)
        self.__prefix = prefix
        self.__lastFile = None
        self.__dryRun = dryRun

    def run(self):
        while True:
            k = cv2.waitKey(0) & 0xFF

            if k == self.ESC:
                break
            elif k == self.RET:
                self.sketcher.reset()
                self.sketcher.show()
            elif k == self.KEY_UP:
                self.brush.brushSize += 1
            elif k == self.KEY_DOWN:
                self.brush.brushSize -= 1
            elif k == self.DEL and not self.__dryRun:
                if self.__lastFile:
                    os.remove(self.__lastFile)
                    self.__lastFile = None
                    print path + " Removed"
            elif chr(k) in self.__folders:
                folder = self.__folders[chr(k)]
                path = common.generateFilename(folder, self.__prefix, self.EXT)
                item = self.sketcher.sketch.copy()
                item = cv2.resize(item, (self.FINAL_SIZE, self.FINAL_SIZE))
                cv2.imshow("Generated Dataset item", item)
                self.sketcher.reset()
                self.__lastFile = path
                if not self.__dryRun:
                    cv2.imwrite(path, item)
                    print path + " Written"
                else:
                    print path + " Preview"

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description='OCR Dataset Creator.')
    parser.add_argument("-p", "--prefix", help='Add a prefix to the filename')
    parser.add_argument("--dry-run", action="store_true", help='Run without writing files')
    args = parser.parse_args()

    print __doc__

    creator = DatasetCreator(args.prefix, args.dry_run)
    creator.run()
    cv2.destroyAllWindows()
