#!/bin/bash

# wip

repo_dir="/usr/local/Colloid-gtk-theme"

git clone https://github.com/vinceliuice/Colloid-gtk-theme.git "$repo_dir"

sudo chmod -R 777 "$repo_dir"

for user_home in /home/*; do
    if [ -d "$user_home" ]; then
        cp -r "$repo_dir" "$user_home/Colloid-gtk-theme"
        sudo chmod -R 777 "$user_home/Colloid-gtk-theme"
        sudo -u $(basename "$user_home") "$user_home/Colloid-gtk-theme/install.sh" -l fixed --color dark --tweaks rimless
        rm -rf "$user_home/Colloid-gtk-theme"
    fi
done

rm -rf "$repo_dir"