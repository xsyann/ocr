#!/usr/bin/env python
##
## test.py for OCR
##
## Made by xsyann
## Contact  <contact@xsyann.com>
##
## Started on  Fri Mar 28 15:09:44 2014 xsyann
## Last update Fri Apr  4 16:36:43 2014 xsyann
##

"""
OCR Test.

Authors:
        Nicolas PELICAN
        Yann KOETH

Keys:
  SPACE - Test
  r     - reset
  UP    - Increase brush size
  DOWN  - Decrease brush size
  ESC   - exit
"""

import os
import string
import numpy as np
import cv2
import common
import subprocess
from common import Sketcher, Brush
from ocr import OCR

class TestOCR:

    ESC = 27
    KEY_UP = 0
    KEY_DOWN = 1

    def __init__(self, model, filenames, flags, pattern):
        self.ocr = OCR(OCR.MODEL_ANN, model, flags)
        if filenames:
            counter = {}
            for filename in filenames:
                ch = self.ocr.charFromFile(filename)
                if pattern:
                    label = self.__exec(pattern, filename)
                    if label in counter:
                        predicted, total = counter[label]
                        counter[label] = (predicted + int(label == ch), total + 1)
                    else:
                        counter[label] = (int(label == ch), 1)
                print "%s in %s" % (ch, filename)
            if pattern:
                self.__analyze(counter)
        else:
            h, w = 200, 200
            img = np.zeros((h, w, 3), np.uint8)
            img[:,:] = (255, 255, 255)
            self.brush = Brush("Brush")
            self.sketcher = Sketcher('Test OCR', img, self.brush)

    def __analyze(self, counter):
        print ""
        totalPercent = []
        for label, (predicted, total) in sorted(counter.iteritems()):
            percent = int(float(predicted) / total * 100)
            totalPercent.append(percent)
            print "{0}\t{1} / {2} - {3} %".format(label, predicted, total, percent)
        print "\nTotal recognized : {0:.1f} %\n".format(np.mean(totalPercent))

    def __exec(self, file, arg):
        out = subprocess.Popen([file, arg], stdout=subprocess.PIPE).communicate()[0]
        return out

    def __displayResponse(self, ch):
        response = np.zeros((75, 75, 3), np.uint8)
        response[:,:] = (255, 255, 255)
        cv2.putText(response, ch, (15, 35), cv2.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 0), 1)
        cv2.imshow("Response", response)

    def run(self):
        while True:
            k = cv2.waitKey(0) & 0xFF
            if k == self.ESC:
                break
            elif k == ord('r'):
                self.sketcher.reset()
                self.sketcher.show()
            elif k == ord(' '):
                ch = self.ocr.charFromImage(self.sketcher.sketch)
                self.sketcher.show()
                self.sketcher.reset()
                self.__displayResponse(ch)
                print "OCR : %s" % ch
            elif k == self.KEY_UP:
                self.brush.brushSize += 1
            elif k == self.KEY_DOWN:
                self.brush.brushSize -= 1


if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description='Test OCR.')
    parser.add_argument('-l', dest='letters', action='store_true', help='Recognize letters')
    parser.add_argument('-s', dest='symbols', action='store_true', help='Recognize symbols')
    parser.add_argument('-d', dest='digits', action='store_true', help='Recognize digits')
    parser.add_argument('-p', '--pattern', help='Pattern to extract label from filename')
    parser.add_argument("filename", nargs='*', help='Image to recognize')
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
        sys.exit(1)

    try:
        test = TestOCR(common.generateModelFilename(args, OCR.MODEL_ANN), args.filename, flags, args.pattern)
    except (OSError, cv2.error) as err:
        print err
        sys.exit(1)

    if not args.filename:
        print __doc__
        test.run()
        cv2.destroyAllWindows()
