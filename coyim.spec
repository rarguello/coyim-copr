%define debug_package %{nil}

Name:           coyim
Version:        0.3.11
Release:        0.2
Summary:        A safe and secure chat client
License:        GPLv3+
URL:            https://coy.im
Source0:        https://github.com/coyim/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        coyim.desktop

ExclusiveArch:  %{go_arches}
BuildRequires:  compiler(go-compiler)
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel

%description
A safe an secure chat client.

%prep
%setup -q

%build
mkdir -p src/github.com/coyim
ln -s ../../../ src/github.com/coyim/coyim

export GTK_VERSION=$(pkg-config --modversion gtk+-3.0 | tr . _ | cut -d '_' -f 1-2)
export GTK_BUILD_TAG=gtk_${GTK_VERSION}
./gen_version_file.sh ignore v%{version}

export GOPATH=$(pwd):%{gopath}
go build -tags ${GTK_BUILD_TAG} -o bin/coyim github.com/coyim/coyim

%install
install -d %{buildroot}/%{_bindir}
install -p -m 755 bin/%{name} %{buildroot}/%{_bindir}

for size in 16x16 32x32 128x128 256x256 512x512; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${size}/apps
  install -p build/mac-bundle/coy.iconset/icon_${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/%{name}.png
done

desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE1}

%files
%license LICENSE
%doc CONTRIBUTING.md DOWNLOADING.md PHILOSOPHY.md README.md RELEASE.md REPRODUCIBILITY.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*

%changelog
* Tue Apr 30 2019 Ricardo Arguello <ricardo.arguello@gmail.com> - 0.3.11-0.2
- Fix vendor directory management

* Wed Apr 24 2019 Ricardo Arguello <ricardo.arguello@gmail.com> - 0.3.11-0.1
- Initial release
