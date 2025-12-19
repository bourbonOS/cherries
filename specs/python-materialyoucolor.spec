## START: Set by rpmautospec
## (rpmautospec version 0.8.1)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%bcond_without debug

%global pypi_name materialyoucolor
%global repo_name %{pypi_name}-python
%global pkgname python3-%{pypi_name}
%global _version 2.0.10
%global commit0 36bd0f433ce9441703b8c4b2f25803e379c16a08
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 1
%if %{without debug}
%global debug_package %{nil}
%endif

Name:           python-%{pypi_name}
Version:        %{_version}%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        %autorelease -b5
Summary:        Material You color algorithms for Python!
License:        MIT
URL:            https://github.com/T-Dynamos/materialyoucolor-python
Source0:        %{url}/archive/%{commit0}/%{repo_name}-%{commit0}.tar.gz
Patch0:         %{name}.patch

#ExclusiveArch:  x86_64

BuildRequires:  python-rpm-macros
BuildRequires:  fdupes

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3dist(setuptools) >= 61.0.0
BuildRequires:  python3-installer
BuildRequires:  python3dist(wheel) >= 0.37.1
%if 0%{?fedora}
BuildRequires:  python3-pip
%endif
BuildRequires:  python3dist(regex)
BuildRequires:  python3dist(poetry)
%if %{with debug}
BuildRequires:  glibc-devel

Requires:       glibc
Requires:       libgcc
%endif
Requires:       python3
Requires:       python3dist(pillow)

%description
Material You color algorithms for Python!

%package -n %{pkgname}
Summary:        %{summary}

%description -n %{pkgname}
%{summary}

%prep
%autosetup -p1 -n %{repo_name}-%{commit0}

%build
# 原命令 python -m build --wheel --no-isolation
%pyproject_wheel

%install
# 原命令 python -m installer --destdir=%%{buildroot} dist/*.whl
%pyproject_install
%pyproject_save_files %{pypi_name}
%fdupes %{buildroot}%{$python3_sitearch}/%{pypi_name}/

%check
%pyproject_check_import

%files -n %{pkgname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
%autochangelog
