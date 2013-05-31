Name:           qt-creator
Version:        2.8.0
Release:        0.1.beta%{?dist}
Summary:        Lightweight and cross-platform IDE for Qt

Group:          Development/Tools
License:        LGPLv2 with exceptions
URL:            http://developer.qt.nokia.com/wiki/Category:Tools::QtCreator
Source0:        http://get.qt.nokia.com/qtcreator/%{name}-%{version}-beta-src.tar.gz

Source1:        qtcreator.desktop

Requires:       hicolor-icon-theme
Requires:       xdg-utils

#required for demos/examples
Requires:       qt-demos
Requires:       qt-examples
# we need qt-devel and gcc-c++ to compile programs using qt-creator
Requires:       qt4-devel
Requires:       gcc-c++
%{?_qt4_version:Requires: qt4 >= %{_qt4_version}}

BuildRequires:  qt4-devel >= 4.7.2
BuildRequires:  qt4-webkit-devel
# for QmlDesigner, see also https://bugzilla.redhat.com/show_bug.cgi?id=657498
BuildRequires:  qt4-devel-private
BuildRequires:  desktop-file-utils

%description
Qt Creator (previously known as Project Greenhouse) is a new,
lightweight, cross-platform integrated  development environment (IDE)
designed to make development with the Qt application framework
even faster and easier.

%prep
%setup -q -n %{name}-%{version}-beta-src

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
# link it to %%{_datadir}/pixmaps/qtcreator_logo_${i}.png
#ln -s ../../../../pixmaps/qtcreator_logo_${i}.png \
# $RPM_BUILD_ROOT/%%{_datadir}/icons/hicolor/${i}x${i}/apps/qtcreator.png

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
%{_bindir}/qmlpuppet
%{_bindir}/qtpromaker
%{_bindir}/qtcreator
%{_bindir}/qtcreator_process_stub
%{_bindir}/sdktool
%{_libdir}/qtcreator
#%{_libdir}/qmldesigner
%{_datadir}/qtcreator
#%%{_datadir}/pixmaps/qtcreator_logo_*.png
%{_datadir}/applications/qtcreator.desktop
%{_datadir}/icons/hicolor/*/apps/QtProject-qtcreator.png
#%%{_datadir}/doc/qtcreator/qtcreator.qch

%changelog
* Fri May 31 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.8.0-0.1.beta
- 2.8.0 beta release

* Fri May 31 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.7.1-1
- 2.7.1 release

* Thu Mar 21 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.7.0-1
- 2.7.0 release

* Thu Mar 07 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.7.0-0.2.rc
- 2.7.0 release candidate

* Sun Feb 10 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.7.0-0.1.beta
- 2.7.0 beta release

* Wed Feb 06 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.6.2-1
- 2.6.2 release

* Fri Dec 21 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.6.1-1
- 2.6.1 release

* Tue Sep 11 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.6.0-0.1.beta
- 2.6.0 beta release

* Wed Aug 15 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.5.2-1
- 2.5.2 release

* Wed Jul 25 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.5.1-1
- 2.5.1 release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 09 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.5.0-1
- 2.5.0 release

* Tue Apr 24 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.5.0-0.2.rc
- 2.5.0 rc release

* Fri Mar 16 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.5.0-0.1.beta
- 2.5.0 beta release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for c++ ABI breakage

* Wed Feb 01 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.4.1-1
- 2.4.1 release
- fix upstream url
- package qmlprofiler

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-0.1.rc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.4.0-0.0.rc
- 2.4.0-rc

* Wed Sep 28 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.3.1-1
- 2.3.1 release

* Thu Sep 01 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.3.0-1
- 2.3.0 release

* Wed Jul 13 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.3.0-0.0.beta
- 2.3.0 beta

* Wed Jun 29 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.2.1-2
- include qmlpuppet

* Tue Jun 21 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.2.1-1
- 2.2.1

* Fri May 06 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.2.0-1
- 2.2.0 final

* Wed Apr 20 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.2.0-0.2.rc1
- 2.2.0 RC

* Tue Apr 05 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.2.0-0.1.beta
- BR: qt4-devel-private, for QmlDesigner

* Sat Mar 26 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.2.0-0.0.beta
- 2.2.0 beta

* Sat Mar 26 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.1.0-5
- 2.1.0 final release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.1.0-4.rc1
- new version 2.1.0 rc1

* Tue Nov 02 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.1.0-2.beta2
- new version 2.1.0 beta2

* Wed Oct 13 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.1.0-1.beta1
- new version 2.1.0 beta1

* Sat Sep 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-2
- rebuild (#632873)

* Fri Jun 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-1
- 2.0.0 final

* Thu May 06 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.0.0-0.3.beta1
- upgrade to qt-creator 2.0 beta1

* Thu Apr 15 2010 Itamar Reis Peixoto - 2.0.0-0.2.alpha1
- Requres qt-devel and gcc-c++ (we need it to compile programs using qt-creator)

* Tue Mar 16 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 2.0.0-0.1.alpha1
- new version qt-creator 2.0 alpha1

* Tue Feb 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.1-3
- add minimal qt4 runtime dep

* Thu Feb 11 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.3.1-2
- include missing requires xdg-utils

* Mon Jan 25 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.3.1-1
- new version 1.3.1

* Tue Dec  1 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.0-2
- Force dependency on Qt >= 4.6.0

* Tue Dec  1 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1.3.0-1
- 1.3.0 final

* Sun Nov 22 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.3.0-0.4.rc
- include demos/examples.

* Wed Nov 18 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.3.0-0.3.rc
- fix install of /usr/bin/qtcreator wrapper

* Tue Nov 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.3.0-0.2.rc
- new version Qt Creator 1.3 Release Candidate(RC)
- include /usr/bin/qtcreator wrapper to /usr/bin/qtcreator.bin

* Wed Oct 14 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.3.0-0.1.beta
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

* Fri Mar 20 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-4
- fix lib's loading in 64 bit machines

* Wed Mar 18 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-3
- Changed License to LGPLv2 with exceptions and BR to qt4-devel >= 4.5.0

* Tue Mar 17 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-2
- Improved Version to make it more compatible with fedora guidelines

* Sun Mar 15 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.0-1
- initial RPM release
