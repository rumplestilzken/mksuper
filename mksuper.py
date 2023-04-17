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
    super_max_size = 0
    gargoyle_rom_path = ""

    print("Starting Script")

    for file in os.listdir(here):
        if file.endswith(".img"):
            gargoyle_rom_path = file
            break

    if gargoyle_rom_path == "":
        print("No gargoyle system image Found.")
        quit()
    else:
        print("gargoyle system image Found:'" + gargoyle_rom_path + "'")

    dev = DeviceType.NotSet
    is_seamless_update = False

    if "slim" in gargoyle_rom_path:
        dev = DeviceType.Slim
    if "pocket" in gargoyle_rom_path:
        dev = DeviceType.Pocket
    if "tank" in gargoyle_rom_path:
        dev = DeviceType.Tank

    match dev:
        case DeviceType.Slim:
            super_max_size = 4831838208
        case DeviceType.Pocket:
            super_max_size = 4831838208
        case DeviceType.Tank:
            super_max_size = 9663676416
            main_a_max_size = 4831838208
            main_b_max_size = 4831838208
            is_seamless_update = True
        case _:
            print("Device Not Detected. Are you using a gargoyle GSI image? Located at mksuper/*.img?")
            quit()

    print("Device Type: '" + dev.name + "'")

    if not dev == DeviceType.Tank:
        print("Copying '" + gargoyle_rom_path + "' to super/custom/system.img")
        shutil.copyfile(gargoyle_rom_path, "super/custom/system.img")
    else:
        print("Copying '" + gargoyle_rom_path + "' to super/custom/system_a.img")
        shutil.copyfile(gargoyle_rom_path, "super/custom/system_a.img")
        print("Copying 'super/stock/system_a.img' to super/custom/system_b.img")
        shutil.copyfile("super/stock/system_a.img", "super/custom/system_b.img")

    print("Super Max Size '" + str(super_max_size) + "' bytes")

    metadata_slots = 0
    metadata_size = 65536

    if not is_seamless_update:
        system_size = os.path.getsize(here + "/super/custom/system.img")
        product_size = os.path.getsize(here + "/super/custom/product.img")
        vendor_size = os.path.getsize(here + "/super/custom/vendor.img")
        group_size = product_size + vendor_size + system_size;
        print("New product Size '" + str(product_size) + "' bytes")
        print("New vendor Size '" + str(vendor_size) + "' bytes")
        print("New system Size '" + str(system_size) + "' bytes")
        print("New group Size '" + str(group_size) + "' bytes")
        metadata_slots = 2
        super_size = group_size + metadata_size;
    else:
        system_a_size = os.path.getsize(here + "/super/custom/system_a.img")
        system_b_size = os.path.getsize(here + "/super/custom/system_b.img")
        product_a_size = os.path.getsize(here + "/super/custom/product_a.img")
        product_b_size = os.path.getsize(here + "/super/custom/product_b.img")
        vendor_a_size = os.path.getsize(here + "/super/custom/vendor_a.img")
        vendor_b_size = os.path.getsize(here + "/super/custom/vendor_b.img")
        main_a_size = system_a_size + product_a_size + vendor_a_size
        main_b_size = system_b_size + product_b_size + vendor_b_size
        default_size = 0
        metadata_slots = 3
        super_size = default_size + main_a_size + main_b_size + metadata_size
        print("default max Size '" + str(default_size) + "' bytes")
        print("main_a max Size '" + str(main_a_max_size) + "' bytes")
        print("main_b max Size '" + str(main_b_max_size) + "' bytes")
        print("New default Size '" + str(default_size) + "' bytes")
        print("New main_a Size '" + str(main_a_size) + "' bytes")
        print("New product_a Size '" + str(product_a_size) + "' bytes")
        print("New vendor_a Size '" + str(vendor_a_size) + "' bytes")
        print("New system_a Size '" + str(system_a_size) + "' bytes")
        print("New main_b Size '" + str(main_b_size) + "' bytes")
        print("New product_b Size '" + str(product_b_size) + "' bytes")
        print("New vendor_b Size '" + str(vendor_b_size) + "' bytes")
        print("New system_b Size '" + str(system_b_size) + "' bytes")

    print("New super Size '" + str(super_size) + "' bytes")

    if super_size > super_max_size:
        print("WARNING: New super.img will be too large for your devices super partition. This is unsupported.")
        quit()

    if is_seamless_update:
        if default_size > 0:
            print("default group is larger than maximum allowed. This is unsupported.")
            quit()
        if main_a_size > main_a_max_size:
            print("main_a group is greater than ('" + str(main_a_size) +
                  "') the maximum allowed('" + str(main_a_max_size) + "'). This is unsupported.")
            quit()
        if main_b_size > main_b_max_size:
            print("main_b group is greater than ('" + str(main_b_size) +
                  "') the maximum allowed('" + str(main_b_max_size) + "'). This is unsupported.")
            quit()

    lpmake_command = "cd super;"
    lpmake_command += here + "/lpunpack_and_lpmake/bin/lpmake"
    lpmake_command += " --metadata-size " + str(metadata_size)
    lpmake_command += " --super-name super "
    lpmake_command += " --metadata-slots=" + str(metadata_slots)
    lpmake_command += " --device super:" + str(super_max_size)

    if not is_seamless_update:
        lpmake_command += " --group=main:" + str(group_size)
        lpmake_command += " --partition system:readonly:" + str(system_size) + ":main --image system=custom/system.img"
        lpmake_command += " --partition vendor:readonly:" + str(vendor_size) + ":main --image vendor=custom/vendor.img"
        lpmake_command += " --partition product:readonly:" + str(product_size) + ":main --image " \
                                                                                 "product=custom/product.img"
    else:
        # lpmake_command += " --group default:" + str(default_size)
        lpmake_command += " --group=main_a:" + str(main_a_size)
        lpmake_command += " --group main_b:" + str(main_b_size)
        lpmake_command += " --partition vendor_b:none:" + str(vendor_b_size) + ":main_b --image " \
                                                                               "vendor_b=custom/vendor_b.img"
        lpmake_command += " --partition product_a:none:" + str(product_a_size) + ":main_a --image " \
                                                                                 "product_a=custom/product_a.img"
        lpmake_command += " --partition product_b:none:" + str(product_b_size) + ":main_b --image " \
                                                                                 "product_b=custom/product_b.img"
        lpmake_command += " --partition system_a:none:" + str(system_a_size) + ":main_a --image " \
                                                                                   "system_a=custom/system_a.img"
        lpmake_command += " --partition system_b:none:" + str(system_b_size) + ":main_b --image " \
                                                                               "system_b=custom/system_b.img"
        lpmake_command += " --partition vendor_a:none:" + str(vendor_a_size) + ":main_a --image " \
                                                                                   "vendor_a=custom/vendor_a.img"


    lpmake_command += " --sparse --output " + here + "/super/super.new.img"

    print("lpmake command:\n\t" + lpmake_command)
    os.system(lpmake_command + "\n")

    print("New super image created: " + here + "/super/super.new.img")

    print("Script Complete")


if __name__ == '__main__':
    main()
