#! /usr/bin/python3

import argparse
import glob
import os
from PIL import Image

MOD_PATH = os.path.dirname(__file__)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Resize photos keeping EXIF metadata")
    parser.add_argument('max_size', help='max size (width or height)', type=int)
    args = parser.parse_args()
    
    _ = [ os.rename(f, f.replace('JPG', 'jpg')) for f in glob.iglob(os.path.join(MOD_PATH, '*.JPG'))]
    fnames = [ f for f in glob.iglob(os.path.join(MOD_PATH, '*.jpg'))]
    
    for fname in fnames:
        
        im = Image.open(fname)
        exif = im.info['exif']
        
        im.thumbnail((args.max_size, args.max_size))
        im.save(fname, exif=exif)
