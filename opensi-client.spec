%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define	oname	opensi

Summary:	OpenSi client
Name:		%{oname}-client
Version:	3.4
Release:	19
License:	GPLv2+
Group:		Office
Url:		http://opensi.org/
Source0:	http://download.gna.org/opensi/opensi-client/3.4/%{name}-%{version}.tgz
BuildRequires:	firefox-devel
Requires:	firefox >= %{firefox_epoch}:%{firefox_version}
Requires:	libopensi

%description
Client for OpenSi.

%prep
%setup -q -n %{oname}

%build

%install
# Jar for the translation
mkdir -p %{buildroot}%{firefox_mozillapath}/chrome/
cp -r `pwd`  %{buildroot}%{firefox_mozillapath}/chrome/
# installed-chrome.txt addition
mkdir -p %{buildroot}%{firefox_mozillapath}/chrome/rc.d/
cat << EOF > %{buildroot}%{firefox_mozillapath}/chrome/rc.d/10_%{oname}.txt
content,install,url,resource:/chrome/opensi/content/opensi/
EOF

mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=firefox -chrome chrome://opensi/content/login.xul
Icon=finances_section
Categories=Office;Finance;
Name=OpenSi
Comment=OpenSi client
EOF

%files
%{firefox_mozillapath}/chrome/%{oname}
%{firefox_mozillapath}/chrome/rc.d/10_%{oname}.txt
%{_datadir}/applications/mandriva-%{name}.desktop

