Name:           qt-creator
Version:        1.0.0
Release:        4%{?dist}
Summary:        Lightweight and cross-platform IDE for Qt

Group:          Development/Tools
License:        LGPLv2 with exceptions
URL:            http://www.qtsoftware.com/developer/qt-creator
Source0:        http://download.qtsoftware.com/qtcreator/%name-%version-src.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:       qtcreator.desktop

#make ui editor works
#patch from http://labs.trolltech.com/gitweb?p=qt-creator;a=commitdiff;h=f3f20d96bdfb5266cc25ac91ae0def8a33875a81
Patch0:         disable_private_header_check.patch

#fix qdoc3 executable location in fedora
Patch1:         qtdoc3_location.patch

#make it install into lib64
Patch2:         qtcreator-qworkbenchlibrary_lib64.patch
Patch3:         qtcreator-qworkbenchplugin_lib64.patch
Patch4:         qworkbench_lib64.patch
Patch5:         qtcreator_rpath.patch

#enable signal/slot editor  http://labs.trolltech.com/gitweb?p=qt-creator;a=commitdiff_plain;h=bf118eba1ee1f5b6e19c6f29cd7d114c121a20ef
Patch6:        enable-signal-slot.patch

#search for plugins in lib64 dir
Patch7:        pluginPaths.patch

#temporary disabled docs
Patch8:       no-docu.diff

BuildRequires:  qt4-devel >= 4.5.0

%description
Qt Creator (previously known as Project Greenhouse) is a new,
lightweight, cross-platform integrated  development environment (IDE)
designed to make development with the Qt application framework
even faster and easier.

%prep
%setup -q -n %name-%version-src
%patch0 -p0
%patch1 -p0

#make it install into lib64
%if "%{_lib}" == "lib64"
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch7 -p0
%endif

%patch6 -p0

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

desktop-file-install                                    \
--add-category="Development"                            \
--dir=%{buildroot}%{_datadir}/applications              \
%{SOURCE1}



%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README LICENSE.LGPL LGPL_EXCEPTION.TXT
%{_bindir}/qtcreator
%{_libdir}/qtcreator
%{_datadir}/qtcreator
%{_datadir}/pixmaps/qtcreator_logo_*.png
%{_datadir}/applications/qtcreator.desktop

%changelog
* Tue Mar 20 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-4
- fix lib's loading in 64 bit machines

* Tue Mar 18 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-3
- Changed License to LGPLv2 with exceptions and BR to qt4-devel >= 4.5.0

* Tue Mar 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-2
- Improved Version to make it more compatible with fedora guidelines

* Sun Mar 15 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-1
- initial RPM release
