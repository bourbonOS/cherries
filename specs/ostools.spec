%define debug_package %{nil}

Name:           ostools
Version: 1.2.5
Release: 1%{?dist}
Summary:        OS tools for bourbonOS

License:        GPLv3
URL:            https://github.com/bourbonOS/os-tools
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

%description
ostools is a collection of tools made specifically for bourbonOS.

%package cherry
Summary:        baseOS managment tool
Requires:       bash
Requires:       ostools-pesticide

%description cherry
cherry is a tool for managing the baseOS and containers.

%package synergy
Summary:        Wrapper for nix
Requires:       bash

%description synergy
synergy is a wrapper for nix that provides a more user-friendly syntax.

%package pesticide
Summary:        FSguard for bourbonOS
Requires:       bash

%description pesticide
pesticide is a tool for hashing and verifying enrolled directories. Does NOT provide live protection.

%package homefs
Summary:        Home encryption tool
Requires:       bash

%description homefs
homefs is a tool for backing up and encrypting your /var/home directory.

%prep
%autosetup -n os-tools-%{version}

%install
mkdir -p %{buildroot}/usr/{libexec/{pesticide,homefs},{lib/systemd/system,bin}}/
mkdir -p %{buildroot}/etc/{containerconf,pesticide.d}
chmod +x cherry/src/cherry
chmod +x synergy/src/synergy
chmod +x pesticide/src/{check,enroll,status,version}
chmod +x homefs/src/homefs-init
install -Dpm755 cherry/src/cherry %{buildroot}/usr/bin/
install -Dpm755 synergy/src/synergy %{buildroot}/usr/bin/
install -Dpm755 pesticide/src/{check,enroll,status,version} %{buildroot}/usr/libexec/pesticide/
install -Dpm755 homefs/src/homefs-init %{buildroot}/usr/libexec/homefs
cp -r cherry/src/files/{*,.cherry} %{buildroot}/etc/containerconf/
cp -r homefs/files/* %{buildroot}/usr/lib/systemd/system/
cp pesticide/src/files/pesticide.conf %{buildroot}/etc/pesticide.d/

%posttrans -n ostools-homefs
/usr/bin/systemctl enable homefs-setup.service

%files cherry
/usr/bin/cherry
/etc/containerconf/*
/etc/containerconf/.cherry/*

%files synergy
/usr/bin/synergy

%files pesticide
/usr/libexec/pesticide/*
/etc/pesticide.d/pesticide.conf

%files homefs
/usr/libexec/homefs/homefs-init
/usr/lib/systemd/system/*

%changelog
%autochangelog
