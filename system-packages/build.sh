#!/bin/bash

# build yay and prepare package lists
git clone https://aur.archlinux.org/yay-bin.git
makepkg -si --noconfirm --dir yay-bin
rm -rf yay-bin
mkdir -p /home/builder/mainsys-pkgs /home/builder/subsys-pkgs

# build mainsys aur pkgs
while read -r pkg; do
    echo "Building $pkg...";
    yay -G "$pkg"
    makepkg -sr --noconfirm --nocheck --dir "$pkg"
    cp *.pkg.tar.zst /home/builder/mainsys-pkgs/
    cd ..
    rm -rf "$pkg";
done < mainsys-pkgs.txt

# build subsys aur pkgs
while read -r pkg; do
    echo "Building $pkg...";
    yay -G "$pkg"
    makepkg -sr --noconfirm --nocheck --dir "$pkg"
    cp *.pkg.tar.zst /home/builder/subsys-pkgs/
    cd ..
    rm -rf "$pkg";
done < subsys-pkgs.txt

# dummy install maplemono - we'll copy the built packages later
yay -S --noconfirm maplemono-ttf