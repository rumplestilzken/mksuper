#!/usr/bin/env python3

import os
import lzma
from zipfile import ZipFile
import shutil
import tarfile
from argparse import ArgumentParser, RawDescriptionHelpFormatter, Action


def usage():
    print("""extract.py
    -stock: extracted stock image location
    -out : extracted super contents location""")


def parse_arguments():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, epilog=usage())
    parser.add_argument("-stock", required=False, type=str, default=None)
    parser.add_argument("-out", required=False, type=str, default=None)
    return parser.parse_args()


def main():
    args = parse_arguments()
    here = os.path.dirname(os.path.realpath(__file__))
    stock_rom_path = ""

    for file in os.listdir(here):
        if file.endswith(".zip"):
            stock_rom_path = file
            break

    if args.stock is not None:
        stock_rom_path = args.stock

    if stock_rom_path == "":
        print("No Stock Rom Found.")
        quit()
    else:
        print("Stock Rom Found:'" + stock_rom_path + "'")

    stock_rom_folder = os.path.splitext(stock_rom_path)[0]

    if args.stock is None:
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
        os.system("rm -rf super")
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
    stock_rom_location = here + "/" + stock_rom_folder
    if args.stock is not None:
        stock_rom_location = stock_rom_folder

    shutil.copyfile(stock_rom_location + "/super.img", here + "/super/stock/super.img")

    print("Unpacking super.img to ext4.img")
    os.system(here + "/bin/simg2img super/stock/super.img super/stock/super.ext4.img")

    print("Unpacking super.ext4.img")
    os.system("cd super/stock/;" + here + "/bin/lpunpack super.ext4.img; cd ../..;")

    is_seamless_update = False
    if os.path.isfile("super/stock/system_a.img") or os.path.isfile("super/stock/system_ext_a.img"):
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
        # Tank Mini
        shutil.copyfile("super/stock/vendor_a.img", "super/custom/vendor_a.img")
        shutil.copyfile("super/stock/vendor_b.img", "super/custom/vendor_b.img")
        shutil.copyfile("super/stock/product_a.img", "super/custom/product_a.img")
        shutil.copyfile("super/stock/product_b.img", "super/custom/product_b.img")

        try: #Tank Mini and Tank
            shutil.copyfile("super/stock/odm_dlkm_a.img", "super/custom/odm_dlkm_a.img")
            shutil.copyfile("super/stock/odm_dlkm_b.img", "super/custom/odm_dlkm_b.img")
            shutil.copyfile("super/stock/vendor_dlkm_a.img", "super/custom/vendor_dlkm_a.img")
            shutil.copyfile("super/stock/vendor_dlkm_b.img", "super/custom/vendor_dlkm_b.img")
            shutil.copyfile("super/stock/system_ext_a.img", "super/custom/system_ext_a.img")
            shutil.copyfile("super/stock/system_ext_b.img", "super/custom/system_ext_b.img")
        except :
            ""

    if args.out is not None:
        print("Copying super to '" + args.out + "'")
        os.system("cp -r super " + args.out + "; rm -rf super")


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
