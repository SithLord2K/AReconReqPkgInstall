
import os
import apt
import sys
import subprocess

#Create a list of the required packages
with open("requiredpackages.txt", "r") as file:
    required_apps = file.read().splitlines()

#Create banner
banner = """
This script will install the packages required for AutoRecon.
Written By: Chris Wiley (SithLord2K)
Twitter: @sithlord2k
LinkedIn: https://www.linkedin.com/in/chris-wiley-007b9585
Email: sithlord2k@gmail.com
"""                                                                                                                                                                                                              

def main():
    #Clear the screen and make sure this is being run as root (sudo)
    os.system('clear')
    print(banner)
    if os.geteuid() != 0:
        print(f"[**] Important.")
        print(f"\tWe need elevated privileges (root)")
        print(f"\tPlease use sudo and re-run")
        exit()

    #Create, update and open apt cache
    print("[*] Updating apt cache")
    cache = apt.cache.Cache()
    cache.update()
    print("[*] Cache Update Complete.")
    cache.open()

    #Loop through the list and determine if the package is already installed or needs to be installed.
    for app in required_apps:
        if app in cache:
            pkg = cache[app]
            if not pkg.is_installed:
                #Flag the packages that need to be installed
                print(f"[*] Package {pkg} is marked for install.")
                pkg.mark_install()
            else:
                print(f"[*] Package {pkg} is already installed.")
        else:
            print(f"[X] Package '{pkg}' not found in cache.")

    #Commit the changes to install the packages
    cache.commit()

if __name__ == '__main__':
    main()
    print(f"[*] Requirements for AutoRecon are met.")
