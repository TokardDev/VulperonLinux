#!/bin/bash

systemctl enable gdm
systemctl enable bluetooth
systemctl enable cronie
systemctl enable timeshift-firstboot.service

dconf update
echo "Post-install configuration done !"

rm -- "$0"