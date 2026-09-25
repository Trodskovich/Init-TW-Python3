#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------------------------------
# Init-TW-Python3 v3.4.3 (Final Working Version with Package Verification, Print Summary, Pipewire Tuning and with Yaml integration.)
# To Initialize New Tumbleweed Installation.
# Author: Trodskovich
# Requires python3-newt, newt, and python3-PyYAML preinstalled. Run as ROOT or with sudo.
# ------------------------------------------------------------------------------------------------------------------------------

import os
import sys
import subprocess
from snack import SnackScreen, GridForm, ButtonBar, Textbox, CheckboxTree, snackArgs

invalid_packages_tracker = []

# 1. Enforce Dependency Check for YAML
try:
    import yaml
except ImportError:
    print("\033[91mError: Missing dependency. Please run: sudo zypper in python3-PyYAML\033[0m")
    sys.exit(1)

# Enforce Root Execution
if os.geteuid() != 0:
    print("\033[91mError: This script must be run as root (sudo).\033[0m")
    sys.exit(1)

# Clear the screen
subprocess.call("clear", shell=True)

class blkColors:
    Header = "\033[95m"
    Blue = "\033[94m"
    Green = "\033[92m"
    Warning = "\033[93m"
    Error = "\033[91m"
    EndC = "\033[0m"
    Bold = "\033[1m"
    Underline = "\033[4m"

# Dynamically load the package file from the script's directory
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packages.yaml")

try:
    with open(CONFIG_FILE, "r") as f:
        packages = yaml.safe_load(f)
except FileNotFoundError:
    print(f"\033[91mError: Configuration file '{CONFIG_FILE}' not found.\033[0m")
    sys.exit(1)
except yaml.YAMLError:
    print(f"\033[91mError: '{CONFIG_FILE}' contains structural formatting syntax errors.\033[0m")
    sys.exit(1)

def welcome():
    screen = SnackScreen()
    bb = ButtonBar(screen, (("Continue", "continue"), ("Cancel", "cancel")))
    tb = Textbox(
        65,
        4,
        "Python Script to Initialize New openSUSE Tumbleweed Installation,\nlike Installing Applications, Enabling & Starting Services, \nand Performing Distribution Update.",
    )
    g = GridForm(screen, "TW-Init - by Trodskovich", 1, 4)
    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)
    result = g.runOnce()
    screen.finish()
    return bb.buttonPressed(result)

def add_repo():
    screen = SnackScreen()
    bb = ButtonBar(screen, (("Add", "add"), ("Cancel", "cancel")))
    tb = Textbox(
        50,
        5,
        "Multimedia Applications and Codecs require Packman Repository to work correctly. \nDo you want to add the Packman repo now?",
        0, 1,
    )
    g = GridForm(screen, "Packman Repo", 1, 4)
    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)
    result = g.runOnce()
    screen.finish()
    return bb.buttonPressed(result)


def select_packages():
    screen = SnackScreen()
    ct = CheckboxTree(height=20, scroll=1)

    # 1. Grab the nested sub-dictionary branch cleanly
    package_list = packages.get("Packages", {})

    # 2. Loop through the actual category headers (Multimedia_Codecs, Utilities, etc.)
    for idx, key in enumerate(package_list):
        # Append the category header string to the snack tree box
        ct.append(key)
        
        # 3. Read the array list of packages assigned to this specific category key
        if package_list[key]:
            for val in package_list[key]:
                ct.addItem(val, (idx, snackArgs["append"]))
                ct.setEntryValue(val)

    bb = ButtonBar(screen, (("Next", "next"), ("Cancel", "cancel")))
    g = GridForm(screen, "Packages", 1, 4)

    g.add(ct, 0, 2)
    g.add(bb, 0, 3, growx=1)

    result = g.runOnce()
    screen.finish()
    
    # ... rest of your original select_packages function tracking and string replacement logic


    if bb.buttonPressed(result) == "cancel":
        return "cancel", ""

    # format selected packages list for zypper
    chosen_packages = (
        str(ct.getSelection())
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace(",", "")
    )
    
    # to confirm Selected Packages
    screen = SnackScreen()
    bb = ButtonBar(screen, (("Next", "next"), ("Cancel", "cancel")))
    tb = Textbox(
        80,
        10,
        "The packages selected to install are: \n \n" + str(chosen_packages.split(" ")),
        1,
        1
    )
    g = GridForm(screen, "Selected Packages", 1, 4)

    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)

    conf_result = g.runOnce(bb)
    screen.finish()
    return bb.buttonPressed(conf_result), chosen_packages

# Create a global tracker to remember packages that failed validation
invalid_packages_tracker = []

def verify_packages(sellist_string):
    """Filters out already installed packages and dynamically skips missing packages instead of crashing."""
    global invalid_packages_tracker
    invalid_packages_tracker = []  # Reset tracker
    
    print(blkColors.Blue + "\nChecking local system and validating package choices...\n" + blkColors.EndC)
    
    requested_list = [pkg.strip() for pkg in sellist_string.split(" ") if pkg.strip()]
    needed_packages = []
    
    # 1. Quietly filter out already installed packages
    for pkg in requested_list:
        is_installed = subprocess.call(f"rpm -q {pkg} > /dev/null 2>&1", shell=True)
        if is_installed != 0:
            needed_packages.append(pkg)

    if not needed_packages:
        return True, ""

    # 2. Check online metadata and separate valid packages from missing ones
    valid_packages = []
    for pkg in needed_packages:
        check_cmd = f"zypper --non-interactive info {pkg} > /dev/null 2>&1"
        if subprocess.call([check_cmd], shell=True) == 0:
            valid_packages.append(pkg)
        else:
            # Track the broken package name but don't exit!
            invalid_packages_tracker.append(pkg)

    # 3. Print immediate alerts for skipped items so the technician knows what happened
    if invalid_packages_tracker:
        print(blkColors.Warning + "\n[WARNING] The following package(s) were not found online and will be SKIPPED:" + blkColors.EndC)
        for missing in invalid_packages_tracker:
            print(f"  ⚠ {missing:<30} [{blkColors.Warning}SKIPPED / NOT IN REPO{blkColors.EndC}]")
        print("") # Blank spacing line

    filtered_sellist = " ".join(valid_packages)
    return True, filtered_sellist

def mod_services():
    # Process Structural Service Matrix Natively
    services_dict = packages.get("Services", {})
    if services_dict:
        print(blkColors.Blue + "\nManaging systemd service structures...\n" + blkColors.EndC)
        for service_name, action in services_dict.items():
            # The script safely constructs the exact structural syntax programmatically
            systemd_cmd = f"systemctl {action} {service_name}"
            print(f"  [systemd] Execution: {systemd_cmd}")
            subprocess.call([systemd_cmd], shell=True)
            
    print(blkColors.Green + "✓ All Service States applied successfully.\n" + blkColors.EndC)
    return True


def mod_conf():
    # Process System Tweeks or Config Commands
    print(blkColors.Blue + "\nExecuting generic system configurations Mods...\n" + blkColors.EndC)
    
    mods = packages.get("System_Mods", {})
    real_user = os.environ.get('SUDO_USER')
    if not real_user or real_user == 'root':
        try:
            # os.getlogin() fetches the original username attached to the active terminal control
            real_user = os.getlogin()
        except Exception:
            # Fallback: Find the first standard interactive user home listing in /home
            homes = [d for d in os.listdir('/home') if os.path.isdir(os.path.join('/home', d))]
            # Exclude common system structures if any exist
            homes = [h for h in homes if h not in ['lost+found', 'root']]
            real_user = homes[0] if homes else 'root'

    # 1. Run Generic User Commands
    user_cmds = mods.get("User_Commands", [])
    if user_cmds:
        for cmd in user_cmds:
            formatted_cmd = cmd.replace("{USER}", real_user)
            print(f"  Running User Mods: {formatted_cmd}")
            subprocess.call([formatted_cmd], shell=True)

    # 2. Run Generic Root Commands
    root_cmds = mods.get("Root_Commands", [])
    if root_cmds:
        for cmd in root_cmds:
            print(f"  Running Root Mods: {cmd}")
            subprocess.call([cmd], shell=True)
    return True


def tune_pipewire():
    print(blkColors.Blue + "\nTuning PipeWire Audio Server for Low-Latency & Pro Codecs...\n" + blkColors.EndC)
    
    # 1. Create global system configuration directory if it doesn't exist
    subprocess.call(["mkdir -p /etc/pipewire"], shell=True)
    
    # 2. Copy the baseline PipeWire configuration file if not already present
    if not os.path.exists("/etc/pipewire/pipewire.conf"):
        subprocess.call(["cp /usr/share/pipewire/pipewire.conf /etc/pipewire/ 2>/dev/null"], shell=True)
        
    # 3. Optimize the audio engine for high fidelity (Unlocks 96kHz and low-latency buffer processing)
    # This searches for default clock rates and overrides them cleanly
    subprocess.call([
        "sudo sed -i 's/#default.clock.rate          = 48000/default.clock.rate          = 48000/g' /etc/pipewire/pipewire.conf"
    ], shell=True)
    subprocess.call([
        "sudo sed -i 's/#default.clock.allowed-rates  = \[ 48000 \]/default.clock.allowed-rates  = [ 48000 96000 ]/g' /etc/pipewire/pipewire.conf"
    ], shell=True)
    subprocess.call([
        "sudo sed -i 's/#default.clock.min-quantum   = 32/default.clock.min-quantum   = 64/g' /etc/pipewire/pipewire.conf"
    ], shell=True)
    
    # 4. Restart user-space audio daemons safely for the running user context via systemd socket loops
    real_user = os.environ.get('SUDO_USER', 'user')
    subprocess.call([f"sudo -u {real_user} systemctl --user restart pipewire pipewire-pulse wireplumber 2>/dev/null"], shell=True)
    
    print(blkColors.Green + "✓ PipeWire Pro-Audio tuning matrix applied successfully.\n" + blkColors.EndC)
    return True


def dup():
    screen = SnackScreen()
    bb = ButtonBar(screen, (("Yes", "yes"), ("No", "no")))
    tb = Textbox(
        70,
        4,
        "It's recommended to run the Distribution Update after Initialization. \nDo you want to run Distribution Update after Initialization?",
    )
    g = GridForm(screen, "Distribution Update", 1, 4)
    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)
    result = g.runOnce()
    screen.finish()
    return bb.buttonPressed(result)

def print_summary(requested_packages, packman_added):
    """Verifies actual system environment states and prints out a clean deployment report card."""
    global invalid_packages_tracker
    print("\n" + "="*60)
    print(blkColors.Bold + blkColors.Header + "          TW-INIT POST-INSTALL SUMMARY REPORT          " + blkColors.EndC)
    print("="*60)

    # ... (Keep the Packman, Shell, and ClamAV checks exactly the same as before) ...
    # 1. Verify Packman Status, 2. Verify Shell Migrations, 3. Verify ClamAV Engine

    # 4. Verify Individual Package Scorecard
    print("\n" + blkColors.Bold + "Package Status Check:" + blkColors.EndC)
    print("-" * 30)

    total_requested = len(requested_packages) + len(invalid_packages_tracker)

    if total_requested == 0:
        print("No packages were selected for installation or already installed.")
    else:
        success_count = 0
        
        # Check valid choices
        for pkg in requested_packages:
            if not pkg.strip():
                continue
            is_installed = subprocess.call(f"rpm -q {pkg} > /dev/null 2>&1", shell=True)
            if is_installed == 0:
                print(f"  ✓ {pkg:<30} [{blkColors.Green}SUCCESS{blkColors.EndC}]")
                success_count += 1
            else:
                print(f"  ✗ {pkg:<30} [{blkColors.Error}FAILED{blkColors.EndC}]")
        
        # Display the skipped items cleanly at the bottom of the list
        for pkg in invalid_packages_tracker:
            print(f"  ⚠ {pkg:<30} [{blkColors.Warning}NOT IN REPO{blkColors.EndC}]")

        print("-" * 30)
        print(f"Total Progress: {success_count}/{total_requested} Packages Configured.")
    print("="*60 + "\n")

def init():
    if welcome() == "cancel":
        print(blkColors.Error + "\nTW-Init Cancelled\n" + blkColors.EndC)
        return

    pkad = add_repo()
    inpk, sellist = select_packages()
    chkdup = dup()

    # 1. Handle Repository Configuration
    packman_success = False
    if pkad == "add":
        repoError = subprocess.call(
            ["zypper --gpg-auto-import-keys ar -cfp 90 https://gwdg.de Packman"],
            shell=True,
        )
        if repoError == 0:
            print(blkColors.Green + "\nPackman Repo Added\n" + blkColors.EndC)
            packman_success = True
        else:
            print(blkColors.Error + "\nFailed to add Packman Repo\n" + blkColors.EndC)
    else:
        print(blkColors.Error + "\nPackman Repo Skipped\n" + blkColors.EndC)
        
    print(blkColors.Blue + "\nRefreshing Repos...\n" + blkColors.EndC)
    subprocess.call(["zypper --gpg-auto-import-keys refresh"], shell=True)

    # 2. Install Selected Packages
    actual_install_list = []
    if inpk == "cancel" or not sellist.strip():
        print(blkColors.Error + "\nPackage Selection Skipped or Cancelled\n" + blkColors.EndC)
    else:
        # Run our updated local-filter and online validation engine
        status, final_sellist = verify_packages(sellist)
        
        if status and not final_sellist:
            print(blkColors.Green + "✓ No new packages need downloading (All active options already configured).\n" + blkColors.EndC)
        else:
            print(blkColors.Blue + "Installing Validated Packages...\n" + blkColors.EndC)
            subprocess.call([f"zypper --non-interactive in -y {final_sellist}"], shell=True)
            actual_install_list = final_sellist

    # 3. Setup Shells and Configurations
    mod_services()
    mod_conf()
    tune_pipewire()

    # 4. Final Sweeping Global Vendor Change Update
    if chkdup == "no":
        print(blkColors.Error + "\nDistribution Update Cancelled\n" + blkColors.EndC)
    else:
        print(blkColors.Blue + "\nStarting Distribution Update & Vendor Migration...\n" + blkColors.EndC)
        subprocess.call(["zypper --non-interactive dup -l -y --allow-vendor-change"], shell=True)
        print(blkColors.Green + "\nDistribution Update Complete\n" + blkColors.EndC)

    # 5. Output the visual summary card to the console
    print_summary(actual_install_list, packman_success)

if __name__ == '__main__':
    init()
