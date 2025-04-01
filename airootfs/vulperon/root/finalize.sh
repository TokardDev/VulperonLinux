#!/bin/bash

systemctl enable gdm
systemctl enable bluetooth
systemctl enable cronie
systemctl enable timeshift-firstboot.service

sed -i '/^GRUB_CMDLINE_LINUX_DEFAULT=/ s/"$/ splash"/' /etc/default/grub && grub-mkconfig -o /boot/grub/grub.cfg
sed -i '/^HOOKS=/ s/\b\(encrypt\|sd-encrypt\)\b/plymouth &/' /etc/mkinitcpio.conf

if ! grep -q 'plymouth' /etc/mkinitcpio.conf; then
    sed -i '/^HOOKS=/ s/)/ plymouth)/' /etc/mkinitcpio.conf
fi

plymouth-set-default-theme spinner

mkinitcpio -P

dconf update
echo "Post-install configuration done !"

rm -- "$0"