#!/usr/bin/env python

import curses
import subprocess


def check_network():
    """
    Vérifie si un miroir Arch Linux est joignable en pingant mirror.archlinux.org.
    Retourne True si la connexion fonctionne, sinon False.
    """
    try:
        subprocess.run(
            ["ping", "-c", "1", "archlinux.org"],  # Ping un miroir Arch officiel
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True  # Réseau Arch OK
    except subprocess.CalledProcessError:
        return False  # Réseau Arch KO


def get_available_devices():
    """
    Récupère les périphériques réseau disponibles via iwctl.
    """
    try:
        result = subprocess.run(["iwctl", "device", "list"], capture_output=True, text=True, check=True)
        devices = []
        lines = result.stdout.splitlines()

        # Ignorer les 3 premières lignes
        for line in lines[4:]:
            device = line.split()[0]  # Récupère le nom de l'interface
            devices.append(device)

        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
        return []


def get_available_devices():
    result = subprocess.run(["iwctl", "device", "list"], capture_output=True, text=True, check=True)[3:]
    devices = []
    lines = result.stdout.splitlines()

    for line in lines[3:]:
        device = line.split()[0]  # Récupère le nom de l'interface
        devices.append(device)
    return devices

def get_available_networks(device):
    subprocess.run(["iwctl", "station", device, "scan"], capture_output=True, text=True, check=True)
    result = subprocess.run(["iwctl", "station", device, "get-networks"], capture_output=True, text=True, check=True)[3:]

    networks = []
    lines = result.stdout.splitlines()
    for line in lines[3:]:
        network = line.split()[0]  # Récupère le nom du network
        networks.append(network)
    return networks


def check_network_true():
    return True


def select_network(stdscr, device):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    selected = 0
    networks = get_available_networks()
    networks.append("Back")
    networks.append("Exit")
    
    while True:
        stdscr.addstr(0, 2, "Please select your network", curses.A_BOLD)

        number_lines = 0

        for idx, option in enumerate(networks):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(idx + 2, 4, f" {option} ", style)
            number_lines = idx+2

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(networks)  # Aller à l'option précédente
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(networks)  # Aller à l'option suivante
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected == len(networks)-1:
                print("exit")
            elif selected == len(networks)-2:
                print("Back")
            else:
                try:
                    
                    user_input = stdscr.getstr(number_lines +2 , 2, 40)
                    #subprocess.run(["iwctl", "station", device, "connect", networks[selected], "--passphrase", user_input ], capture_output=True, text=True, check=True)
                    print(user_input)
                    if check_network_true():
                        main()
                    else:
                        stdscr.addstr(number_lines +3, 2, "Possibly wrong password !", curses.A_BOLD)
                except subprocess.CalledProcessError as e:
                    print("Error :", e)





def network_menu(stdscr):
    """
    Connexion à un réseau Wi-Fi via iwctl.
    Demande à l'utilisateur de choisir un réseau Wi-Fi et de saisir un mot de passe.
    """
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    selected = 0
    buttons = get_available_devices()
    buttons.append("Back")
    buttons.append("Exit")

    while True:
        stdscr.addstr(0, 2, "Please select your interface", curses.A_BOLD)

        for idx, option in enumerate(buttons):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(idx + 2, 4, f" {option} ", style)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(buttons)  # Aller à l'option précédente
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(buttons)  # Aller à l'option suivante
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected == len(buttons)-1:
                print("exit")
            elif selected == len(buttons)-2:
                print("Back")
            else:
                select_network(stdscr, buttons[selected])
                
        



def menu(stdscr, network_connected):
    """
    Affiche le menu principal et gère la navigation.
    """
    options = ["Configure and Install", "Exit"]
    curses.curs_set(0)  # Cache le curseur
    stdscr.clear()
    stdscr.refresh()

    # Vérifie si le réseau est connecté
    if network_connected:
            stdscr.addstr(3, 2, "Network: ✅ Connected")
    else:
        stdscr.addstr(3, 2, "Network: ❌ Not connected")
        stdscr.addstr(4, 2, "Your network isn't working! Please connect your computer to the internet.")
        options.insert(0, "Connect Wifi")

    selected = 0

    while True:
        stdscr.addstr(0, 2, "Welcome! I'm Vulperine Installer!", curses.A_BOLD)
        stdscr.addstr(1, 2, "First, let's configure some settings!")

        for idx, option in enumerate(options):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(idx + 6, 4, f" {option} ", style)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)  # Aller à l'option précédente
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)  # Aller à l'option suivante
        elif key in [curses.KEY_ENTER, 10, 13]:
            return selected


def run_archinstall():
    """
    Lance l'installation d'Arch Linux avec les paramètres spécifiés.
    """
    subprocess.run([
        "archinstall",
        "--script", "vulperine-archiso",
        "--config", ".user_configuration.json",
        "--creds", ".user_credentials.json"
    ])


def main():
    """
    Point d'entrée principal du programme.
    """
    network_connected = check_network()  # Vérifie l'état du réseau
    choice = curses.wrapper(lambda stdscr: menu(stdscr, network_connected))  # Lance le menu principal dans l'environnement curses

    if (choice == 0 and network_connected) or (choice == 1 and not network_connected):
        # Démarre l'installation si l'option "Configure and Install" est choisie et que le réseau est connecté
        print("\nStarting installation...")
        run_archinstall()
    elif choice == 0:
        # Si le réseau n'est pas connecté, lance le menu de configuration réseau
        print("\nOpening network configuration...")
        curses.wrapper(network_menu)
    else:
        # Quitte l'installateur
        print("\nExiting installer.")


if __name__ == "__main__":
    main()
