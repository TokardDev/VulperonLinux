#!/bin/bash

if [ ! -d "/mnt" ]; then
    echo "Error : /mnt is missing."
    exit 1
fi

arch-chroot /mnt pacman -Syu
arch-chroot /mnt /bin/bash -c "/root/download-extensions.sh"
arch-chroot /mnt /bin/bash -c "/root/install-theme.sh"
arch-chroot /mnt /bin/bash -c "/root/finalize.sh"
arch-chroot /mnt /bin/bash -c "/root/post-app-install.sh"