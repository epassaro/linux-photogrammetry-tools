# linux-photogrammetry-tools
![build](https://github.com/epassaro/linux-photogrammetry-tools/workflows/build/badge.svg)

A set of photogrammetry tools compiled for Ubuntu 18.04, fully open source and ready to use:

- SIFT* by [vlfeat.org](https://www.vlfeat.org/).
- [Bundler](https://github.com/snavely/bundler_sfm) (compiled with Ceres Solver) by Noah Snavely.
- [CMVS \& PMVS2](https://github.com/pmoulon/CMVS-PMVS) by Yasutaka Furukawa.
- A patched version of Isaac Lenton's `bundler.py`:
  - Compatible with Python 2-3.
  - Works with VLFeat SIFT (patch based on [Python Photogrammetry Toolbox](https://github.com/steve-vincent/photogrammetry) code).
  - Uses Ceres Solver by default.
  - Reads `CCD_WIDTHS` from a YAML file.
- An image resizer script that keeps EXIF metadata.
- A `Makefile` to run the pipeline steps.

> If you want to know more about how this software is packed [see here](https://github.com/epassaro/linux-photogrammetry-tools/blob/master/.github/workflows/release.yml).

> \* SIFT patent [expired on March 2020](https://patents.google.com/patent/US6711293B1/en).


## Dependencies
`build-essential` `libjpeg62` `liblapack3` `libceres1` `jhead` `python` `python-pil` `python-ruamel.yaml`


## Download
Get latest build [from here](https://github.com/epassaro/linux-photogrammetry-tools/releases/download/latest/lpt-ubuntu-18.04.tar.gz) and extract it.


## Run example
Open a new terminal, go to the program folder and run `make` to process the Kermit dataset.


## Options

You can edit the following parameters at the top of `Makefile`.

- IMG_DIR: *path*. Directory with a collection of images to be processed. Default: `examples/kermit`.
- RESIZE: *bool*. Resize pictures before processing. Default: `True`.
- MAX_SIZE: *int*. If RESIZE is `True`, maximum size in pixels (width or height). Default: `1200`.
- LOGFILE: *path*. Default: `log.txt`.


## Visualize the results & post-processing
Open the `.ply` file located at `work_dir/pmvs/models/` with [Meshlab](http://www.meshlab.net/) or [CloudCompare](https://www.danielgm.net/cc/). You should visualize the point cloud clearly.

To generate a textured mesh from point cloud with Meshlab, I recommend following the [Shubham Wagh's guide](https://gist.github.com/shubhamwagh/0dc3b8173f662d39d4bf6f53d0f4d66b).


## Known issues
Check the log file inside `work_dir` directory in case of error.

1. `No CCD width available for camera`. 

    Only a small number of CCD widths are listed in `cfg/ccd_widths.yml`. 

    **Solution:** google your camera specs and add a new entry to the list.


## License

Code released under the [GNU GPLv3 License](https://raw.githubusercontent.com/epassaro/linux-photogrammetry-tools/master/LICENSE).
