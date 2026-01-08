FROM archlinux:latest

RUN pacman -Syu --noconfirm --needed base-devel git sudo
RUN useradd -m builduser && \
    echo "builduser ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/builduser

USER builduser
WORKDIR /home/builduser

RUN git clone https://aur.archlinux.org/yay-bin.git && \
    cd yay-bin && \
    makepkg -si --noconfirm
COPY --chown=builduser:builduser packages.txt .
RUN mkdir -p /home/builduser/output

RUN while read -r pkg; do \
    [[ -z "$pkg" || "$pkg" == #* ]] && continue; \
    echo "Building $pkg..."; \
    yay -G "$pkg" && \
    cd "$pkg" && \
    makepkg -sr --noconfirm && \
    cp *.pkg.tar.zst /home/builduser/output/ && \
    cd .. && \
    rm -rf "$pkg"; \
    done < packages.txt

FROM scratch AS ctx
COPY chezmoi/ /system_files/usr/share/tartaria
COPY --from=builder home/builder/packages/ /system_files/packages/
