#!/bin/bash

EXTENSIONS_LIST=("7065" "307" "1010" "97")

VERSION_GNOME=$(gnome-shell --version | awk '{print $3}' | cut -d'.' -f1)

EXTENSIONS_DIR="/usr/share/gnome-shell/extensions/"

CURRENT_EXTENSIONS=$(dconf read /org/gnome/shell/enabled-extensions | tr -d "[]'")

for ID_EXTENSION in "${EXTENSIONS_LIST[@]}"; do
    echo "Installing extension $ID_EXTENSION..."

    EXT_INFO=$(curl -s "https://extensions.gnome.org/extension-info/?pk=$ID_EXTENSION&shell_version=$VERSION_GNOME")
    
    DL_URL=$(echo "$EXT_INFO" | grep -o '"download_url":[^,]*' | cut -d'"' -f4)
    UUID=$(echo "$EXT_INFO" | grep -o '"uuid":[^,]*' | cut -d'"' -f4)

    if [ -z "$DL_URL" ] || [ -z "$UUID" ]; then
        echo "Can't download extension $ID_EXTENSION for GNOME $VERSION_GNOME"
        continue
    fi

    wget "https://extensions.gnome.org$DL_URL" -O "$UUID.zip"

    EXT_DIR="$EXTENSIONS_DIR/$UUID"
    mkdir -p "$EXT_DIR"
    unzip -o "$UUID.zip" -d "$EXT_DIR"
    rm "$UUID.zip"

    sudo find "$EXT_DIR" -type d -exec sudo chmod 755 {} \;

    sudo find "$EXT_DIR" -type f -exec sudo chmod 644 {} \;

    if [ "$ID_EXTENSION" -eq 1010 ]; then
        SCHEMA_FILE="$EXT_DIR/schemas/org.gnome.shell.extensions.arch-update.gschema.xml"
        
        if [ -f "$SCHEMA_FILE" ]; then
            echo "Modifying schema for extension $ID_EXTENSION..."
            # Remplacer "gnome-terminal" par "kgx" dans le fichier XML
            sudo sed -i 's/gnome-terminal/kgx/g' "$SCHEMA_FILE"
        else
            echo "Schema file not found for extension $ID_EXTENSION"
        fi
    fi

    if [ -d "$EXT_DIR/schemas" ]; then
        echo "Compiling for $UUID..."
        glib-compile-schemas "$EXT_DIR/schemas"
    fi

    # Ajouter à la liste des extensions activées
    if [[ "$CURRENT_EXTENSIONS" != *"$UUID"* ]]; then
        CURRENT_EXTENSIONS="['$UUID', ${CURRENT_EXTENSIONS// /}]"
    fi
done

dconf write /org/gnome/shell/enabled-extensions "$CURRENT_EXTENSIONS"

echo "Extensions installed !"

