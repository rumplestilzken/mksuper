#!/usr/bin/env python3

import os
import shutil
from enum import Enum
from argparse import ArgumentParser, RawDescriptionHelpFormatter, Action


class DeviceType(Enum):
    NotSet = ""
    Pocket = "pocket"
    Slim = "slim"
    Tank = "tank"
    Tank_Mini = "tank_mini"
    Jelly2E = "jelly2e"
    AtomL = "atoml"


class EnumAction(Action):
    """Argparse action for handling Enums"""

    def __init__(self, **kwargs):
        enum_type = kwargs.pop("type", None)
        if enum_type is None:
            raise ValueError("Type must be assigned an Enum when using EnumAction")

        if not issubclass(enum_type, Enum):
            raise TypeError("Type must be an Enum when using EnumAction")

        kwargs.setdefault("choices", tuple(e.value for e in enum_type))

        super(EnumAction, self).__init__(**kwargs)
        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        value = self._enum(values)
        setattr(namespace, self.dest, value)


def usage():
    print("""mksuper.py
    -repack: repacks stock image
    -dev: slim, pocket, tank, jelly2e, atoml, tank_mini automatically detected from gargoyle img if provided.
    -gsi: path to raw GSI image
    -out: output path of super image
    -no-product: produce a super image without product partitions """)


def parse_arguments():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, epilog=usage())
    parser.add_argument("-repack", required=False, action="store_false", default=None)
    parser.add_argument("-dev", required=False, type=DeviceType, action=EnumAction, default=DeviceType.NotSet)
    parser.add_argument("-gsi", required=False, type=str, default=None)
    parser.add_argument("-out", required=False, type=str, default=None)
    parser.add_argument("-super_path", required=False, type=str, default=None)
    parser.add_argument("-no-product", required=False, action="store_false", default=None)
    return parser.parse_args()


def main():
    args = parse_arguments()

    here = os.path.dirname(os.path.realpath(__file__))
    super_max_size = 0
    gargoyle_rom_path = ""

    print("Starting Script")

    if args.repack is None:
        for file in os.listdir(here):
            if file.endswith(".img"):
                gargoyle_rom_path = file
                break

        if args.gsi is not None:
            gargoyle_rom_path = args.gsi

        if gargoyle_rom_path == "":
            print("No gargoyle system image Found.")
            quit()
        else:
            print("gargoyle system image Found:'" + gargoyle_rom_path + "'")

    dev = DeviceType.NotSet
    is_seamless_update = False

    if args.dev == DeviceType.NotSet:
        if "slim" in gargoyle_rom_path:
            dev = DeviceType.Slim
        if "pocket" in gargoyle_rom_path:
            dev = DeviceType.Pocket
        if "tank" in gargoyle_rom_path:
            dev = DeviceType.Tank
        if "tank_mini" in gargoyle_rom_path:
            dev = DeviceType.Tank_Mini
        if "jelly2e" in gargoyle_rom_path:
            dev = DeviceType.Jelly2E
        if "atoml" in gargoyle_rom_path:
            dev = DeviceType.AtomL
    else:
        dev = args.dev

    match dev:
        case DeviceType.Slim:
            super_max_size = 4831838208
        case DeviceType.Pocket:
            super_max_size = 4831838208
        case DeviceType.AtomL:
            super_max_size = 4831838208
        case DeviceType.Tank:
            super_max_size = 9663676416
            main_a_max_size = 4831838208
            main_b_max_size = 4831838208
            is_seamless_update = True
        case DeviceType.Jelly2E:
            super_max_size = 5368709120
            main_a_max_size = 4831838208
            main_b_max_size = 4831838208
            is_seamless_update = True
        case DeviceType.Tank_Mini:
            super_max_size = 19323158528
            main_a_max_size = 9661579264
            main_b_max_size = 9661579264
            is_seamless_update = True
        case _:
            print("Device Not Detected. Are you using a gargoyle GSI image? Located at mksuper/*.img?")
            quit()

    print("Device Type: '" + dev.name + "'")

    super_path = here + "/super/"
    if args.super_path is not None:
        super_path = args.super_path + "/"

    if args.repack is None:
        if not dev == DeviceType.Tank and not dev == DeviceType.Tank_Mini and not dev == DeviceType.Jelly2E:
            print("Copying '" + gargoyle_rom_path + "' to " + super_path +"/custom/system.img")
            shutil.copyfile(gargoyle_rom_path, super_path + "/custom/system.img")
        else:
            print("Copying '" + gargoyle_rom_path + "' to " + super_path + "/custom/system_a.img")
            shutil.copyfile(gargoyle_rom_path, super_path + "/custom/system_a.img")
            # print("Copying '" + super_path + "/stock/system_a.img' to " + super_path + "/custom/system_b.img")
            # shutil.copyfile(super_path + "/stock/system_a.img", super_path + "/custom/system_b.img")
            shutil.copyfile(super_path + "/stock/system_b.img", super_path + "/custom/system_b.img")
    else:  # Repack
        if not dev == DeviceType.Tank and not dev == DeviceType.Jelly2E:
            print("Copying '" + super_path + "/stock/system.img' to " + super_path + "/custom/system.img")
            shutil.copyfile(super_path + "/stock/system.img", super_path + "/custom/system.img")
        else:
            print("Copying 'super/stock/system_a.img' to super/custom/system_a.img")
            shutil.copyfile(super_path + "/stock/system_a.img", super_path + "/custom/system_a.img")
            print("Copying 'super/stock/system_b.img' to super/custom/system_b.img")
            shutil.copyfile(super_path + "/stock/system_b.img", super_path + "/custom/system_b.img")

    print("Super Max Size '" + str(super_max_size) + "' bytes")

    metadata_slots = 0
    metadata_size = 65536
    odm_dlkm_a_size = 0
    odm_dlkm_b_size = 0
    vendor_dlkm_a_size = 0
    vendor_dlkm_b_size = 0

    if not is_seamless_update:
        system_size = os.path.getsize(super_path + "/custom/system.img")
        product_size = os.path.getsize(super_path + "/custom/product.img")
        vendor_size = os.path.getsize(super_path + "/custom/vendor.img")
        group_size = vendor_size + system_size

        if args.no_product is None:
            group_size =  product_size + group_size
            print("New product Size '" + str(product_size) + "' bytes")

        print("New vendor Size '" + str(vendor_size) + "' bytes")
        print("New system Size '" + str(system_size) + "' bytes")
        print("New group Size '" + str(group_size) + "' bytes")
        metadata_slots = 2
        super_size = group_size + metadata_size
    else:
        system_a_size = os.path.getsize(super_path + "/custom/system_a.img")
        system_b_size = os.path.getsize(super_path + "/custom/system_b.img")

        if args.no_product is None:
            product_a_size = os.path.getsize(super_path + "/custom/product_a.img")
            product_b_size = os.path.getsize(super_path + "/custom/product_b.img")
        vendor_a_size = os.path.getsize(super_path + "/custom/vendor_a.img")
        vendor_b_size = os.path.getsize(super_path + "/custom/vendor_b.img")

        main_a_size = system_a_size + vendor_a_size

        if args.no_product is None:
            main_a_size = product_a_size + main_a_size

        main_b_size = system_b_size + vendor_b_size

        if args.no_product is None:
            main_b_size =  product_b_size + main_b_size

        if dev is DeviceType.Tank_Mini:
            odm_dlkm_a_size = os.path.getsize(super_path + "/custom/odm_dlkm_a.img")
            vendor_dlkm_a_size = os.path.getsize(super_path + "/custom/vendor_dlkm_a.img")
            main_a_size = main_a_size + odm_dlkm_a_size + vendor_dlkm_a_size

            odm_dlkm_b_size = os.path.getsize(super_path + "/custom/odm_dlkm_b.img")
            vendor_dlkm_b_size = os.path.getsize(super_path + "/custom/vendor_dlkm_b.img")
            main_b_size = main_b_size + odm_dlkm_b_size + vendor_dlkm_b_size

        default_size = 0
        metadata_slots = 3
        super_size = default_size + main_a_size + main_b_size + metadata_size
        print("default max Size '" + str(default_size) + "' bytes")
        print("main_a max Size '" + str(main_a_max_size) + "' bytes")
        print("main_b max Size '" + str(main_b_max_size) + "' bytes")
        print("New default Size '" + str(default_size) + "' bytes")
        print("New main_a Size '" + str(main_a_size) + "' bytes")
        if args.no_product is None:
            print("New product_a Size '" + str(product_a_size) + "' bytes")
        print("New vendor_a Size '" + str(vendor_a_size) + "' bytes")
        print("New system_a Size '" + str(system_a_size) + "' bytes")
        print("New main_b Size '" + str(main_b_size) + "' bytes")
        if args.no_product is None:
            print("New product_b Size '" + str(product_b_size) + "' bytes")
        print("New vendor_b Size '" + str(vendor_b_size) + "' bytes")
        print("New system_b Size '" + str(system_b_size) + "' bytes")

        if dev is DeviceType.Tank_Mini:
            print("New odm_dlkm_a Size '" + str(odm_dlkm_a_size) + "' bytes")
            print("New odm_dlkm_b Size '" + str(odm_dlkm_b_size) + "' bytes")
            print("New vendor_dlkm_a Size '" + str(vendor_dlkm_a_size) + "' bytes")
            print("New vendor_dlkm_b Size '" + str(vendor_dlkm_b_size) + "' bytes")


    print("New super Size '" + str(super_size) + "' bytes")

    if super_size > super_max_size:
        print("WARNING: New super.img will be too large for your devices super partition. This is unsupported.")
        quit()

    #    if is_seamless_update:
    #        if default_size > 0:
    #            print("default group is larger than maximum allowed. This is unsupported.")
    #            quit()
    #        if main_a_size > main_a_max_size:
    #            print("main_a group is greater than ('" + str(main_a_size) +
    #                  "') the maximum allowed('" + str(main_a_max_size) + "'). This is unsupported.")
    #            quit()
    #        if main_b_size > main_b_max_size:
    #            print("main_b group is greater than ('" + str(main_b_size) +
    #                  "') the maximum allowed('" + str(main_b_max_size) + "'). This is unsupported.")
    #            quit()

    lpmake_command = "cd " + super_path + ";"
    lpmake_command += here + "/lpunpack_and_lpmake/bin/lpmake"
    lpmake_command += " --metadata-size " + str(metadata_size)
    lpmake_command += " --super-name super "
    lpmake_command += " --metadata-slots=" + str(metadata_slots)
    lpmake_command += " --device super:" + str(super_max_size)

    if not is_seamless_update:
        lpmake_command += " --group=main:" + str(group_size)
        lpmake_command += " --partition system:none:" + str(system_size) + ":main --image system=" + super_path + "/custom/system.img"
        lpmake_command += " --partition vendor:none:" + str(vendor_size) + ":main --image vendor=" + super_path + "/custom/vendor.img"
        if args.no_product is None:
            lpmake_command += " --partition product:none:" + str(product_size) + ":main --image " \
                                                                             "product=" + super_path + "/custom/product.img"
    else:
        # lpmake_command += " --group default:" + str(default_size)
        lpmake_command += " --group=main_a:" + str(main_a_size)
        lpmake_command += " --group main_b:" + str(main_b_size)
        lpmake_command += " --partition vendor_b:none:" + str(vendor_b_size) + ":main_b --image " \
                                                                               "vendor_b=" + super_path + "/custom/vendor_b.img"
        if args.no_product is None:
            lpmake_command += " --partition product_a:none:" + str(product_a_size) + ":main_a --image " \
                                                                                 "product_a=" + super_path + "/custom/product_a.img"
            lpmake_command += " --partition product_b:none:" + str(product_b_size) + ":main_b --image " \
                                                                                 "product_b=" + super_path + "/custom/product_b.img"
        lpmake_command += " --partition system_a:none:" + str(system_a_size) + ":main_a --image " \
                                                                               "system_a=" + super_path + "/custom/system_a.img"
        lpmake_command += " --partition system_b:none:" + str(system_b_size) + ":main_b --image " \
                                                                               "system_b=" + super_path + "/custom/system_b.img"
        lpmake_command += " --partition vendor_a:none:" + str(vendor_a_size) + ":main_a --image " \
                                                                               "vendor_a=" + super_path + "/custom/vendor_a.img"
        if dev is DeviceType.Tank_Mini:
            lpmake_command += " --partition odm_dlkm_a:none:" + str(odm_dlkm_a_size) + ":main_a --image " \
                                                                                   "odm_dlkm_a=" + super_path + "/custom/odm_dlkm_a.img"
            lpmake_command += " --partition odm_dlkm_b:none:" + str(odm_dlkm_b_size) + ":main_b --image " \
                                                                                       "odm_dlkm_b=" + super_path + "/custom/odm_dlkm_b.img"
            lpmake_command += " --partition vendor_dlkm_a:none:" + str(vendor_dlkm_a_size) + ":main_a --image " \
                                                                                       "vendor_dlkm_a=" + super_path + "/custom/vendor_dlkm_a.img"
            lpmake_command += " --partition vendor_dlkm_b:none:" + str(vendor_dlkm_b_size) + ":main_b --image " \
                                                                                             "vendor_dlkm_b=" + super_path + "/custom/vendor_dlkm_b.img"

    output_path = here + "/super/super.new.img"

    if args.out is not None:
        output_path = args.out

    lpmake_command += " --sparse --output " + output_path

    print("lpmake command:\n\t" + lpmake_command)
    os.system(lpmake_command + "\n")

    print("New super image created: " + here + "/super/super.new.img")

    if args.repack is not None:
        print("REPACK COMPLETE")

    print("Script Complete")


if __name__ == '__main__':
    main()
