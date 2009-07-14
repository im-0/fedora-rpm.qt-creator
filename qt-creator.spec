Name:           qt-creator
Version:        1.2.1
Release:        1%{?dist}
Summary:        Lightweight and cross-platform IDE for Qt

Group:          Development/Tools
License:        LGPLv2 with exceptions
URL:            http://www.qtsoftware.com/developer/qt-creator
Source0:        http://download.qtsoftware.com/qtcreator/%name-%version-src.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:       qtcreator.desktop

# make it install into lib/lib64
Patch0:         qt-creator-1.2.0-qtcreatorwidgets_pro.patch
#fix qdoc3 executable location in fedora
Patch1:         qtdoc3_location.patch

Requires:       hicolor-icon-theme
BuildRequires:  qt4-devel >= 4.5.0
BuildRequires:  desktop-file-utils

%description
Qt Creator (previously known as Project Greenhouse) is a new,
lightweight, cross-platform integrated  development environment (IDE)
designed to make development with the Qt application framework
even faster and easier.

%prep
%setup -q -n %name-%version-src
%patch0 -p1
%patch1 -p0

#make it install into lib64
#%if "%{_lib}" == "lib64"
#%patch0 -p2
#%endif


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
