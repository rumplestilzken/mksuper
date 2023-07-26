#!/usr/bin/env python3

import os
import lzma
from zipfile import ZipFile
import shutil
import tarfile


def main():
    here = os.path.dirname(os.path.realpath(__file__))
    stock_rom_path = ""

    for file in os.listdir(here):
        if file.endswith(".zip"):
            stock_rom_path = file
            break

    if stock_rom_path == "":
        print("No Stock Rom Found.")
        quit()
    else:
        print("Stock Rom Found:'" + stock_rom_path + "'")

    stock_rom_folder = os.path.splitext(stock_rom_path)[0]

    print("Unzipping Stock rom to " + stock_rom_folder)
    with ZipFile(stock_rom_path) as zObject:
        zObject.extract(stock_rom_folder + "/super.img", here)
        zObject.extract(stock_rom_folder + "/boot.img", here)
        zObject.extract(stock_rom_folder + "/vbmeta.img", here)
        zObject.extract(stock_rom_folder + "/vbmeta_system.img", here)
        zObject.extract(stock_rom_folder + "/vbmeta_vendor.img", here)
        try:
            zObject.extract(stock_rom_folder + "/vendor_boot.img", here)
        except:
            ""
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
    os.system("cd super/stock/;" + here + "/lpunpack_and_lpmake/bin/lpunpack super.ext4.img; cd ../..;")

    is_seamless_update = False
    if os.path.isfile("super/stock/system_a.img"):
        is_seamless_update = True

    print("Copying images to super/custom")
    if not is_seamless_update:
        # Titan Pocket
        # Atom L
        shutil.copyfile("super/stock/vendor.img", "super/custom/vendor.img")
        shutil.copyfile("super/stock/product.img", "super/custom/product.img")
    else:
        # Tank
        # Jelly 2E
        shutil.copyfile("super/stock/vendor_a.img", "super/custom/vendor_a.img")
        shutil.copyfile("super/stock/vendor_b.img", "super/custom/vendor_b.img")
        shutil.copyfile("super/stock/product_a.img", "super/custom/product_a.img")
        shutil.copyfile("super/stock/product_b.img", "super/custom/product_b.img")

    # Get Compressed File
    compressed_file = ""
    tar = False
    xz = False
    for file in os.listdir(here):
        if file.endswith(".tar.gz"):
            compressed_file = file
            tar = True
            break
        if file.endswith(".xz"):
            compressed_file = file
            xz = True
            break

    # Uncompress compressed_file
    if not compressed_file == "" and tar:
        print("Extracting gargoyle GSI '" + compressed_file + "'")
        with tarfile.open(compressed_file, "r") as tf:
            tf.extractall(path=here + "/")
    elif not compressed_file == "" and xz:
        print("Extracting gargoyle GSI '" + compressed_file + "'")
        with lzma.open(compressed_file) as f, open(here + "/" + compressed_file.strip(".xz"), 'wb') as fout:
            file_content = f.read()
            fout.write(file_content)

    print("Script Complete")


if __name__ == '__main__':
    main()
