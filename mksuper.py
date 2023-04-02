#!/usr/bin/env python3

import platform
import os
import sys
import subprocess

def main():
    here = os.path.dirname(os.path.realpath(__file__))
    super_max_size=0

    print("Starting Script")

    menu={}
    menu['1']="Pocket"
    menu['2']="Slim"

    for menuItem in menu:
        print(menuItem, menu[menuItem])

    selection=input("Please Select which device you are working on:")

    if not selection in ['1', '2']:
        print("Please select an option from the list.")
        quit()

    match selection:
        case '1':
            super_max_size=4831838208
        case '2':
            super_max_size=4831838208

    print("Super Max Size '" + str(super_max_size) + "' bytes")

    product_size=os.path.getsize(here+"/super/custom/product.img")
    vendor_size=os.path.getsize(here+"/super/custom/vendor.img")
    system_size=os.path.getsize(here+"/super/custom/system.img")
    metadata_size=65536
    group_size=product_size + vendor_size + system_size;
    super_size=group_size + metadata_size;

    print("New product Size '" + str(product_size) + "' bytes")
    print("New vendor Size '" + str(vendor_size) + "' bytes")
    print("New system Size '" + str(system_size) + "' bytes")
    print("New group Size '" + str(group_size) + "' bytes")
    print("New super Size '" + str(super_size) + "' bytes")

    if super_size > super_max_size:
        print("WARNING: New super.img will be too large for your devices super partition. This is unsupported.")
        quit()

    lpmake_command="cd super;"
    lpmake_command+=here+"/lpunpack_and_lpmake/bin/lpmake"
    lpmake_command+= " --metadata-size " + str(metadata_size)
    lpmake_command+= " --super-name super "
    lpmake_command+= " --metadata-slots 2 "
    lpmake_command+= " --device super:" + str(super_max_size)
    lpmake_command+= " --group main:" + str(group_size)
    lpmake_command+= " --partition system:readonly:" + str(system_size) + ":main --image system=custom/system.img"
    lpmake_command+= " --partition vendor:readonly:" + str(vendor_size) + ":main --image vendor=custom/vendor.img"
    lpmake_command+= " --partition product:readonly:" + str(product_size) + ":main --image product=custom/product.img"
    lpmake_command+= " --sparse --output " + here + "/super/super.new.img"

    print("lpmake command:\n\t" + lpmake_command)
    os.system(lpmake_command)

    print("New super image created: "+ here +"/super/super.new.img")

    print("Script Complete")

if __name__ == '__main__':
    main()
