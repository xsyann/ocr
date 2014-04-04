#!/usr/bin/env python
##
## generator.py for OCR
## 
## Made by xsyann
## Contact  <contact@xsyann.com>
## 
## Started on  Thu Apr  3 19:57:08 2014 xsyann
## Last update Thu Apr  3 20:58:50 2014 xsyann
##

"""
Create Dataset for OCR.

Authors:
        Nicolas PELICAN
        Yann KOETH
"""

import generator.creator as creator
import generator.reader as reader

def reader_keys():
    return """Dataset Reader Keys:
        UP    - Increase boxes size
        DOWN  - Decrease boxes
        SPACE - Write Dataset"""

def creator_keys():
    return """Dataset Creator Keys:
        Any Key - Write file
        DEL     - Remove the last written file
        SPACE   - Reset
        UP      - Increase brush size
        DOWN    - Decrease brush size
        ESC     - Exit"""

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description='OCR Dataset Creator.')
    parser.add_argument("-p", "--prefix", help='Add a prefix to the filename')
    parser.add_argument("filename", nargs='?', help='The file to read')
    parser.add_argument("--dry-run", action="store_true", help='Run without writing files')
    args = parser.parse_args()

    if not args.filename:
        print __doc__
        print creator_keys()
        creator = creator.DatasetCreator(args.prefix, args.dry_run)
        creator.run()
    else:
        try:
            dr = reader.DatasetReader(args.filename, args.dry_run)
        except (OSError, cv2.error) as err:
            print err
            sys.exit(1)
            
        print __doc__ 
        print reader_keys()
        dr.createDataset(args.prefix)
