# linux-photogrammetry-tools
A set of photogrammetry tools compiled for Ubuntu and containerized, fully open source and ready to use:

- SIFT* by [vlfeat.org](https://www.vlfeat.org/).
- [Bundler](https://github.com/snavely/bundler_sfm) (compiled w/Ceres Solver) by Noah Snavely.
- [CMVS \& PMVS2](https://github.com/pmoulon/CMVS-PMVS) by Yasutaka Furukawa.
- A patched version of Isaac Lenton's `bundler.py`:
  - Ported to Python 3.
  - Works with VLFeat SIFT (patch based on [Python Photogrammetry Toolbox](https://github.com/steve-vincent/photogrammetry) code).
  - Uses Ceres Solver by default.
  - Reads `CCD_WIDTHS` from a YAML file.
- An image resizer script that keeps EXIF metadata.
- A `Makefile` to run the pipeline steps.
- A Jupyter Notebook for point cloud meshing with [Open3D](https://github.com/intel-isl/Open3D).

> If you want to know more about how this software is packed [see here](https://github.com/epassaro/linux-photogrammetry-tools/blob/master/.github/workflows/release.yml).

> \* SIFT patent [expired on March 2020](https://patents.google.com/patent/US6711293B1/en).


## Installation

### Docker
Get the latest image:

`docker pull epassaro/linux-photogrammetry-tools:latest`

### Ubuntu 18.04
1. Get latest build from [releases section](https://github.com/epassaro/linux-photogrammetry-tools/releases) and extract it. 
2. Install the following dependencies via `apt`:
    
    `build-essential` `libjpeg62` `liblapack3` `libceres1` `jhead` `python3` `python3-pil` `python3-ruamel.yaml`

## Usage

### Docker
Usage via container is described in [DOCKER.md](https://github.com/epassaro/linux-photogrammetry-tools/blob/master/DOCKER.md).

### Ubuntu
To process the example dataset open a new terminal, go to the program folder and run `make`. 


## Options

The following options can be passed to `make` in the command line:

- IMG_DIR: *path*. Directory with a collection of images to be processed. Default: `examples/kermit`.
- RESIZE: *bool*. Resize pictures before processing. Default: `True`.
- MAX_SIZE: *int*. If RESIZE is `True`, maximum size in pixels (width or height). Default: `1200`.
- LOGFILE: *path*. Default: `log.txt`.


## Visualize results & post-processing

Results are stored under `<IMG_DIR>/output` folder.

### Open3D
To generate a 3D mesh from the point cloud with [Open3D](https://github.com/intel-isl/Open3D) you will need Anaconda or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system, and then create a new environment:

```
$ conda create -n open3d -c open3d-admin -c conda-forge open3d=0.12
```

Finally, run the notebook `gen_3d_mesh.ipynb` located at the `docs` folder.


### Meshlab
Open the `.ply` file located at `work_dir/pmvs/models/` with [Meshlab](http://www.meshlab.net/). You should visualize the point cloud clearly. To generate a textured mesh from point cloud, I recommend following the [Shubham Wagh's guide](https://gist.github.com/shubhamwagh/0dc3b8173f662d39d4bf6f53d0f4d66b).


## Known issues

1. `No CCD width available for camera`. 

    Only a small number of CCD widths are listed in `cfg/ccd_widths.yml`. 

    **Solution:** google your camera specs and add a new entry to the list.
    
> If your problem is not listed here please check the log file inside your `work_dir` directory and open a [new issue](https://github.com/epassaro/linux-photogrammetry-tools/issues/new).


## License
Code released under the [GNU GPLv3 License](https://raw.githubusercontent.com/epassaro/linux-photogrammetry-tools/master/LICENSE).
