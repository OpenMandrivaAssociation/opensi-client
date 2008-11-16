%define	oname	opensi
%define name	%{oname}-client
%define version	3.4
%define firefox_version %(rpm -q --whatprovides mozilla-firefox --queryformat %{VERSION})
%define firefox_epoch %(rpm -q --whatprovides mozilla-firefox --queryformat %{EPOCH})
%define mozillalibdir %{_libdir}/firefox-%{firefox_version}
%define	Summary	OpenSi client

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%mkrel 5
Source0:	http://download.gna.org/opensi/opensi-client/3.4/%name-%version.tgz
License:	GPLv2+
Group:		Office
Url:		http://opensi.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	mozilla-firefox
Requires(pre):	mozilla-firefox = %{firefox_epoch}:%{firefox_version}
Requires:	libopensi

%description
Client for OpenSi.

%prep
%setup -q -n %{oname}

%build

%install
rm -rf %{buildroot}
# Jar for the translation
mkdir -p %{buildroot}%{mozillalibdir}/chrome/
cp -r `pwd`  %{buildroot}%{mozillalibdir}/chrome/
# installed-chrome.txt addition
mkdir -p %{buildroot}%{mozillalibdir}/chrome/rc.d/
cat << EOF > %{buildroot}%{mozillalibdir}/chrome/rc.d/10_%{oname}.txt
content,install,url,resource:/chrome/opensi/content/opensi/
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=mozilla-firefox -chrome chrome://opensi/content/login.xul
Icon=finances_section
Categories=Office;Finance;
Name=OpenSi
Comment=%{Summary}
EOF


%post
if test -x %{mozillalibdir}/mozilla-rebuild-databases.pl; then %{mozillalibdir}/mozilla-rebuild-databases.pl; fi
%if %mdkversion < 200900
%update_menus
%endif

%postun
if test -x %{mozillalibdir}/mozilla-rebuild-databases.pl; then %{mozillalibdir}/mozilla-rebuild-databases.pl; fi
%if %mdkversion < 200900
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{mozillalibdir}/chrome/%{oname}
%{mozillalibdir}/chrome/rc.d/10_%{oname}.txt
%{_datadir}/applications/mandriva-%{name}.desktop

