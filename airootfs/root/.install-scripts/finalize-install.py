import curses
import subprocess

current_menu = "main"
pacman_packages = []
pacman_packages_gpu = []
flatpak_packages = []

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

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options) 
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected == 0:
                current_menu = "gpu"
            else:
                current_menu = "exit"

def menu_gpu(stdscr):
    global current_menu, pacman_packages_gpu

    # Définition des options de GPU et leurs paquets associés
    gpu_options = [
        ("Mesa (Open Source)", False, "mesa"),  # Paquet pour Mesa
        ("NVIDIA Proprietary (Recommended for NVIDIA)", False, "nvidia"),  # Paquet pour NVIDIA propriétaire
        ("Nouveau (NVIDIA Open Source)", False, "nouveau-dri"),  # Paquet pour Nouveau
        ("AMD (Open Source)", False, "xf86-video-amdgpu"),  # Paquet pour AMD
        ("Intel (Open Source)", False, "xf86-video-intel")  # Paquet pour Intel
    ]
    
    curses.curs_set(0)  # Cache le curseur
    stdscr.clear()
    stdscr.refresh()

    selected = 0

    while current_menu == "gpu":
        stdscr.clear()

        # Header
        stdscr.addstr(0, 2, "Choose the GPU driver(s) to install", curses.A_BOLD)
        stdscr.addstr(2, 4, "Use arrow keys to navigate, space to select, Enter to confirm.")
        
        # Afficher les options avec cases à cocher
        for idx, (option, selected_flag, _) in enumerate(gpu_options):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            checkbox = "[x]" if selected_flag else "[ ]"
            stdscr.addstr(idx + 4, 4, f"{checkbox} {option}", style)

        # Capturer l'entrée clavier
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(gpu_options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(gpu_options)
        elif key == 32:  # Espace pour basculer la sélection
            option, selected_flag, package = gpu_options[selected]
            gpu_options[selected] = (option, not selected_flag, package)  # Bascule la sélection
        elif key in [curses.KEY_ENTER, 10, 13]:
            # Ajouter les paquets sélectionnés dans pacman_packages
            selected_drivers = [option for option, selected_flag, _ in gpu_options if selected_flag]
            pacman_packages_gpu = [package for option, selected_flag, package in gpu_options if selected_flag]

            current_menu = "recommended_packages"  # Revenir au menu principal

        stdscr.refresh()


def menu_packages(stdscr):
    global current_menu, pacman_packages

    # Liste des applications recommandées avec leurs paquets correspondants
    recommended_packages = [
        ("Steam", False, "steam"),
        ("Visual Studio Code (Open Source Arch)", False, "code"),
        ("VirtManager & Qemu", False, "virt-manager qemu-full"),
        ("Firefox", False, "firefox"),
        ("VLC", False, "vlc"),
        ("GIMP", False, "gimp"),
        ("Audacity", False, "audacity"),
        ("Chromium", False, "chromium"),
        ("Thunderbird", False, "thunderbird"),
        ("OBS Studio", False, "obs-studio")
    ]
    
    curses.curs_set(0)  # Cache le curseur
    stdscr.clear()
    stdscr.refresh()

    selected = 0

    while current_menu == "recommended_packages":
        stdscr.clear()

        # Header
        stdscr.addstr(0, 2, "Choose the recommended packages to install", curses.A_BOLD)
        stdscr.addstr(0, 2, "You'll be able to install more packages after reboot with \"sudo pacman -S <package>\" ", curses.A_BOLD)
        stdscr.addstr(2, 4, "Use arrow keys to navigate, space to select, Enter to confirm.")
        
        # Afficher les options avec cases à cocher
        for idx, (option, selected_flag, _) in enumerate(recommended_packages):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            checkbox = "[x]" if selected_flag else "[ ]"
            stdscr.addstr(idx + 4, 4, f"{checkbox} {option}", style)

        # Capturer l'entrée clavier
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(recommended_packages)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(recommended_packages)
        elif key == 32:  # Espace pour basculer la sélection
            option, selected_flag, package = recommended_packages[selected]
            recommended_packages[selected] = (option, not selected_flag, package)  # Bascule la sélection
        elif key in [curses.KEY_ENTER, 10, 13]:
            # Ajouter les paquets sélectionnés dans pacman_packages
            selected_apps = [option for option, selected_flag, _ in recommended_packages if selected_flag]
            pacman_packages.extend([package for option, selected_flag, package in recommended_packages if selected_flag])
        
            current_menu = "flatpak_packages"

        stdscr.refresh()


def menu_flatpak(stdscr):
    global current_menu, flatpak_packages

    # Liste des applications Flatpak recommandées avec leurs identifiants
    flatpak_apps = [
        ("Discord", False, "com.discordapp.Discord"),
        ("GitHub Desktop", False, "io.github.shiftey.Desktop"),
        ("Brave Browser", False, "com.brave.Browser"),
        ("Deezer", False, "dev.aunetx.deezer"),
        ("Spotify", False, "com.spotify.Client"),
        ("Telegram", False, "org.telegram.desktop"),
        ("Materialgram (Telegram client)", False, "io.github.kukuruzka165.materialgram")
    ]

    curses.curs_set(0)  # Cache le curseur
    stdscr.clear()
    stdscr.refresh()

    selected = 0

    while current_menu == "flatpak_packages":
        stdscr.clear()

        # Header
        stdscr.addstr(0, 2, "Choose the Flatpak apps to install", curses.A_BOLD)
        stdscr.addstr(2, 4, "Use arrow keys to navigate, space to select, Enter to confirm.")
        
        # Afficher les options avec cases à cocher
        for idx, (option, selected_flag, _) in enumerate(flatpak_apps):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            checkbox = "[x]" if selected_flag else "[ ]"
            stdscr.addstr(idx + 4, 4, f"{checkbox} {option}", style)

        # Capturer l'entrée clavier
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(flatpak_apps)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(flatpak_apps)
        elif key == 32:  # Espace pour basculer la sélection
            option, selected_flag, app = flatpak_apps[selected]
            flatpak_apps[selected] = (option, not selected_flag, app)  # Bascule la sélection
        elif key in [curses.KEY_ENTER, 10, 13]:
            # Ajouter les applications sélectionnées dans flatpak_packages
            selected_apps = [option for option, selected_flag, _ in flatpak_apps if selected_flag]
            flatpak_packages.extend([app for option, selected_flag, app in flatpak_apps if selected_flag])
        
            current_menu = "ask_install"  # Revenir au menu principal

        stdscr.refresh()


def menu_install(stdscr):
    global current_menu, pacman_packages, flatpak_packages

    curses.curs_set(0)  # Cache le curseur
    stdscr.clear()
    stdscr.refresh()

    # Contenu des paquets à afficher
    pacman_content = " ".join(pacman_packages + pacman_packages_gpu) if pacman_packages or pacman_packages_gpu else "No package selected."
    flatpak_content = " ".join(flatpak_packages) if flatpak_packages else "No Flatpak application selected."

    # Afficher le contenu des paquets
    stdscr.addstr(0, 2, "The following packages will be installed:")
    stdscr.addstr(2, 2, f"Pacman: {pacman_content}")
    stdscr.addstr(3, 2, f"Flatpak: {flatpak_content}")

    # Demander si l'utilisateur veut installer
    stdscr.addstr(5, 2, "Do you want to install these packages?", curses.A_BOLD)

    options = ["No / Reconfigure", "Yes"]
    selected = 0

    # Affichage des boutons "Oui" et "Non"
    while current_menu == "ask_install":
        for idx, option in enumerate(options):
            style = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(7 + idx, 4, f" {option} ", style)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [curses.KEY_ENTER, 10, 13]:
            if selected == 1:  # Si l'utilisateur choisit "Oui"
                # Commande d'installation pour pacman
                pacman_command = f"pacman -S --noconfirm {' '.join(pacman_packages + pacman_packages_gpu)}"
                
                # Commande d'installation pour flatpak
                flatpak_command = f"flatpak install --assumeyes {' '.join(flatpak_packages)}"

                # Exécution des commandes dans le chroot
                try:
                    # Installation des paquets Pacman dans le chroot
                    subprocess.run(f"arch-chroot /mnt/archinstall {pacman_command}", shell=True, check=True)

                    # Installation des applications Flatpak dans le chroot
                    subprocess.run(f"arch-chroot /mnt/archinstall {flatpak_command}", shell=True, check=True)

                    print("Packages installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error during installation: {e}")
                
                sys.exit()
            else:
                current_menu = "main"

            stdscr.clear()
            stdscr.refresh()
            break

        stdscr.refresh()


def main(stdscr):
    global current_menu

    while True:
        if current_menu == "main":
            menu_main(stdscr)
        elif current_menu == "gpu":
            menu_gpu(stdscr)
        elif current_menu == "recommended_packages":
            menu_packages(stdscr)
        elif current_menu == "flatpak_packages":
            menu_flatpak(stdscr)
        elif current_menu == "ask_install":
            menu_install(stdscr)
        elif current_menu == "exit":
            return


curses.wrapper(main)