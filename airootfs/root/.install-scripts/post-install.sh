#!/bin/bash

if [ ! -d "/mnt/archinstall" ]; then
    echo "Error : /mnt/archinstall is missing."
    exit 1
fi

arch-chroot /mnt/archinstall pacman -Syu
arch-chroot /mnt/archinstall /bin/bash -c "/root/download-extensions.sh"
arch-chroot /mnt/archinstall /bin/bash -c "/root/install-theme.sh"
arch-chroot /mnt/archinstall /bin/bash -c "/root/finalize.sh"
arch-chroot /mnt/archinstall /bin/bash -c "/root/post-app-install.sh"