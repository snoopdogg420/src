Client Build Preparation
========================
The first step in building a distributable Toontown Infinite client is building ```GameData.bin```. ```GameData.bin``` is an encrypted blob of frozen Python code. It contains all of the code necessary to run the game. There are three steps to building this file:

* Prepare for building
* Build the frozen Python module
* Encrypt the frozen Python module

This document outlines how to accomplish the first task.

- - -

Preparing the client for building is quite simple when using the ```prepare_client.py``` utility. What it does is it creates a build directory with all of the necessary files for running a client. All server-specific files get removed. Next, it removes all ```__debug__``` blocks from the code, and they may pose a security risk, or be developer specific. After that, a file called ```game_data.py``` is generated. This file contains the PRC file data, (stripped) DC file, and time zone info. If a ```REVISION``` token was provided in the ```--server-ver``` option, it gets replaced in the PRC file data with the first 7 characters of the GitHub revision. Finally, if ```--build-mfs``` is provided, any phase files that were modified get compiled.

## Usage ##

    usage: prepare_client.py [-h] [--distribution DISTRIBUTION]
                             [--build-dir BUILD_DIR] [--src-dir SRC_DIR]
                             [--server-ver SERVER_VER] [--build-mfs]
                             [--resources-dir RESOURCES_DIR]
                             [modules [modules ...]]
    
    positional arguments:
      modules               The Toontown Infinite modules to be included in the
                            build.
    
    optional arguments:
      -h, --help            show this help message and exit
      --distribution DISTRIBUTION
                            The distribution token.
      --build-dir BUILD_DIR
                            The directory in which to store the build files.
      --src-dir SRC_DIR     The directory of the Toontown Infinite source code.
      --server-ver SERVER_VER
                            The server version of this build. REVISION tokens will
                            be replaced with the current Git revision string.
      --build-mfs           When present, multifiles will be built.
      --resources-dir RESOURCES_DIR
                            The directory of the Toontown Infinite resources.

## Example ##

    ppython -m prepare_client --distribution devdist --build-dir build --src-dir ..
                              --server-ver infinite-REVISION --build-mfs
                              --resources-dir ../resources otp toontown
