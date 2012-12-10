%define debug_package	%{nil}

%define oname	elisa

# It's the same for releases, but different for pre-releases: please
# don't remove, even if it seems superfluous - AdamW 2008/03
%define fversion	%{version}

Summary:	Media center written in Python
Name:		moovida
Version:	1.0.9
Release:	3
# For bzr:
# bzr branch lp:~elisa-developers/elisa/relook
Source0:	http://www.moovida.com/media/public/%{name}-%{version}.tar.gz
# Disable automatic updates - AdamW 2009/02
Patch0:		moovida-1.0.1-disable_plugin_updates.patch
License:	GPLv3 and MIT
Group:		Graphical desktop/Other
URL:		http://www.moovida.com/
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python-setuptools
BuildRequires:	python-devel
BuildRequires:	python-twisted
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	gstreamer0.10-python
Requires:	moovida-plugins-good = %{version}
Requires:	moovida-plugins-bad = %{version}
Requires:	moovida-core = %{version}
Suggests:	moovida-plugins-ugly = %{version}
Suggests:	gstreamer0.10-libvisual
%rename	elisa

%description
Moovida is a project to create an open source cross platform media center 
solution. Moovida runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Moovida will also 
interoperate with devices following the DLNA standard like Intel's ViiV 
systems.

Moovida was formerly know as Elisa.

%package core
Summary:	Media center written in Python: core files
Group:		Development/Python
Requires:	pigment-python
Requires:	python-imaging
Requires:	python-twisted
Requires:	python-twisted-web2
Requires:	gnome-python-extras
Requires:	gstreamer0.10-python
Requires:	gstreamer0.10-plugins-base
Requires:	python-sqlite2
Requires:	pyxdg
Requires:	python-pkg-resources
Suggests:	gstreamer0.10-plugins-good
Suggests:	gstreamer0.10-plugins-bad
Suggests:	python-gpod
Suggests:	python-dbus
%rename	elisa-core = %{version}-%{release}

%description core
Moovida is a project to create an open source cross platform media center 
solution. Moovida runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Moovida will also 
interoperate with devices following the DLNA standard like Intel's ViiV 
systems. This package contains the core Python files for Moovida. It is
split from the binaries for packaging reasons.

Moovida was formerly known as Elisa.

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1 -b .update_disable

%build

%install
python setup.py install --root=%{buildroot} --single-version-externally-managed --compile --optimize=2

pushd %{buildroot}%{_bindir}
ln -s %{oname} %{name}
popd

# Install some stuff manually because the build process can't.
install -D -m644 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# Generate and install 32x32 and 16x16 icons.
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,16x16}/apps

convert -scale 32 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Menu file
rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop
rm -f %{buildroot}%{_datadir}/applications/%{name}-mobile.desktop
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=Moovida Media Center
Comment=Play movies and songs on TV with remote
Exec=%{oname} %U
StartupWMClass=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;AudioVideo;Audio;Video;Player;X-MandrivaLinux-CrossDesktop;
X-Osso-Service=com.fluendo.elisa
EOF

#don't want these
rm -rf %{buildroot}%{py_puresitedir}/mswin32
rm -f %{buildroot}%{_datadir}/pixmaps/%{name}.png
rm -f %{buildroot}%{_datadir}/icons/%{name}.png
rm -rf %{buildroot}%{_datadir}/mobile-basic-flash

# as there's three plugins packages that aren't interdependent, best
# let the core package own the plugins dir - AdamW 2008/02
mkdir -p %{buildroot}%{py_puresitedir}/%{name}/plugins

%files
%doc AUTHORS FAQ FIRST_RUN NEWS RELEASE TRANSLATORS
%{_bindir}/%{oname}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/dbus-1/services/*.service

%files core
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{oname}
%{py_puresitedir}/%{oname}-%{fversion}-py%{py_ver}-nspkg.pth
%{py_puresitedir}/%{oname}-%{fversion}-py%{py_ver}.egg-info


