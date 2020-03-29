# Usage on Docker

## Process images

To process a set of images located in a folder on the host system, open a terminal and run:

```
docker run --rm -v <PATH_TO_LOCAL_FOLDER>:/tmp epassaro/linux-photogrammetry-tools:latest make IMG_DIR=/tmp
```

> Notice you still need to do post-processing outside the container as described in [README.md](https://github.com/epassaro/linux-photogrammetry-tools/blob/master/README.md).


## Debug

To run a `bash` session inside the container:
 
```
docker run --rm -ti epassaro/linux-photogrammetry-tools:latest
```

If you need to share files between the host and the container prepend the `-v <PATH_TO_LOCAL_FOLDER>:/tmp` option.


## Remove image

```
docker image ls
docker rmi -f <IMAGE_ID>
```
