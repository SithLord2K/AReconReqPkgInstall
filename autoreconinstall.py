import os
import sys
import argparse
import subprocess
from platform import system as platform_system

# // Import the apt library, but handle the case where it's not installed.
try:
    import apt
except ImportError:
    print("[!] python3-apt is not installed. Please install it using: sudo apt-get install python3-apt")
    sys.exit(1)

# // Function to clear the console screen in a cross-platform way.
def clear_screen():
    # // Check the operating system and use the appropriate clear command.
    if platform_system() == "Windows":
        os.system("cls")
    else:
        # // For Linux and macOS
        os.system("clear")

# // Create banner with contact and project information.
banner = """
This script will install the packages required for AutoRecon.
Written By: Chris Wiley (SithLord2K)
Twitter: @sithlord2k
LinkedIn: https://www.linkedin.com/in/chris-wiley-007b9585
Email: sithlord2k@gmail.com
"""

def main(packages_file):
    # // Clear the screen and display the banner.
    clear_screen()
    print(banner)

    # // Check for root privileges, which are required for package management.
    if os.geteuid() != 0:
        print("[**] Important: This script requires elevated privileges.")
        print("\tPlease run it with sudo.")
        sys.exit(1)

    # // Read the list of required packages from the specified file.
    try:
        with open(packages_file, "r") as file:
            required_apps = file.read().splitlines()
    except FileNotFoundError:
        print(f"[X] Error: The file '{packages_file}' was not found.")
        sys.exit(1)

    try:
        # // Initialize the apt cache.
        print("[*] Updating apt cache...")
        cache = apt.cache.Cache()
        cache.update()
        print("[*] Cache update complete.")
        cache.open()

        packages_to_install = []

        # // Loop through the list of required packages.
        for app in required_apps:
            # // Check if the package exists in the cache.
            if app in cache:
                pkg = cache[app]
                # // Check if the package is already installed.
                if not pkg.is_installed:
                    print(f"[*] Marking '{app}' for installation.")
                    pkg.mark_install()
                    packages_to_install.append(app)
                else:
                    print(f"[*] Package '{app}' is already installed.")
            else:
                print(f"[X] Package '{app}' not found in the apt repository.")

        # // If there are packages to install, commit the changes.
        if packages_to_install:
            print("\n[*] Installing the following packages:", ", ".join(packages_to_install))
            try:
                cache.commit()
                print("\n[+] All packages were installed successfully.")
            except Exception as e:
                print(f"\n[X] An error occurred during installation: {e}")
                sys.exit(1)
        else:
            print("\n[*] No new packages to install.")

    except Exception as e:
        print(f"\n[X] An unexpected error occurred with apt: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # // Set up command-line argument parsing.
    parser = argparse.ArgumentParser(description="AutoRecon Package Installer")
    parser.add_argument(
        "-r", "--requirements",
        default="requiredpackages.txt",
        help="Path to the requirements file (default: requiredpackages.txt)"
    )
    args = parser.parse_args()

    # // Call the main function with the provided requirements file.
    main(args.requirements)
    print("\n[*] Requirement check for AutoRecon is complete.")
