#!/bin/bash

cp -r -f /vulperon/* /mnt/
rm -r /mnt/usr/share/pixmaps/archlinux*

# Check if the move was successful
if [ $? -eq 0 ]; then
    echo "Move completed successfully."
else
    echo "Error during the move."
    exit 1
fi


