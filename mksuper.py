#!/usr/bin/env python3

import os
import shutil
from enum import IntEnum

class DeviceType(IntEnum):
    NotSet = 1
    Pocket = 2
    Slim = 3
    Tank = 4

def main():
    here = os.path.dirname(os.path.realpath(__file__))
    super_max_size=0
    gargoyle_rom_path = ""

    print("Starting Script")

    for file in os.listdir(here):
        if file.endswith(".img"):
            gargoyle_rom_path=file
            break

    if gargoyle_rom_path == "":
        print("No gargoyle system image Found.")
        quit()
    else:
        print("gargoyle system image Found:'" + gargoyle_rom_path + "'")

    dev = DeviceType.NotSet

    if "slim" in gargoyle_rom_path:
        dev = DeviceType.Slim
    if "pocket" in gargoyle_rom_path:
        dev = DeviceType.Pocket
    if "tank" in gargoyle_rom_path:
        dev = DeviceType.Tank

    match dev:
        case DeviceType.Slim:
            super_max_size=4831838208
        case DeviceType.Pocket:
            super_max_size=4831838208
        case DeviceType.Tank:
            super_max_size=4831838208
        case _:
            print("Device Not Detected")
            quit()

    print("Device Type: '" + dev.name + "'")

    print("Copying '" + gargoyle_rom_path + "' to super/custom/system.img")
    shutil.copyfile(gargoyle_rom_path, "super/custom/system.img")

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
