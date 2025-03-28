#!/bin/bash

apps=("electron34" "avahi-discover" "qvidcap" "bssh" "bvnc" "qv4l2")
app_dir="/usr/share/applications"

for app in "${apps[@]}"; do
    desktop_file="$app_dir/$app.desktop"
    if [[ -f "$desktop_file" ]]; then
        if ! grep -q "^NoDisplay=true$" "$desktop_file"; then
            echo "NoDisplay=true" >> "$desktop_file"
            echo "Added NoDisplay=true to $desktop_file"
        else
            echo "$desktop_file already contains NoDisplay=true"
        fi
    fi
done

echo "Post-Application-Installation configuration done !"

rm -- "$0"