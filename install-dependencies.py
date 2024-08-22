#!/usr/bin/env python3

import platform
import os
import sys
import subprocess

def main():
    print("Starting Script")
    print("There are several dependencies needed.")
    answer = input("Would you like to try to install them?(Y,n):");
    if answer == "" or answer == "Y" or answer == "y":
        name = subprocess.run(['uname', '-a'], capture_output=True, text=True).stdout
        if "Ubuntu" in name or "Debian" in name:
            os.system("sudo apt install git libc++-dev clang g++ make libz-dev")
        else:
            print("You need to manually install git libc++-dev, clang, g++, make and libz-dev to continue with the process")
            answer = input("Are these already installed?(Y,n):")
    print("Script Complete")

if __name__ == '__main__':
    main()
