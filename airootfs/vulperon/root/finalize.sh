#!/bin/bash

systemctl enable gdm

dconf update
echo "Post-install configuration done !"

rm -- "$0"