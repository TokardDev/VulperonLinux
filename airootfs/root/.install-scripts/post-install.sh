#!/bin/bash

if [ ! -d "/mnt/archinstall" ]; then
    echo "Error : /mnt/archinstall is missing."
    exit 1
fi

arch-chroot /mnt/archinstall /bin/bash -c "/root/finalize.sh"