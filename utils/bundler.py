#! /usr/bin/python3
# #### BEGIN LICENSE BLOCK ####
#
# bundler.py - Python convenience module for running Bundler.
# Copyright (C) 2013 Isaac Lenton (aka ilent2)
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# #### END LICENSE BLOCK ####

import argparse
import gzip
import os
import sys
import glob
import subprocess
import tempfile
from multiprocessing import Pool
from PIL import Image, ExifTags
from ruamel.yaml import YAML

VERSION = "Bundler 0.4"
DESCRIPTION = """\
Python convenience module to process a series of images and reconstruct
the scene using Bundler.

Bundler is a structure-from-motion system for unordered image
collections (for instance, images from the Internet). Bundler takes a
set of images, image features, and image matches as input, and
produces a 3D reconstruction of the camera and (sparse) scene geometry
as output."""

# This module replaces the existing RunBundler.sh script with a more
# cross platform implementation.  Additional elements replaced:
#   - RunBundler.sh             2008-2013 Noah Snavely
#   - ToSift.sh
#   - extract_focal.pl          2005-2009 Noah Snavely
#   - jhead

MOD_PATH = os.path.dirname(__file__)
BIN_PATH = os.path.join(MOD_PATH, "../bin")
LIB_PATH = os.path.join(MOD_PATH, "../lib")
CFG_PATH = os.path.join(MOD_PATH, "../cfg")
BIN_SIFT = None
BIN_BUNDLER = None
BIN_MATCHKEYS = None

yaml = YAML()
with open(os.path.join(CFG_PATH, "ccd_widths.yml"), 'r') as f:
    CCD_WIDTHS = yaml.load(f)

def get_images():
    """Searches the present directory for JPEG images."""
    images = glob.glob("./*.[jJ][pP][gG]")
    if len(images) == 0:
        error_str = ("Error: No images supplied!  "
                     "No JPEG files found in directory!")
        raise Exception(error_str)
    return images

def extract_focal_length(images=[], scale=1.0, verbose=False):
    """Extracts (pixel) focal length from images where available.
    The functions returns a dictionary of image, focal length pairs.
    If no focal length is extracted for an image, the second pair is None.
    """
    if len(images) == 0:
        if verbose: print("[- Creating list of images -]")
        images = get_images()

    ret = {}
    for image in images:
        if verbose: print("[Extracting EXIF tags from image {0}]".format(image))

        tags = {}
        with open(image, 'rb') as fp:
            img = Image.open(fp)
            if hasattr(img, '_getexif'):
                exifinfo = img._getexif()
                if exifinfo is not None:
                    for tag, value in exifinfo.items():
                        tags[ExifTags.TAGS.get(tag, tag)] = value

        ret[image] = None

        # Extract Focal Length
        focalN, focalD = tags.get('FocalLength', (0, 1))
        focal_length = float(focalN)/float(focalD)

        # Extract Resolution
        img_width = tags.get('ExifImageWidth', 0)
        img_height = tags.get('ExifImageHeight', 0)
        if img_width < img_height:
            img_width,img_height = img_height,img_width



        # Extract CCD Width (Prefer Lookup Table)
        ccd_width = 1.0
        make_model = tags.get('Make', '') + ' ' + tags.get('Model', '')
        if make_model.strip() in CCD_WIDTHS:
            ccd_width = CCD_WIDTHS[make_model.strip()]
        else:
            fplaneN, fplaneD = tags.get('FocalPlaneXResolution', (0, 1))
            if fplaneN != 0:
                ccd_width = 25.4*float(img_width)*float(fplaneD)/float(fplaneN)
                if verbose: print("  [Using CCD width from EXIF tags]")
            else:
                ccd_width = 0

        if verbose:
            print("  [EXIF focal length = {0}mm]".format(focal_length))
            print("  [EXIF CCD width = {0}mm]".format(ccd_width))
            print("  [EXIF resolution = {0} x {1}]".format(
                img_width, img_height))
            if ccd_width == 0:
                print("  [No CCD width available for camera {0}]".format(
                    make_model))

        if (img_width==0 or img_height==0 or focalN==0 or ccd_width==0):
            if verbose: print("  [Could not determine pixel focal length]")
            continue

        # Compute Focal Length in Pixels
        ret[image] = img_width * (focal_length / ccd_width) * scale
        if verbose: print("  [Focal length (pixels) = {0}]".format(ret[image]))

    return ret

def sift_image(image, verbose=False):
    """Extracts SIFT features from a single image.  See sift_images."""
    global BIN_SIFT, BIN_PATH

    if BIN_SIFT is None:
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            BIN_SIFT = os.path.join(BIN_PATH, "siftWin32.exe")
        else:
            BIN_SIFT = os.path.join(BIN_PATH, "sift")

    pgm_filename = image.rsplit('.', 1)[0] + ".pgm"
    key_filename = image.rsplit('.', 1)[0] + ".key"

    # Convert image to PGM format (grayscale)
    with open(image, 'rb') as fp_img:
        image = Image.open(fp_img)
        image.convert('L').save(pgm_filename)
        
    # Add lib folder to LD_LIBRARY_PATH
    env = dict(os.environ)
    if 'LD_LIBRARY_PATH' in env:
        env['LD_LIBRARY_PATH'] = env['LD_LIBRARY_PATH'] + ':' + LIB_PATH
    else:
        env['LD_LIBRARY_PATH'] = LIB_PATH

    # Extract SIFT data
    if verbose:
        subprocess.call([BIN_SIFT, "-v", "-o", key_filename, pgm_filename], env=env)
    else:
        subprocess.call([BIN_SIFT, "-o", key_filename, pgm_filename], env=env)

    # Remove pgm file
    os.remove(pgm_filename)

    # GZIP compress key file (and remove)
    with open(key_filename, 'rt') as fp_in:
        with gzip.open(key_filename + ".gz", 'wt') as fp_out:
            featureStrings = fp_in.readlines()
            numFeatures = len(featureStrings)
            fp_out.write("%s 128\n" % numFeatures)
            
            for featureString in featureStrings:
                features = featureString.split()
                # swap features[0] and features[1]
                tmp = features[0]
                features[0] = features[1]
                features[1] = tmp
                i1 = 0
                for i2 in (4,24,44,64,84,104,124,132):
                    fp_out.write("%s\n" % " ".join(features[i1:i2]))
                    i1 = i2
                    
    os.remove(key_filename)

    return key_filename

def sift_images(images, verbose=False, parallel=True):
    """Extracts SIFT features from images in 'images'.

    'images' should be a list of file names.  The function creates a
    SIFT compressed key file for each image in 'images' with a '.key.gz'
    extension.  A list of the uncompressed key file names is returned.

    If 'parallel' is True, the function executes SIFT in parallel.
    """
    global BIN_SIFT, BIN_PATH

    key_filenames = []

    if BIN_SIFT is None:
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            BIN_SIFT = os.path.join(BIN_PATH, "siftWin32.exe")
        else:
            BIN_SIFT = os.path.join(BIN_PATH, "sift")
        
    if parallel:
        pool = Pool()
        key_filenames = pool.map(sift_image, images)
    else:
        for image in images:
            key_filenames.append(sift_image(image, verbose=verbose))

    return key_filenames

def match_images(key_files, matches_file, verbose=False):
    "Executes KeyMatchFull to match key points in images."""
    global BIN_MATCHKEYS, BIN_PATH

    if BIN_MATCHKEYS is None:
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            BIN_MATCHKEYS = os.path.join(BIN_PATH, "KeyMatchFull.exe")
        else:
            BIN_MATCHKEYS = os.path.join(BIN_PATH, "KeyMatchFull")

    keys_file = ""
    with tempfile.NamedTemporaryFile(delete=False, mode='wt') as fp:
        for key in key_files:
            fp.write(key + '\n')
        keys_file = fp.name

    # Add lib folder to LD_LIBRARY_PATH
    env = dict(os.environ)
    if 'LD_LIBRARY_PATH' in env:
        env['LD_LIBRARY_PATH'] = env['LD_LIBRARY_PATH'] + ':' + LIB_PATH
    else:
        env['LD_LIBRARY_PATH'] = LIB_PATH

    if verbose:
        subprocess.call([BIN_MATCHKEYS, keys_file, matches_file], env=env)
    else:
        with open(os.devnull, 'w') as fp_out:
            subprocess.call([BIN_MATCHKEYS, keys_file, matches_file],
                            stdout=fp_out, env=env)
            
    os.remove(keys_file)

def bundler(image_list=None, options_file=None, shell=False, *args, **kwargs):
    """Run bundler, parsing arguments from args and kwargs through.
    For Bundler usage run bundler("--help").

    image_list : File containing list of images.
    options_file : Specify an options file for bundler (optional).
    shell : Enable full shell support for parsing args (default: False).
    """
    global BIN_BUNDLER, BIN_PATH

    if BIN_BUNDLER is None:
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            BIN_BUNDLER = os.path.join(BIN_PATH, "Bundler.exe")
        else:
            BIN_BUNDLER = os.path.join(BIN_PATH, "bundler")

    def kwargs_bool(b, r):
        if b: return r
        else: return []

    kwargs_dict = {
        'match_table'            : lambda k,v: ['--'+k,v],
        'output'                 : lambda k,v: ['--'+k,v],
        'output_all'             : lambda k,v: ['--'+k,v],
        'output_dir'             : lambda k,v: ['--'+k,v],
        'variable_focal_length'  : lambda k,v: kwargs_bool(v, ['--'+k]),
        'use_focal_estimate'     : lambda k,v: kwargs_bool(v, ['--'+k]),
        'constrain_focal'        : lambda k,v: kwargs_bool(v, ['--'+k]),
        'constrain_focal_weight' : lambda k,v: ['--'+k, str(v)],
        'estimate_distortion'    : lambda k,v: kwargs_bool(v, ['--'+k]),
        'run_bundle'             : lambda k,v: kwargs_bool(v, ['--'+k]),
        'use_ceres'              : lambda k,v: kwargs_bool(v, ['--'+k]),
    }

    str_args = [a for a in args if type(a) == str]
    for k,v in kwargs.items():
        if not k in kwargs_dict: continue
        str_args.extend(kwargs_dict[k](k,v))

    if len(str_args) != 0 and options_file is not None:
        with open(options_file, 'wt') as fp:
            for o in str_args:
                if o.startswith('--'): fp.write('\n')
                else: fp.write(' ')
                fp.write(o)

    image_list_file = ""
    if type(image_list) == dict:
        with tempfile.NamedTemporaryFile(delete=False, mode='wt') as fp:
            for image,value in image_list.items():
                if value == None: fp.write(image + '\n')
                else: fp.write(' '.join([image, '0', str(value), '\n']))
            image_list_file = fp.name
    elif type(image_list) == str:
        image_list_file = image_list
    else:
        raise Exception("Error: Not a valid list or filename for image_list!")

    # Add lib folder to LD_LIBRARY_PATH
    env = dict(os.environ)
    if 'LD_LIBRARY_PATH' in env:
        env['LD_LIBRARY_PATH'] = env['LD_LIBRARY_PATH'] + ':' + LIB_PATH
    else:
        env['LD_LIBRARY_PATH'] = LIB_PATH

    try:    os.mkdir("bundle")
    except: pass

    with open(os.path.join("bundle", "out"), 'wt') as fp_out:
        if options_file is not None:
            subprocess.call([BIN_BUNDLER, image_list_file, "--options_file",
                options_file], shell=shell, env=env, stdout=fp_out)
        else:
            subprocess.call([BIN_BUNDLER, image_list_file] + str_args,
                shell=shell, env=env, stdout=fp_out)

    if type(image_list) == dict:
        os.remove(image_list_file)

def run_bundler(images=[], verbose=False, parallel=True):
    """Prepare images and run bundler with default options."""
    # Create list of images
    if len(images) == 0:
        if verbose: print("[- Creating list of images -]")
        images = get_images()

    # Extract focal length
    if type(images) == list:
        if verbose: print("[- Extracting EXIF tags from images -]")
        images = extract_focal_length(images, verbose=verbose)

    # Extract SIFT features from images
    if verbose: print("[- Extracting keypoints -]")
    key_files = sift_images(images, parallel=parallel, verbose=verbose)

    # Match images
    if verbose: print("[- Matching keypoints (this can take a while) -]")
    matches_file = "matches.init.txt"
    match_images(key_files, matches_file, verbose=verbose)

    # Run Bundler
    if verbose: print("[- Running Bundler -]")
    bundler(image_list=images,
            options_file="options.txt",
            verbose=verbose,
            match_table=matches_file,
            output="bundle.out",
            output_all="bundle_",
            output_dir="bundle",
            variable_focal_length=True,
            use_focal_estimate=True,
            constrain_focal=True,
            constrain_focal_weight=0.0001,
            estimate_distortion=True,
            run_bundle=True,
            use_ceres=True)

    if verbose: print("[- Done -]")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-v', '--verbose', action='store_true',
        help="generate additional output in execution", default=False)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--no-parallel', action='store_true',
        help="disable parallelisation", default=False)
    parser.add_argument('--extract-focal', action='store_true',
        help="only create list of images to be reconstructed", default=False)
    args = parser.parse_args()

    if args.extract_focal:
        images = extract_focal_length(verbose=args.verbose)
        with open("list.txt", 'w') as fp:
            for image,value in images.items():
                if value == None: fp.write(image + '\n')
                else: fp.write(' '.join([image, '0', str(value), '\n']))
    else:
        run_bundler(verbose=args.verbose, parallel=not args.no_parallel)

