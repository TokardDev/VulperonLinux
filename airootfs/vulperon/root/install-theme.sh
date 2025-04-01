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
        sudo chsh -s /bin/zsh "$(basename "$user_home")"
    fi
done

rm -rf "$repo_dir"

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "/usr/local/share/oh-my-zsh/custom/themes/powerlevel10k"

global_zsh="/usr/local/share/oh-my-zsh"
skel_zshrc="/etc/skel/.zshrc"

if [ ! -d "$global_zsh" ]; then
    sudo git clone https://github.com/ohmyzsh/ohmyzsh.git "$global_zsh"
fi

sudo cp "$global_zsh/templates/zshrc.zsh-template" "$skel_zshrc"


grep -q "export ZSH=$global_zsh" "$skel_zshrc" || echo "export ZSH=$global_zsh" | sudo tee -a "$skel_zshrc"
sed -i 's/^ZSH_THEME=.*$/ZSH_THEME="powerlevel10k/powerlevel10k"/' "$skel_zshrc"
grep -q "export ZSH_CACHE_DIR=\$HOME/.cache/ohmyzsh" "$skel_zshrc" || echo "export ZSH_CACHE_DIR=\$HOME/.cache/ohmyzsh" | sudo tee -a "$skel_zshrc"

for user in $(ls /home); do
    home_dir="/home/$user"
    user_zshrc="$home_dir/.zshrc"
    
    sudo cp "$skel_zshrc" "$user_zshrc"
    sudo chown "$user:$user" "$user_zshrc"
    grep -q "source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme" "$user_zshrc" || \
    echo "source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme" | sudo tee -a "$user_zshrc"
    
done

echo "Installation et configuration terminées !"