# mksuper
Guide and Scripts to help unmake and make a super partition

These scripts assume you are on an ubuntu based distro. You may need to
adjust the scripts or run the commands individually on your machine to get the
desired results.

## Download your appropriate version of stock firmware.
## Titan Pocket
[tee](https://drive.google.com/file/d/1HZZ84TOGcj6zQcGn5_o1i0CW5GfI6H4D/view?usp=share_link)
[eea](https://drive.google.com/file/d/1bL0QO-rmMTnsEtEXYm6aetdXd-y8I19g/view?usp=share_link)
## Titan Slim
[tee](https://drive.google.com/file/d/16VHhHYQWZocxS1WzeEFCSRsBKH1G5cKN/view?usp=share_link)
[eea](https://drive.google.com/file/d/1Bpfi5Uf4dQf-YgSbmd-0WMRMWILyxgS8/view?usp=share_link)

## For those working on windows machines, you need to install WSL and an Ubuntu Image
See [here](https://gist.github.com/rumplestilzken/186d1aaebf2d3927ddfae6f7619e5780#file-installing-ubuntu-on-wsl)

## Download Repository
    git clone https://github.com/rumplestilzken/mksuper.git mksuper

## Setup Scripts
    chmod +x mksuper.sh install-dependencies.sh extract.sh

## Stock Rom
Place your downloaded stock rom in the mksuper directory.

## Place your gargoyle image in the mksuper directory
Copy your new bvN or bgN system image to the mksuper directory

## Run install-dependencies.sh
This will ask for your admin password, it is installing apt packages, inspect the script if you have an issue and run the commands yourself.

    ./install-dependencies.sh

## Run extract.sh
This will extract the super, system, vendor and product partitions, then copy them for update

    ./extract.sh

## mksuper
This will package the super.new.img for your device

    ./mksuper.sh
