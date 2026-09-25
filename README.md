# Init-TW-Python3
## openSUSE Tumbleweed Desktop Post-Install Initializer
### -- by Trodskovich

[![Platform](https://shields.io)](https://opensuse.org)
[![Language](https://shields.io)](https://python.org)
[![License](https://shields.io)](LICENSE)

An interactive, text-based **TUI (Text User Interface) deployment utility** designed for field technicians to instantly initialize fresh openSUSE Tumbleweed desktop installations at customer sites. Driven entirely by a modular external configuration profile, it streamlines software installation, configures modern systemd timers, adjusts security modules, and tunes pro-audio environments.

---

## ⚡ The Quick Technician One-Liner

When standing at a customer's desk, open a terminal or switch to a text-only TTY, elevate to **root**, install the visual runtime framework, and run the utility directly from your repository in a single stream:

```bash
# Install the lightweight interactive dependencies...
sudo zypper in -y python3-newt newt python3-PyYAML
```


## 🛠️ Features & Architecture

* **Interactive TUI Flow:** Uses a responsive `newt/snack` menu framework that functions perfectly over native, text-only TTY consoles.
* **Completely Data-Driven:** Zero hardcoded package arrays or system commands. Software lists, shells, and systemd tracking are entirely isolated within an easily modifiable `packages.yaml` file.
* **Fault-Tolerant Package Validation:** Quietly checks local system states, cross-references choices against online repository metadata, filters out typos or deprecated packages on the fly, and continues the installation seamlessly.
* **Targeted Vendor Migration:** Safely handles openSUSE "vendor stickiness" by migrating multimedia codecs to the Packman mirror securely, without broadly breaking core system stability.
* **Pro-Audio & Security Modifications:** Deploys a custom PipeWire low-latency matrix (unlocking high-res Bluetooth audio like LDAC/aptX) and cleanly aligns security preferences to standard desktop AppArmor workflows.
* ** Technician Scorecard Report:** Generates a clean, green/red success scorecard directly to the terminal buffer at the end of the script to verify states before handing the machine to the customer.

---

## 🤷 Why not Ansible? (The Technician's Reality)

While Ansible is excellent for managing corporate clouds or large-scale headless server infrastructure, it is a poor fit for **walk-up, on-site desktop support on isolated customer networks**:
1.  Ansible requires you to pre-install extensive Python frameworks, modules, and SSH key configurations on a machine that hasn't even been initialized yet.
2.  Ansible is designed to be completely silent and push identical states. Customers are human beings who want custom configurations. `Init-TW-Python3` provides a visual checklist right in front of the customer, allowing you to check/uncheck software based on their unique billable requirements on the spot.

---

## 📂 Configuration Mapping (`packages.yaml`)

Modifying what this initialization tool deploys is entirely handled inside your configuration file:

```yaml
# Add software categories here
Packages:
  Multimedia_Codecs:
    - ffmpeg
    - pipewire-aptx
  Multimedia_Applications:
    - vlc
    - keysmith

# Add service behaviors and custom commands here
System_Mods:
  User_Commands:
    - "chsh -s /usr/bin/fish {USER}"
  Root_Commands:
    - "freshclam"
  Services:
    clamd: "enable --now"
    freshclam.timer: "enable --now"
```

---

## 📊 Deployment Summary Example

When the configuration finishes, the console buffer clears to render a structured environment audit:

```text
============================================================
          Init-TW-Python3 POST-INSTALL SUMMARY REPORT          
============================================================
Packman Repository:    [ENABLED]
User Shell (client):   [FISH]
Root Shell:            [FISH]
ClamAV Protection:     [RUNNING]

Package Status Check:
------------------------------
  ✓ ffmpeg                         [SUCCESS]
  ✓ vlc                            [SUCCESS]
  ✓ keysmith                       [SUCCESS]
  ⚠ pipewire-plugin-libav          [NOT IN REPO]
------------------------------
Total Progress: 3/4 Packages Configured successfully.
============================================================
```

---

## ⚖️ License

GNU General Public License v3.0. See `LICENSE` for more information.
# Init-TW-Python3
## openSUSE Tumbleweed Desktop Post-Install Initializer

[![Platform](https://shields.io)](https://opensuse.org)
[![Language](https://shields.io)](https://python.org)
[![License](https://shields.io)](LICENSE)

An interactive, text-based **TUI (Text User Interface) deployment utility** designed for field technicians to instantly initialize fresh openSUSE Tumbleweed desktop installations at customer sites. Driven entirely by a modular external configuration profile, it streamlines software installation, configures modern systemd timers, adjusts security modules, and tunes pro-audio environments.

---

## ⚡ The Quick Technician One-Liner

When standing at a customer's desk, open a terminal or switch to a text-only TTY, elevate to **root**, install the visual runtime framework, and run the utility directly from your repository in a single stream:

```bash
# 1. Install the lightweight interactive dependencies
sudo zypper in -y python3-newt newt python3-PyYAML

# 2. Run the deployment engine directly via GitHub streaming
sudo curl -sSL https://githubusercontent.com | sudo python3
```
*(Make sure to replace `YOUR_USERNAME/YOUR_REPO` with your actual GitHub coordinates).*

---

## 🛠️ Features & Architecture

* **Interactive TUI Flow:** Uses a responsive `newt/snack` menu framework that functions perfectly over native, text-only TTY consoles.
* **Completely Data-Driven:** Zero hardcoded package arrays or system commands. Software lists, shells, and systemd tracking are entirely isolated within an easily modifiable `packages.yaml` file.
* **Fault-Tolerant Package Validation:** Quietly checks local system states, cross-references choices against online repository metadata, filters out typos or deprecated packages on the fly, and continues the installation seamlessly.
* **Targeted Vendor Migration:** Safely handles openSUSE "vendor stickiness" by migrating multimedia codecs to the Packman mirror securely, without broadly breaking core system stability.
* **Pro-Audio & Security Modifications:** Deploys a custom PipeWire low-latency matrix (unlocking high-res Bluetooth audio like LDAC/aptX) and cleanly aligns security preferences to standard desktop AppArmor workflows.
* ** Technician Scorecard Report:** Generates a clean, green/red success scorecard directly to the terminal buffer at the end of the script to verify states before handing the machine to the customer.

---

## 🤷 Why not Ansible? (The Technician's Reality)

While Ansible is excellent for managing corporate clouds or large-scale headless server infrastructure, it is a poor fit for **walk-up, on-site desktop support on isolated customer networks**:
1.  Ansible requires you to pre-install extensive Python frameworks, modules, and SSH key configurations on a machine that hasn't even been initialized yet.
2.  Ansible is designed to be completely silent and push identical states. Customers are human beings who want custom configurations. `Init-TW-Python3` provides a visual checklist right in front of the customer, allowing you to check/uncheck software based on their unique billable requirements on the spot.

---

## 📂 Configuration Mapping (`packages.yaml`)

Modifying what this initialization tool deploys is entirely handled inside your configuration file:

```yaml
# Add software categories here
Packages:
  Multimedia_Codecs:
    - ffmpeg
    - pipewire-aptx
  Multimedia_Applications:
    - vlc
    - keysmith

# Add service behaviors and custom commands here
System_Mods:
  User_Commands:
    - "chsh -s /usr/bin/fish {USER}"
  Root_Commands:
    - "freshclam"
  Services:
    clamd: "enable --now"
    freshclam.timer: "enable --now"
```

---

## 📊 Deployment Summary Example

When the configuration finishes, the console buffer clears to render a structured environment audit:

```text
============================================================
          Init-TW-Python3 POST-INSTALL SUMMARY REPORT          
============================================================
Packman Repository:    [ENABLED]
User Shell (client):   [FISH]
Root Shell:            [FISH]
ClamAV Protection:     [RUNNING]

Package Status Check:
------------------------------
  ✓ ffmpeg                         [SUCCESS]
  ✓ vlc                            [SUCCESS]
  ✓ keysmith                       [SUCCESS]
  ⚠ pipewire-plugin-libav          [NOT IN REPO]
------------------------------
Total Progress: 3/4 Packages Configured successfully.
============================================================
```

---

## ⚖️ License

GNU General Public License v3.0. See `LICENSE` for more information.

