Name:           qt-creator
Version:        1.1.0
Release:        2%{?dist}
Summary:        Lightweight and cross-platform IDE for Qt

Group:          Development/Tools
License:        LGPLv2 with exceptions
URL:            http://www.qtsoftware.com/developer/qt-creator
Source0:        http://download.qtsoftware.com/qtcreator/%name-%version-src.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:       qtcreator.desktop

#fix qdoc3 executable location in fedora
Patch1:         qtdoc3_location.patch

#temporary disabled docs
Patch8:       no-docu.diff
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
%patch1 -p0
%patch8 -p0

%build
QTDIR="%{_qt4_prefix}" ; export QTDIR ; \
PATH="%{_qt4_bindir}:$PATH" ; export PATH ; \
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \

qmake-qt4
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT/%{_prefix}

for i in 16 24 32 48 64 128
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


%files
%defattr(-,root,root,-)
%doc README LICENSE.LGPL LGPL_EXCEPTION.TXT
%{_bindir}/qtcreator
%{_bindir}/qtcreator.bin
%{_bindir}/qtcreator_process_stub
%{_libdir}/qtcreator
%{_datadir}/qtcreator
%{_datadir}/pixmaps/qtcreator_logo_*.png
%{_datadir}/applications/qtcreator.desktop
%{_datadir}/icons/hicolor/*/apps/Nokia-QtCreator.png

%changelog
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
