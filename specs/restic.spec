%global debug_package %{nil}

Name:           restic
Version:        0.18.0
Release:        1%{?dist}
Summary:        A modern backup program that is fast, efficient and secure

License:        BSD-2-Clause
URL:            https://restic.net/
Source0:        https://github.com/restic/restic/archive/v%{version}.tar.gz

BuildRequires:  go >= 1.16

%description
restic is a modern backup program that is fast, efficient and secure.
It supports saving your data locally or to various cloud services.

%prep
%autosetup -n restic-%{version}

%build
go build -o restic .

%install
install -Dm755 restic %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}

%changelog
%autochangelog