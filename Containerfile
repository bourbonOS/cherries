FROM archlinux:latest AS builder

RUN pacman -Syu --noconfirm --needed base-devel git sudo
RUN useradd -m builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/builder

USER builder
WORKDIR /home/builduser

RUN git clone https://aur.archlinux.org/yay-bin.git && \
    cd yay-bin && \
    makepkg -si --noconfirm
RUN mkdir -p /home/builder/packages
RUN yay -S --buildonly --noconfirm \
    iio-niri \
    warehouse-git \
    jetbrains-gateway \
    jre-jetbrains \
    maplemono-otf
RUN find . -name "*.pkg.tar.zst" -exec cp {} /home/builder/packages/ \;

FROM scratch AS ctx
COPY chezmoi/ /system_files/usr/share/tartaria
COPY --from=builder home/builder/packages/ /system_files/packages/