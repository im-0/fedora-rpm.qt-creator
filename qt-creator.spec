Name:           qt-creator
Version:        1.3.0
Release:        1.0.beta%{?dist}
Summary:        Lightweight and cross-platform IDE for Qt

Group:          Development/Tools
License:        LGPLv2 with exceptions
URL:            http://www.qtsoftware.com/developer/qt-creator
#Source0:        http://download.qtsoftware.com/qtcreator/%name-%version-src.tar.gz
#source0 from http://qt.gitorious.org/qt-creator/qt-creator/commits/1.3.0-beta
Source0:        qt-creator-qt-creator-1.3.0-beta.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:       qtcreator.desktop

Requires:       hicolor-icon-theme
BuildRequires:  qt4-devel >= 4.5.0
BuildRequires:  desktop-file-utils

%description
Qt Creator (previously known as Project Greenhouse) is a new,
lightweight, cross-platform integrated  development environment (IDE)
designed to make development with the Qt application framework
even faster and easier.

%prep
%setup -q -n qt-creator-qt-creator
# -n %name-%version-src

%build
QTDIR="%{_qt4_prefix}" ; export QTDIR ; \
PATH="%{_qt4_bindir}:$PATH" ; export PATH ; \
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \

qmake-qt4 -r IDE_LIBRARY_BASENAME=%{_lib}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT/%{_prefix}

for i in 16 24 32 48 64 128 256
do
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/${i}x${i}/apps
# link it to %{_datadir}/pixmaps/qtcreator_logo_${i}.png
ln -s ../../../../pixmaps/qtcreator_logo_${i}.png \
 $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/${i}x${i}/apps/Nokia-QtCreator.png

done

desktop-file-install                                    \
--add-category="Development"                            \
--dir=%{buildroot}%{_datadir}/applications              \
%{SOURCE1}

%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :



%files
%defattr(-,root,root,-)
%doc README LICENSE.LGPL LGPL_EXCEPTION.TXT
%{_bindir}/qtcreator.bin
%{_bindir}/qtcreator_process_stub
%{_libdir}/qtcreator
%{_datadir}/qtcreator
%{_datadir}/pixmaps/qtcreator_logo_*.png
%{_datadir}/applications/qtcreator.desktop
%{_datadir}/icons/hicolor/*/apps/Nokia-QtCreator.png
%{_datadir}/doc/qtcreator/qtcreator.qch

%changelog
* Wed Oct 14 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.3.0-1.0.beta
- new version 1.3.0-beta

* Sat Sep 12 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.2.90-1
- new version 1.2.90 (Qt Creator Technology Snapshot 1.2.90)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.2.1-3
- Use upstream gzipped tarball instead of zip.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.2.1-1
- new version 1.2.1

* Mon Jul 13 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.2.0-2
- fix BZ #498563 patch from Michel Salim <salimma@fedoraproject.org>
- Update GTK icon cache

* Sun Jun 28 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.2.0-1
- new version 1.2.0

* Sat Apr 25 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.1.0-2
- fix icons

* Thu Apr 23 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.1.0-1
- qt-creator 1.1.0
- include missing BuildRequires desktop-file-utils

* Tue Mar 20 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-4
- fix lib's loading in 64 bit machines

* Tue Mar 18 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-3
- Changed License to LGPLv2 with exceptions and BR to qt4-devel >= 4.5.0

* Tue Mar 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-2
- Improved Version to make it more compatible with fedora guidelines

* Sun Mar 15 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-1
- initial RPM release
