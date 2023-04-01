#!/usr/bin/env python3

import subprocess
import os
from zipfile import ZipFile
import shutil

def main():
    here = os.path.dirname(os.path.realpath(__file__))
    stock_rom_path=""
    gargoyle_rom_path = ""

    for file in os.listdir(here):
        if file.endswith(".zip"):
            stock_rom_path=file
        if file.endswith(".img"):
            gargoyle_rom_path=file

    if stock_rom_path == "":
        print("No Stock Rom Found.")
        quit()
    else:
        print("Stock Rom Found:'" + stock_rom_path + "'")

    if gargoyle_rom_path == "":
        print("No gargoyle system image Found.")
        quit()
    else:
        print("gargoyle system image Found:'" + gargoyle_rom_path + "'")

    stock_rom_folder=os.path.splitext(stock_rom_path)[0]

    print("Unzipping Stock rom to " + stock_rom_folder)
    with ZipFile(stock_rom_path) as zObject:
        zObject.extract(stock_rom_folder + "/super.img", here)
        zObject.extract(stock_rom_folder+"/vbmeta.img",  here)
        zObject.extract(stock_rom_folder+"/vbmeta_system.img",  here)
        zObject.extract(stock_rom_folder+"/vbmeta_vendor.img", here)
    zObject.close();

    try:
        os.mkdir(here + "/super")
    except OSError as error:
        error

    try:
        os.mkdir(here + "/super/stock")
    except OSError as error:
        error
    try:
        os.mkdir(here + "/super/custom")
    except OSError as error:
        error

    print("Copying super to super/stock")
    shutil.copyfile(here + "/" + stock_rom_folder + "/super.img", here + "/super/stock/super.img")

    print("Unpacking super.img to ext4.img")
    os.system(here + "/simg2img/simg2img super/stock/super.img super/stock/super.ext4.img")

    print("Unpacking super.ext4.img")
    os.system("cd super/stock/;" + here +"/lpunpack_and_lpmake/bin/lpunpack super.ext4.img; cd ../..;")

    print("Copying images to super/custom")
    shutil.copyfile(gargoyle_rom_path, "super/custom/system.img")
    shutil.copyfile("super/stock/vendor.img", "super/custom/vendor.img")
    shutil.copyfile("super/stock/product.img", "super/custom/product.img")

    print("Script Complete")

if __name__ == '__main__':
    main()
