# linux-photogrammetry-tools
![build](https://github.com/epassaro/linux-photogrammetry-tools/workflows/build/badge.svg)

A set of photogrammetry tools compiled for Ubuntu 18.04 and ready to use:

- [Bundler](https://github.com/snavely/bundler_sfm) by Noah Snavely
- [CMVS \& PMVS2](https://github.com/pmoulon/CMVS-PMVS) by Yasutaka Furukawa


## Download
Get latest build from [here](https://github.com/epassaro/linux-photogrammetry-tools/releases/download/stable/lpt-ubuntu-18.04.tar.gz).


## Dependencies
Probably you have most of these dependencies already installed on your system:

`build-essential` `libc6-i386` `libjpeg62` `liblapack3` `python` `python-pil`


## Install SIFT
Due to license restrictions David Lowe's SIFT feature extractor is not included. You must install it by running the script:

`$ ./install-sift.sh`


## Run example
`IMG_DIR` is set at the top of `Makefile` and pointing to the example folder by default. Just run `make` in the terminal to process the images.


## Visualize the results
Open with [Meshlab](http://www.meshlab.net/) the `.ply` file located at `work_dir/pmvs/models/`.
