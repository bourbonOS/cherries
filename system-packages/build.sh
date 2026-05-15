#!/bin/bash

JOBS=$(wc -l < "$1")
parallel --tag --halt now,fail=1 -j "$JOBS" '
    echo "Building {}..."
    yay -G "{}" &&
    cd "{}" &&
    makepkg -sr --noconfirm --nocheck &&
    cp *.pkg.tar.zst /home/builder/mainsys-pkgs/ &&
    cd /home/builder &&
    rm -rf "{}"
' :::: "$1"