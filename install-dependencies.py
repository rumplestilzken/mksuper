#!/usr/bin/env python3

import platform
import os
import sys

def main():
    print("Starting Script")
    print("There are several dependencies needed.")
    # answer = input("Would you like to try to install them?(Y,n):");
    # if answer == "" or answer == "Y" or answer == "y":
    #     uname = os.system("uname -a")
    #     if "Ubuntu" in uname or "Debian" in uname:
    #         os.system("sudo apt install git libc++-dev clang")
    #     else:
    #         print("You need to manually install git libc++-dev and clang to continue with the process")
    os.
    if not os.path.exists("./lpunpack_and_lpmake"):
        print("Installing lpunpack_and_lpmake")
        os.system("git clone --quiet https://github.com/rumplestilzken/lpunpack_and_lpmake.git lpunpack_and_lpmake")
    if not os.path.exists("./lpunpack_and_lpmake/bin"):
        print("Building lpunpack_and_lpmake")
        os.system("cd lpunpack_and_lpmake; ./make.sh; cd ..")
    if os.path.exists("./lpunpack_and_lpmake/bin"):
        os.system("chmod +x lpunpack_and_lpmake/bin/*")
    if not os.path.exists("./simg2img"):
        print("Installing simg2img")
        os.system("git clone --quiet https://github.com/rumplestilzken/simg2img.git simg2img")
    if not os.path.exists("./simg2img/simg2img")
        os.system("cd simg2img; make")
    print("Script Complete")

if __name__ == '__main__':
    main()
