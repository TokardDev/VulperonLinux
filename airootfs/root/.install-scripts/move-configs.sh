#!/bin/bash

cp -r -f /vulperon/* /mnt/archinstall/
rm -r /mnt/archinstall/usr/share/pixmaps/archlinux*

# Vérifier si le déplacement a réussi
if [ $? -eq 0 ]; then
    echo "Déplacement terminé avec succès."
else
    echo "Erreur lors du déplacement."
    exit 1
fi

