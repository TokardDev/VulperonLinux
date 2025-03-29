#!/bin/python

import curses
import subprocess
import os

current_menu = "main"
interface = None


# ======= Functions =======


def check_network():
    try:
        subprocess.run(
            ["ping", "-c", "1", "archlinux.org"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False 


def get_available_devices(): # not tested yet
    try:
        result = subprocess.run(["iwctl", "device", "list"], capture_output=True, text=True, check=True)
        devices = []
        lines = result.stdout.splitlines()

        for line in lines[4:]:
            device = line.split()[0]
            devices.append(device)

        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
        return []


def run_archinstall(stdscr):
    global current_menu

    curses.def_prog_mode()
    curses.endwin()

    subprocess.run([
        "archinstall",
        "--script", "vulperon-archiso",
        "--config", "/root/.install-scripts/user_configuration.json",
        "--creds", "/root/.install-scripts/user_credentials.json"
    ])
    subprocess.run(["/root/.install-scripts/move-configs.sh"]) # move files to new system
    subprocess.run(["/root/.install-scripts/post-install.sh"]) # execute scripts in chroot, maybe can be merged with above script ? 
    subprocess.run(["python3", "/root/.install-scripts/finalize-install.py"]) # mostly systemctl related, update dconf
    subprocess.run("clear", shell=True, check=True)
    curses.reset_prog_mode()
    stdscr.refresh()


def get_available_networks(device): # not tested yet
    subprocess.run(["iwctl", "station", device, "scan"], capture_output=True, text=True, check=True)
    result = subprocess.run(["iwctl", "station", device, "get-networks"], capture_output=True, text=True, check=True)[3:]

    networks = []
    lines = result.stdout.splitlines()
    for line in lines[3:]:
        network = line.split()[0] # get network name
        networks.append(network)
    return networks


# ======= Menus =======


def menu_wifi(stdscr):
    global interface, current_menu

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    selected = 0
    networks = get_available_networks()
    # networks = ["wifi1", "wifi2", "wifi3"] # for testing only
    networks.append("Back (interface selection)")
    networks.append("Return to installer")
    
    while current_menu == "wifi":
        stdscr.addstr(0, 2, "Please select your network", curses.A_BOLD)

        number_lines = 0

        for idx, option in enumerate(networks):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            if idx >= len(networks)-2:
                idx+=1
            stdscr.addstr(idx + 2, 4, f" {option} ", style)
            number_lines = idx+2

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                selected = (selected - 1) % len(networks)

            case curses.KEY_DOWN:
                selected = (selected + 1) % len(networks) 

            case curses.KEY_ENTER | 10 | 13: 
                match selected:
                    case len(networks) - 1:
                        current_menu = "main" # button return to installer
                    case len(networks) - 2:
                        current_menu = "interfaces" # button "back"
                    case _:
                        menu_password(stdscr, networks[selected])


def menu_password(stdscr, ssid, wrong_password=False):
    global current_screen, interface

    stdscr.clear()
    stdscr.addstr(1, 2, f"Enter password for {ssid}: ")
    if wrong_password:
        stdscr.addstr(0, 2, f"Wrong password for {ssid} !", curses.A_BOLD)
    curses.echo()
    
    stdscr.refresh()
    password = stdscr.getstr(2, 2, 20).decode('utf-8')

    curses.noecho()
    subprocess.run(["iwctl", "station", interface, "connect", ssid, "--passphrase", password ], capture_output=True, text=True, check=True)

    if check_network():
        current_menu = "main"
    else:
        menu_password(stdscr, ssid, True)
    

def menu_interfaces(stdscr):
    global current_menu, interface
    
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    selected = 0
    buttons = get_available_devices()
    buttons.append("Back to installer")

    while current_menu == "interfaces":
        stdscr.addstr(0, 2, "Please select your interface", curses.A_BOLD)

        for idx, option in enumerate(buttons):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            if idx == len(buttons)-1:
                idx+=1
            stdscr.addstr(idx + 2, 4, f" {option} ", style)

        key = stdscr.getch()

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                selected = (selected - 1) % len(buttons)

            case curses.KEY_DOWN:
                selected = (selected + 1) % len(buttons)

            case curses.KEY_ENTER | 10 | 13:
                match selected:
                    case len(buttons) - 1:
                        current_menu = "main"

                    case _:
                        interface = buttons[selected] 
                        current_menu = "wifi"



def menu_main(stdscr):
    global current_menu
    options = ["Configure and Install", "Exit"]
    curses.curs_set(0) 
    stdscr.clear()
    stdscr.refresh()

    if check_network():
        stdscr.addstr(3, 2, "Network: Connected")
    else:
        stdscr.addstr(3, 2, "Network: Not connected")
        stdscr.addstr(4, 2, "Your network isn't working! Please connect your computer to the internet.")
        options.insert(0, "Connect Wifi")

    selected = 0

    while current_menu == "main":
        stdscr.addstr(0, 2, "Welcome! I'm Vulperon Installer!", curses.A_BOLD)
        stdscr.addstr(1, 2, "Now, let's configure some settings!")

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
                match selected:
                    case len(options) - 1:
                        current_menu = "exit"

                    case len(options) - 2:
                        curses.curs_set(0)
                        stdscr.clear()
                        stdscr.refresh()
                        current_menu = "install"

                    case _:
                        current_menu = "interfaces"


# ======= Main Loop =======


def main(stdscr):
    global current_menu

    while True:
        match current_menu:
            case "main":
                menu_main(stdscr)

            case "interfaces":
                menu_interfaces(stdscr)

            case "wifi":
                menu_wifi(stdscr)

            case "exit":
                break

            case "install":
                stdscr.clear()
                stdscr.refresh()
                run_archinstall(stdscr)
                print("Installation done! Please type \"reboot\" in your terminal to boot into your new system!")
                break


curses.wrapper(main)