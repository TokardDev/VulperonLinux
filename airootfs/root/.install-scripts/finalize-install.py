#!/bin/python

import curses
import subprocess
import os

current_menu = "main"
pacman_packages = []
pacman_packages_gpu = []
flatpak_packages = []


# ======= Functions =======


def installing(stdscr):

    curses.def_prog_mode()
    curses.endwin()

    pacman_command = f"pacman -S --noconfirm {' '.join(pacman_packages + pacman_packages_gpu)}"
    flatpak_command = f"flatpak install --assumeyes {' '.join(flatpak_packages)}"

    try:
        if len(pacman_packages) != 0 and len(pacman_packages_gpu) != 0:
            subprocess.run(f"arch-chroot /mnt/archinstall {pacman_command}", shell=True, check=True)

        if len(flatpak_packages) != 0:
            subprocess.run(f"arch-chroot /mnt/archinstall {flatpak_command}", shell=True, check=True)

        print("Packages installed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")

    curses.reset_prog_mode()
    stdscr.refresh()
    subprocess.run("clear", shell=True, check=True)
    print("Additions installed :3")
    return


# ======= Menus =======


def menu_main(stdscr):
    global current_menu
    options = ["Yes", "No"]
    curses.curs_set(0) 
    stdscr.clear()
    stdscr.refresh()

    selected = 0

    while current_menu == "main":
        stdscr.addstr(0, 2, "Yoooo ! Vulperon is installed !", curses.A_BOLD)
        stdscr.addstr(1, 2, "Would you like to add some recommended apps ?")
        stdscr.addstr(2, 4, "- GPU drivers")
        stdscr.addstr(3, 4, "- Recommended packages")
        stdscr.addstr(4, 4, "- Recommended Flatpak apps")

        for idx, option in enumerate(options):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(idx + 6, 4, f" {option} ", style)

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                selected = (selected - 1) % len(options)

            case curses.KEY_DOWN:
                selected = (selected + 1) % len(options)

            case curses.KEY_ENTER | 10 | 13:
                current_menu = "gpu" if selected == 0 else "exit"


def menu_gpu(stdscr):
    global current_menu, pacman_packages_gpu

    gpu_options = [
        ("Mesa (Open Source)", False, "mesa lib32-mesa lib32-mesa"),
        ("NVIDIA Proprietary (Recommended for NVIDIA)", False, "nvidia nvidia-utils lib32-nvidia-utils"), 
        ("AMD (Open Source)", False, "xf86-video-amdgpu mesa lib32-mesa vulkan-radeon"),
        ("Intel (Open Source)", False, "xf86-video-intel mesa lib32-mesa vulkan-intel") 
    ]
    
    curses.curs_set(0) 
    stdscr.clear()
    stdscr.refresh()

    selected = 0

    while current_menu == "gpu":
        stdscr.clear()

        stdscr.addstr(0, 2, "Choose the GPU driver(s) to install", curses.A_BOLD)
        stdscr.addstr(2, 4, "Use arrow keys to navigate, space to select, Enter to confirm.")
        
        for idx, (option, selected_flag, _) in enumerate(gpu_options):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            checkbox = "[x]" if selected_flag else "[ ]"
            stdscr.addstr(idx + 4, 4, f"{checkbox} {option}", style)

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                selected = (selected - 1) % len(gpu_options)

            case curses.KEY_DOWN:
                selected = (selected + 1) % len(gpu_options)

            case 32: # space bar pressed
                option, selected_flag, package = gpu_options[selected]
                gpu_options[selected] = (option, not selected_flag, package)

            case curses.KEY_ENTER | 10 | 13:
                selected_drivers = [option for option, selected_flag, _ in gpu_options if selected_flag]
                pacman_packages_gpu = [package for option, selected_flag, package in gpu_options if selected_flag]
                current_menu = "recommended_packages"


        stdscr.refresh()


def menu_packages(stdscr):
    global current_menu, pacman_packages

    recommended_packages = [
        ("Steam", False, "steam"),
        ("Visual Studio Code (Open Source Arch)", False, "code"),
        ("VirtManager & Qemu", False, "virt-manager qemu-full"),
        ("Firefox", False, "firefox"),
        ("GIMP", False, "gimp"),
        ("Audacity", False, "audacity"),
        ("Chromium", False, "chromium"),
        ("Thunderbird", False, "thunderbird"),
        ("OBS Studio", False, "obs-studio"),
        ("Kleopatra", False, "kleopatra")
    ]
    
    curses.curs_set(0) 
    stdscr.clear()
    stdscr.refresh()

    selected = 0

    while current_menu == "recommended_packages":
        stdscr.clear()

        stdscr.addstr(0, 2, "Choose the recommended packages to install", curses.A_BOLD)
        stdscr.addstr(0, 2, "You'll be able to install more packages after reboot with \"sudo pacman -S <package>\" ", curses.A_BOLD)
        stdscr.addstr(2, 4, "Use arrow keys to navigate, space to select, Enter to confirm.")
        
        for idx, (option, selected_flag, _) in enumerate(recommended_packages):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            checkbox = "[x]" if selected_flag else "[ ]"
            stdscr.addstr(idx + 4, 4, f"{checkbox} {option}", style)

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                selected = (selected - 1) % len(recommended_packages)

            case curses.KEY_DOWN:
                selected = (selected + 1) % len(recommended_packages)

            case 32: # space bar pressed
                option, selected_flag, package = recommended_packages[selected]
                recommended_packages[selected] = (option, not selected_flag, package)

            case curses.KEY_ENTER | 10 | 13:
                selected_apps = [option for option, selected_flag, _ in recommended_packages if selected_flag]
                pacman_packages.extend([package for _, selected_flag, package in recommended_packages if selected_flag])
                current_menu = "flatpak_packages"

        stdscr.refresh()



def menu_flatpak(stdscr):
    global current_menu, flatpak_packages

    flatpak_apps = [
        ("Flatseal (Manage flatpak permissions)", False, "com.github.tchx84.Flatseal")
        ("Discord", False, "com.discordapp.Discord"),
        ("GitHub Desktop", False, "io.github.shiftey.Desktop"),
        ("Brave Browser", False, "com.brave.Browser"),
        ("Deezer", False, "dev.aunetx.deezer"),
        ("Telegram", False, "org.telegram.desktop"),
        ("Materialgram (Telegram client)", False, "io.github.kukuruzka165.materialgram")
    ]

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    selected = 0

    while current_menu == "flatpak_packages":
        stdscr.clear()

        stdscr.addstr(0, 2, "Choose the Flatpak apps to install", curses.A_BOLD)
        stdscr.addstr(2, 4, "Use arrow keys to navigate, space to select, Enter to confirm.")

        for idx, (option, selected_flag, _) in enumerate(flatpak_apps):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            checkbox = "[x]" if selected_flag else "[ ]"
            stdscr.addstr(idx + 4, 4, f"{checkbox} {option}", style)

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                selected = (selected - 1) % len(flatpak_apps)

            case curses.KEY_DOWN:
                selected = (selected + 1) % len(flatpak_apps)

            case 32:
                option, selected_flag, app = flatpak_apps[selected]
                flatpak_apps[selected] = (option, not selected_flag, app)

            case curses.KEY_ENTER | 10 | 13:
                selected_apps = [option for option, selected_flag, _ in flatpak_apps if selected_flag]
                flatpak_packages.extend([app for option, selected_flag, app in flatpak_apps if selected_flag])
                current_menu = "ask_install"

        stdscr.refresh()



def menu_install(stdscr):
    global current_menu, pacman_packages, flatpak_packages

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    pacman_content = " ".join(pacman_packages + pacman_packages_gpu) if pacman_packages or pacman_packages_gpu else "No package selected."
    flatpak_content = " ".join(flatpak_packages) if flatpak_packages else "No Flatpak application selected."

    stdscr.addstr(0, 2, "The following packages will be installed:")
    stdscr.addstr(2, 2, f"Pacman: {pacman_content}")
    stdscr.addstr(3, 2, f"Flatpak: {flatpak_content}")

    stdscr.addstr(5, 2, "Do you want to install these packages?", curses.A_BOLD)

    options = ["No / Reconfigure", "Yes"]
    selected = 0

    while current_menu == "ask_install":
        for idx, option in enumerate(options):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(7 + idx, 4, f" {option} ", style)

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                selected = (selected - 1) % len(options)

            case curses.KEY_DOWN:
                selected = (selected + 1) % len(options)

            case curses.KEY_ENTER | 10 | 13:
                current_menu = "installing" if selected == 1 else "main"

        stdscr.refresh()


# ======= Main Loop =======


def main(stdscr):
    global current_menu

    while True:
        match current_menu:
            case "main":
                menu_main(stdscr)

            case "gpu":
                menu_gpu(stdscr)

            case "recommended_packages":
                menu_packages(stdscr)

            case "flatpak_packages":
                menu_flatpak(stdscr)

            case "ask_install":
                menu_install(stdscr)

            case "installing":
                installing(stdscr)
                return
                
            case "exit":
                return



curses.wrapper(main)