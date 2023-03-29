#!/usr/bin/env python3

import platform
import os
import sys
import subprocess

def main():
    install_lpmake=True
    install_simg2img=True
    print("Starting Script")
    print("There are several dependencies needed.")
    answer = input("Would you like to try to install them?(Y,n):");
    if answer == "" or answer == "Y" or answer == "y":
        name = subprocess.run(['uname', '-a'], capture_output=True, text=True).stdout
        if "Ubuntu" in name or "Debian" in name:
            os.system("sudo apt install git libc++-dev clang g++")
        else:
            print("You need to manually install git libc++-dev, clang and g++ to continue with the process")
            answer = input("Are these already installed?(Y,n):")
            if not answer == "" or answer == "Y" or answer == "y":
                install_lpmake=False
                install_simg2img=False
    if not os.path.exists("./lpunpack_and_lpmake"):
        print("Installing lpunpack_and_lpmake")
        os.system("git clone --quiet https://github.com/rumplestilzken/lpunpack_and_lpmake.git lpunpack_and_lpmake")
    if not os.path.exists("./lpunpack_and_lpmake/bin") and install_lpmake:
        print("Building lpunpack_and_lpmake")
        os.system("cd lpunpack_and_lpmake; ./make.sh; cd ..")
    if os.path.exists("./lpunpack_and_lpmake/bin") and install_lpmake:
        os.system("chmod +x lpunpack_and_lpmake/bin/*")
    if not os.path.exists("./simg2img"):
        print("Installing simg2img")
        os.system("git clone --quiet https://github.com/rumplestilzken/simg2img.git simg2img")
    if not os.path.exists("./simg2img/simg2img") and install_simg2img:
        print("Building simg2img")
        os.system("cd simg2img; make; cd ..;")
    print("Script Complete")

if __name__ == '__main__':
    main()
