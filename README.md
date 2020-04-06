# linux-photogrammetry-tools
![build](https://github.com/epassaro/linux-photogrammetry-tools/workflows/build/badge.svg)

A set of photogrammetry tools compiled for Ubuntu 18.04 and ready to use:

- SIFT by [vlfeat.org](https://www.vlfeat.org/).
- [Bundler](https://github.com/snavely/bundler_sfm) (compiled with Ceres Solver) by Noah Snavely.
- [CMVS \& PMVS2](https://github.com/pmoulon/CMVS-PMVS) by Yasutaka Furukawa.
- A patched version of `bundler.py`:
  - Compatible with Python 2-3.
  - Works with VLFeat SIFT (based on [Python Photogrammetry Toolbox](https://github.com/steve-vincent/photogrammetry) code).
  - Uses Ceres Solver by default.
  - Reads `CCD_WIDTHS` from a YAML file.
- An image resizer script that keeps EXIF metadata.
- A `Makefile` to run the pipeline steps.

> If you want to know more about how this software is packed see [here](https://github.com/epassaro/linux-photogrammetry-tools/blob/master/.github/workflows/release.yml).


## Dependencies
Probably you have most of these dependencies already installed on your system:

`build-essential` `libjpeg62` `liblapack3` `libceres1` `jhead` `python` `python-pil` `python-ruamel.yaml`


## Download
Get latest build from [here](https://github.com/epassaro/linux-photogrammetry-tools/releases/download/stable/lpt-ubuntu-18.04.tar.gz) and extract it.


## Run example
`IMG_DIR` is set at the top of `Makefile` and pointing to the example folder by default.

Just run `make` in the terminal to process the images.


## Visualize the results & post-processing
Open with [Meshlab](http://www.meshlab.net/) the `.ply` file located at `work_dir/pmvs/models/`. You should visualize the point cloud clearly.

For post-processing I recommend following the [Shubham Wagh's guide](https://gist.github.com/shubhamwagh/0dc3b8173f662d39d4bf6f53d0f4d66b).


## Known issues
Check the log file inside `work_dir` directory in case of error.

1. `No CCD width available for camera`. 

    Only a small number of CCD widths are listed in `cfg/ccd_widths.yml`. 

    **Solution:** google your camera specs and add a new entry to the list.


## License

Code released under the [GNU GPLv3 License](https://raw.githubusercontent.com/epassaro/linux-photogrammetry-tools/master/LICENSE).
