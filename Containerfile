FROM archlinux:latest AS builder

RUN pacman -Syu --noconfirm --needed base-devel git sudo
RUN useradd -m builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/builder

USER builder
WORKDIR /home/builder

RUN git clone https://aur.archlinux.org/yay-bin.git && \
    cd yay-bin && \
    makepkg -si --noconfirm
COPY --chown=builder:builder packages.txt .
RUN mkdir -p /home/builder/packages

RUN while read -r pkg; do \
    echo "Building $pkg..."; \
    yay -G "$pkg" && \
    cd "$pkg" && \
    makepkg -sr --noconfirm --nocheck && \
    cp *.pkg.tar.zst /home/builder/packages/ && \
    cd .. && \
    rm -rf "$pkg"; \
    done < packages.txt

FROM scratch AS ctx
COPY chezmoi/ /system_files/usr/share/tartaria
COPY --from=builder home/builder/packages/ /system_files/packages/
