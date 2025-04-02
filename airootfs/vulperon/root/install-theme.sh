#!/bin/bash

# wip

repo_dir="/usr/local/Colloid-gtk-theme"

git clone https://github.com/vinceliuice/Colloid-gtk-theme.git "$repo_dir"

chmod -R 777 "$repo_dir"

for user_home in /home/*; do
    if [ -d "$user_home" ]; then
        cp -r "$repo_dir" "$user_home/Colloid-gtk-theme"
        chmod -R 777 "$user_home/Colloid-gtk-theme"
        sudo -u $(basename "$user_home") "$user_home/Colloid-gtk-theme/install.sh" -l fixed --color dark --tweaks rimless
        rm -rf "$user_home/Colloid-gtk-theme"
        chsh -s /bin/zsh "$(basename "$user_home")"
    fi
done

rm -rf "$repo_dir"

global_zsh="/usr/local/share/oh-my-zsh"
skel_zshrc="/etc/skel/.zshrc"

git clone https://github.com/ohmyzsh/ohmyzsh.git "$global_zsh"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "/usr/local/share/oh-my-zsh/custom/themes/powerlevel10k"

cp "$global_zsh/templates/zshrc.zsh-template" "$skel_zshrc"

sed -i 's/^ZSH_THEME=.*/ZSH_THEME="powerlevel10k\/powerlevel10k"/' "$skel_zshrc"
sed -i 's|^export ZSH=.*|export ZSH="/usr/local/share/oh-my-zsh"|' "$skel_zshrc"
grep -q "export ZSH_CACHE_DIR=\$HOME/.cache/ohmyzsh" "$skel_zshrc" || echo "export ZSH_CACHE_DIR=\$HOME/.cache/ohmyzsh" | tee -a "$skel_zshrc"

for user in $(ls /home); do
    home_dir="/home/$user"
    user_zshrc="$home_dir/.zshrc"
    
    cp "$skel_zshrc" "$user_zshrc"
    chown "$user:$user" "$user_zshrc"
done

wget -qO- https://git.io/papirus-icon-theme-install | sh

echo "Installation et configuration terminées !"