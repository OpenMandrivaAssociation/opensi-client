%define	oname	opensi
%define name	%{oname}-client
%define version	2.0.7
%define release 3
#(peroyvind): yes, doing this twice is done on purpose to work around weird issue..
%{expand:%%define firefox_version %(mozilla-firefox-config --version)}
%{expand:%%define firefox_version %(mozilla-firefox-config --version)}
%define mozillalibdir %{_libdir}/mozilla-firefox-%{firefox_version}
%define	Summary	OpenSi client

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Source0:	%{name}-%{version}.tar.bz2
License:	GPL
Group:		Office
Url:		http://opensi.org/
BuildRequires:	mozilla-firefox
Requires(pre):	mozilla-firefox = %{firefox_version}
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

install -d %{buildroot}%{_menudir}
cat <<EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}):command="mozilla-firefox -chrome chrome://opensi/content/login.xul" \
                icon="finances_section.png" \
                needs="x11" \
                section="More Applications/Finances" \
                title="OpenSi"\
                longtitle="%{Summary}"
EOF


%post
if test -x %{mozillalibdir}/mozilla-rebuild-databases.pl; then %{mozillalibdir}/mozilla-rebuild-databases.pl; fi
%update_menus

%postun
if test -x %{mozillalibdir}/mozilla-rebuild-databases.pl; then %{mozillalibdir}/mozilla-rebuild-databases.pl; fi
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{mozillalibdir}/chrome/%{oname}
%{mozillalibdir}/chrome/rc.d/10_%{oname}.txt
%{_menudir}/%{name}

