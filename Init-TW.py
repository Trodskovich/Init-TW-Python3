# ------------------------------------------------------------------------------------------------------------------------------
# Init-TW-Python3 v2.0
# To Initialize New Tumbleweed Installation.
# Authour: Trodskovich
# requires python3-newt and newt preinstalled
# Run at your own Risk
# ------------------------------------------------------------------------------------------------------------------------------


import subprocess
from snack import SnackScreen, GridForm, ButtonBar, Textbox, CheckboxTree, snackArgs

# Clear the screen
subprocess.call("clear", shell=True)
seltext = ""

# class for the colors to use in printing messages
class blkColors:
    Header = "\033[95m"
    Blue = "\033[94m"
    Green = "\033[92m"
    Warning = "\033[93m"
    Error = "\033[91m"
    EndC = "\033[0m"
    Bold = "\033[1m"
    Undeline = "\033[4m"


# list of packages to install
packages = {
    "Multimedia_Codecs": (
        "lame",
        "ffmpeg-6",
        "ffmpegthumbs",
        "libxine2-codecs",
        "libavdevice60",
        "gstreamer",
        "gstreamer-plugins-bad",
        "gstreamer-plugins-base",
        "gstreamer-plugins-good",
        "gstreamer-plugins-good-extra",
        "gstreamer-plugins-good-gtk",
        "gstreamer-plugins-libav",
        "gstreamer-plugins-ugly",
        "gstreamer-plugins-ugly-orig-addon",
        "vlc-codec-gstreamer",
        "vlc-codecs",

    ),

    "Multimedia_Applications": (
        "vlc",
        "phonon4qt5-backend-vlc",
        "obs-studio",
        "kodi",
        "kdenlive",
        "audacity",
        "inkscape",
        "gimp",
        "krita",
        "elisa",
        "amarok",
        "smplayer",
        "smplayer-themes",
        "smplayer-skins",
    ),

    "Multimedia_Convertors": ("handbrake-gtk", "winff"),

    "Core_Applications": (
        "zip",
        "unzip",
        "rar",
        "unrar",
        "fish",
        "ibus-m17n",
        "git",
        "git-gui",
        "wordnet",
        "wine",
        "tmux",
        "screen",
        "yakuake",
        "ntfs-3g",
        "ntfsprogs",
        "libnotify-tools",
        "xdotool",
    ),
    "Antivirus": ("clamav", "clamtk"),

    "Internet_Applications": ("chromium", "flash-player", "filezilla"),

    "Utilities": (
        "dropbox",
        "krename",
        "kdeconnect-kde",
        "imagewriter",
        "filelight",
        "sweeper",
        "ktorrent",
        "konversation",
    ),

}

# to show a welcome screen
def welcome():
    screen = SnackScreen()
    bb = ButtonBar(screen, (("Continue", "continue"), ("Cancel", "cancel")))
    tb = Textbox(
        65,
        4,
        "Python Script to Initialize New openSUSE Tumbleweed Installation,\nlike Installing Applications, Enabling & Starting Services, \nand Performing Distrubution Update.",
    )
    g = GridForm(screen, "TW-Init - by Trodskovich", 1, 4)

    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)

    result = g.runOnce()
    screen.finish()
    return bb.buttonPressed(result)


# ask to add Packman Repo
def add_repo():
    screen = SnackScreen()
    bb = ButtonBar(screen, (("Add", "add"), ("Cancel", "cancel")))
    tb = Textbox(
        50,
        5,
        "Multimedia Applications and Codecs require Packman Repositary to be added in order to work correctly. \nDo you want add Packman repo now ?",0,1,
    )
    g = GridForm(screen, "Packman Repo", 1, 4)

    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)

    result = g.runOnce()
    screen.finish()
    return bb.buttonPressed(result)


# to show & Select Packages
def select_packages():
    global sellist
    screen = SnackScreen()
    ct = CheckboxTree(height=20, scroll=1)

    for idx, key in enumerate(packages):
        ct.append(key)
        for val in packages[key]:
            ct.addItem(val, (idx, snackArgs["append"]))
            ct.setEntryValue(val)

    bb = ButtonBar(screen, (("Next", "next"), ("Cancel", "cancel")))
    g = GridForm(screen, "Packages", 1, 4)

    g.add(ct, 0, 2)
    g.add(bb, 0, 3, growx=1)

    result = g.runOnce()
    screen.finish()

    # format selected packages list for zypper  and print(result)
    sellist = (
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
        "the packages selected to install are \n \n" + str(sellist.split(" ")),
        1,
        1
    )
    g = GridForm(screen, "Selected Packages", 1, 4)

    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)

    result = g.runOnce()
    screen.finish()
    return bb.buttonPressed(result)


# to start & Enable Services
def startups():
    print(
        blkColors.Blue
        + "\nchanging Default Login Shell to Fish for user...\n"
        + blkColors.EndC
    )
    subprocess.call(["sudo chsh -s /usr/bin/fish"], shell=True)
    print(
        blkColors.Blue
        + "\nchanging Default Login Shell to Fish for Root...\n"
        + blkColors.EndC
    )
    subprocess.call(["sudo chsh -s /usr/bin/fish root"], shell=True)
    print(
        blkColors.Blue + "\nupdating Clamav Antivirus Defintions...\n" + blkColors.EndC
    )
    subprocess.call(["sudo freshclam"], shell=True)
    print(
        blkColors.Blue
        + "\nEnabling and starting Clamav Antivirus Daemon [clamd] and Defintion update Daemon [freshclam] to autostart...\n"
        + blkColors.EndC
    )
    #subprocess.call(["sudo systemctl enable clamd"], shell=True)
    subprocess.call(["sudo systemctl enable freshclam"], shell=True)
    #subprocess.call(["sudo systemctl start clamd"], shell=True)
    return True


# to ask to run zypper Dup
def dup():
    screen = SnackScreen()
    bb = ButtonBar(screen, (("Yes", "yes"), ("No", "no")))
    tb = Textbox(
        70,
        4,
        "It's recomended to run the Distribution Update after Initiliazation. \nDo you want to run Distribution Update after Initiliazation ?",
    )
    g = GridForm(screen, "Distribution Update", 1, 4)

    g.add(tb, 0, 2)
    g.add(bb, 0, 3, growx=1)

    result = g.runOnce()
    screen.finish()
    return bb.buttonPressed(result)


# to run based on user inputs received
def init():
    chkwel = welcome()
    if chkwel == "cancel":
        print(blkColors.Error + "\nTw-Init Cancelled\n" + blkColors.EndC)
        quit()

    pkad = add_repo()
    inpk = select_packages()
    chkdup = dup()

    if pkad == "add":
        repoError=subprocess.call(
            [
                "sudo zypper ar -cfp 90 http://ftp.gwdg.de/pub/linux/packman/suse/openSUSE_Tumbleweed/ Packman"
            ],
            shell=True,
        )
        if repoError==0:
            print(blkColors.Green + "\nPackman Repo Added\n" + blkColors.EndC)
        else:
            print(blkColors.Error + "\nFailed to add Packman Repo Added\n" + blkColors.EndC)
    else:
        print(blkColors.Error + "\nPackman Repo Skipped\n" + blkColors.EndC)
    print(blkColors.Blue + "\nRefreshing Repos...\n" + blkColors.EndC)
    subprocess.call(["sudo zypper refresh"], shell=True)

    if inpk == "cancel":
        print(blkColors.Error + "\nPackage Selection Cancelled\n" + blkColors.EndC)
    elif sellist == "":
        print(blkColors.Error + "\nNo Packages Selected\n" + blkColors.EndC)
    else:
        print(blkColors.Blue + "\nInstalling Selected Packages...\n" + blkColors.EndC)
        subprocess.call(["sudo zypper in -ly " + sellist], shell=True)

    startups()

    if chkdup == "no":
        print(blkColors.Error + "\nDistribution Update Cancelled\n" + blkColors.EndC)
    else:
        print(blkColors.Blue + "\nStarting Distribution Update...\n" + blkColors.EndC)
        subprocess.call(["sudo zypper dup -l -y --allow-vendor-change"], shell=True)
        print(blkColors.Green + "\nDistribution Update Complete\n" + blkColors.EndC)
        print(blkColors.Green + "\nTW-Init Complete\n" + blkColors.EndC)
    return True


init()
