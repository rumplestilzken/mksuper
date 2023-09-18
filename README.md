# mksuper
Guide and Scripts to help unmake and make a super partition

These scripts assume you are on an ubuntu based distro. You may need to
adjust the scripts or run the commands individually on your machine to get the
desired results.

Requires python3

## Supported Devices
* Titan Pocket
* Titan Slim
* Jelly 2E
* Atom L
* Tank

## Supported Image Formats
* .img
* .img.tar.gz
* .img.xz

## Download your appropriate version of stock firmware.
See [here](http://rumplestilzken.com:14005/Unihertz/StockResources)

## For those working on windows machines, you need to install WSL and an Ubuntu Image
See [here](https://gist.github.com/rumplestilzken/186d1aaebf2d3927ddfae6f7619e5780#file-installing-ubuntu-on-wsl)

## Download Repository
    git clone https://github.com/rumplestilzken/mksuper.git mksuper

## Stock Rom
Place your downloaded stock rom in the mksuper directory.

## Place your gargoyle image in the mksuper directory
Copy your new system image or archive into the mksuper directory

## Run install-dependencies.py
This will ask for your admin password, it is installing apt packages, inspect the script if you have an issue and run the commands yourself.

    python install-dependencies.py

## Run extract.py
This will extract the super, system, vendor and product partitions, then copy them for update

    python extract.py

## mksuper
This will package the super.new.img for your device

    python mksuper.py
