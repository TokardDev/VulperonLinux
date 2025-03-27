#!/usr/bin/env python

import curses
import subprocess

current_menu = "main"
interface = None

def check_network():
    try:
        subprocess.run(
            ["ping", "-c", "1", "archlinux.org"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True  # OK
    except subprocess.CalledProcessError:
        return False 


def get_available_devices(): # not tested yet
    try:
        result = subprocess.run(["iwctl", "device", "list"], capture_output=True, text=True, check=True)
        devices = []
        lines = result.stdout.splitlines()

        for line in lines[4:]:
            device = line.split()[0]  # get interfa
            devices.append(device)

        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
        return []


def run_archinstall():
    """
    Lance l'installation d'Arch Linux avec les paramètres spécifiés.
    """
    subprocess.run([
        "archinstall",
        "--script", "vulperon-archiso",
        "--config", "/root/.install-scripts/user_configuration.json",
        "--creds", "/root/.install-scripts/user_credentials.json"
    ])
    subprocess.run(["/root/.install-scripts/move-configs.sh"])
    subprocess.run(["/root/.install-scripts/post-install.sh"])
    subprocess.run(["/root/.install-scripts/finalize-install.py"])
    print("Installation Complete !")


def get_available_networks(device): # not tested yet
    subprocess.run(["iwctl", "station", device, "scan"], capture_output=True, text=True, check=True)
    result = subprocess.run(["iwctl", "station", device, "get-networks"], capture_output=True, text=True, check=True)[3:]

    networks = []
    lines = result.stdout.splitlines()
    for line in lines[3:]:
        network = line.split()[0] # get network name
        networks.append(network)
    return networks


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

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(networks)  # Aller à l'option précédente
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(networks)  # Aller à l'option suivante
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected == len(networks)-1:
                current_menu = "main"
            elif selected == len(networks)-2:
                current_menu = "interfaces"
            else:
                menu_password(stdscr, networks[selected])

def menu_password(stdscr, ssid, wrong_password=False):
    global current_screen, interface

    stdscr.clear()
    stdscr.addstr(1, 2, f"Enter password for {ssid}: ")
    if wrong_password:
        stdscr.addstr(0, 2, f"Wrong password for {ssid} !", curses.A_BOLD)
    curses.echo()
    
    stdscr.refresh()
    password = stdscr.getstr(2, 2, 20).decode('utf-8')  # Lire le mot de passe

    curses.noecho()
    #subprocess.run(["iwctl", "station", interface, "connect", ssid, "--passphrase", password ], capture_output=True, text=True, check=True)
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
    #buttons = ["wifi","ethernet"]
    buttons.append("Back to installer")

    while current_menu == "interfaces":
        stdscr.addstr(0, 2, "Please select your interface", curses.A_BOLD)

        for idx, option in enumerate(buttons):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            if idx == len(buttons)-1:
                idx+=1
            stdscr.addstr(idx + 2, 4, f" {option} ", style)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(buttons)  # Aller à l'option précédente
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(buttons)  # Aller à l'option suivante
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected == len(buttons)-1:
                current_menu = "main"
            else:
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

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options) 
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected == len(options)-1:
                current_menu = "exit"
            elif selected == len(options)-2:
                run_archinstall()
            else:
                current_menu = "interfaces"



def main(stdscr):
    global current_menu

    while True:
        if current_menu == "main":
            menu_main(stdscr)
        elif current_menu == "interfaces":
            menu_interfaces(stdscr)
        elif current_menu == "wifi":
            menu_wifi(stdscr)
        elif current_menu == "exit":
            return


curses.wrapper(main)