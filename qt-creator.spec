#define prerelease rc1

# We need avoid oython byte compiler to not crash over template .py file which
# is not a valid python file, only for the IDE
%global _python_bytecompile_errors_terminate_build 0

Name:           qt-creator
Version:        4.0.1
Release:        1%{?prerelease:.%prerelease}%{?dist}
Summary:        Cross-platform IDE for Qt
Group:          Development/Tools
License:        GPLv3 with exceptions
URL:            http://qt-project.org/wiki/Category:Tools::QtCreator
Provides:       qtcreator = %{version}-%{release}
Source0:        http://download.qt.io/%{?prerelease:development}%{?!prerelease:official}_releases/qtcreator/4.0/%{version}%{?prerelease:-%prerelease}/qt-creator-opensource-src-%{version}%{?prerelease:-%prerelease}.tar.gz
# Use absolute paths for the specified rpaths, not $ORIGIN-relative paths
# (to fix some /usr/bin/<binary> having rpath $ORIGIN/..)
Patch0:         qt-creator_rpath.patch
# In Fedora, the ninja command is called ninja-build
Patch1:         qt-creator_ninja-build.patch
# Don't add LLVM_INCLUDEPATH to INCLUDES, since it translates to adding -isystem /usr/include to the compiler flags which breaks compilation
Patch2:         qt-creator_llvmincdir.patch
# Fix build failure due to missing include
Patch3:         qt-creator_build.patch

Source1:        qtcreator.desktop
Source2:        qt-creator-Fedora-privlibs
Source3:        qtcreator.appdata.xml

Requires:       hicolor-icon-theme
Requires:       xdg-utils
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtdoc

# tight dep on qt5-qtbase used to build, uses some private apis
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

# we need qt-devel and gcc-c++ to compile programs using qt-creator
Requires:       qt5-qtbase-devel
Requires:       gcc-c++
Requires:       %{name}-data = %{version}-%{release}


BuildRequires:  qt5-qtbase-devel >= 5.5.0
BuildRequires:  qt5-qdoc
BuildRequires:  pkgconfig(Qt5Designer) >= 5.5.0
BuildRequires:  pkgconfig(Qt5Script) >= 5.5.0
BuildRequires:  pkgconfig(Qt5XmlPatterns) >= 5.5.0
BuildRequires:  pkgconfig(Qt5X11Extras) >= 5.5.0
BuildRequires:  pkgconfig(Qt5WebKit) >= 5.5.0
BuildRequires:  pkgconfig(Qt5Help) >= 5.5.0
BuildRequires:  desktop-file-utils
BuildRequires:  botan-devel
BuildRequires:  diffutils
BuildRequires:  libappstream-glib
BuildRequires:  llvm-devel
BuildRequires:  clang-devel


%description
Qt Creator is a cross-platform IDE (integrated development environment)
tailored to the needs of Qt developers.


%package data
Summary:        Application data for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description data
Application data for %{name}.


%package translations
Summary:        Translations for %{name}
Requires:       %{name}-data = %{version}-%{release}
Requires:       qt5-qttranslations
BuildArch:      noarch

%description translations
Translations for %{name}.


%package doc
Summary:        User documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
User documentation for %{name}.


# long list of private shared lib names to filter out
%include %{SOURCE2}
%global __provides_exclude ^(%{privlibs})\.so
%global __requires_exclude ^(%{privlibs})\.so


%prep
%setup -q -n qt-creator-opensource-src-%{version}%{?prerelease:-%prerelease}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
export QTDIR="%{_qt5_prefix}"
export PATH="%{_qt5_bindir}:$PATH"

%qmake_qt5 -r IDE_LIBRARY_BASENAME=%{_lib} USE_SYSTEM_BOTAN=1 LLVM_INSTALL_DIR=%{_prefix} CONFIG+=disable_rpath
make %{?_smp_mflags}
make qch_docs %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}/%{_prefix}
make install_inst_qch_docs INSTALL_ROOT=%{buildroot}/%{_prefix}


for i in 16 24 32 48 64 128 256; do
    mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/${i}x${i}/apps
done

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

install -Dpm0644 %{SOURCE3} %{buildroot}%{_datadir}/appdata/qtcreator.appdata.xml
%{_bindir}/appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/qtcreator.appdata.xml

# Output an up-to-date list of Provides/Requires exclude statements.
outfile=__Fedora-privlibs
i=0
sofiles=$(find %{buildroot}%{_libdir}/qtcreator -name \*.so\*|sed 's!^.*/\(.*\).so.*!\1!g'|sort|uniq)
for so in ${sofiles} ; do
    if [ $i == 0 ]; then
        echo "%%global privlibs $so" > $outfile
        i=1
    else
        echo "%%global privlibs %%{privlibs}|$so" >> $outfile
    fi
done
diff -u %{SOURCE2} $outfile || :
cat $outfile


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
%doc README.md
%license LICENSE.GPL3-EXCEPT
%{_bindir}/qbs
%{_bindir}/qbs-config
%{_bindir}/qbs-config-ui
%{_bindir}/qbs-qmltypes
%{_bindir}/qbs-setup-*
%{_bindir}/qtcreator
%{_libdir}/qtcreator
%{_libexecdir}/qtcreator/
%{_datadir}/applications/qtcreator.desktop
%{_datadir}/appdata/qtcreator.appdata.xml
%{_datadir}/icons/hicolor/*/apps/QtProject-qtcreator.png

%files data
%{_datadir}/qtcreator/
%exclude %{_datadir}/qtcreator/translations

%files translations
%{_datadir}/qtcreator/translations/

%files doc
%doc %{_defaultdocdir}/qtcreator/qtcreator.qch


%changelog
* Wed Jun 08 2016 Sandro Mani <manisandro@gmail.com> - 4.0.1-1
- Update to 4.0.1

* Wed May 11 2016 Sandro Mani <manisandro@gmail.com> - 4.0.0-1
- Update to 4.0.0

* Wed Apr 20 2016 Helio Chissini de Castro <helio@kde.org> - 4.0.0-0.3.rc1
- Update to 4.0.0 rc1

* Sun Apr 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.0.0-0.2.beta2
- BR: qt5-qtbase-private-devel

* Thu Mar 24 2016 Sandro Mani <manisandro@gmail.com> - 4.0.0-0.1.beta1
- Update to 4.0.0 beta1

* Wed Mar 16 2016 Sandro Mani <manisandro@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Feb 23 2016 Sandro Mani <manisandro@gmail.com> - 3.6.0-9
- Rebuild for Qt5 ABI breakage

* Fri Feb 19 2016 Sandro Mani <manisandro@gmail.com> - 3.6.0-8
- Rebuild (clang)
- Fix build against Qt 5.6rc

* Mon Feb 08 2016 Sandro Mani <manisandro@gmail.com> - 3.6.0-7
- Add qt-creator_llvmincdir.patch to fix FTBFS

* Mon Feb 08 2016 Rex Dieter <rdieter@fedoraproject.org> 3.6.0-6
- rebuild (botan)

* Fri Feb 05 2016 Rex Dieter <rdieter@fedoraproject.org> 3.6.0-5
- add tight dep on qt5-qtbase version used to build qt-creator

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Adam Jackson <ajax@redhat.com> 3.6.0-3
- Rebuild for llvm 3.7.1 library split

* Thu Dec 24 2015 Sandro Mani <manisandro@gmail.com> - 3.6.0-2
- Ensure ClangCodeModel is built

* Tue Dec 15 2015 Sandro Mani <manisandro@gmail.com> - 3.6.0-1
- 3.6.0 release
- Clarify license

* Fri Nov 27 2015 Helio Chissini de Castro <helio@kde.org> - 3.6.0-0.3.rc1
- QDoc was splitted to prepare 5.6.0 changes

* Wed Nov 25 2015 Sandro Mani <manisandro@gmail.com> - 3.6.0-0.2.rc1
- 3.6.0 rc1 release

* Tue Oct 27 2015 Sandro Mani <manisandro@gmail.com> - 3.6.0-0.1.beta1
- 3.6.0 beta1 release

* Thu Oct 15 2015 Sandro Mani <manisandro@gmail.com> - 3.5.1-1
- 3.5.1 release

* Mon Aug 24 2015 Sandro Mani <manisandro@gmail.com> - 3.5.0-1
- 3.5.0 release

* Thu Aug 06 2015 Sandro Mani <manisandro@gmail.com> - 3.5.0-0.4.rc1
- 3.5.0 rc1 release

* Wed Jul 08 2015 Helio Chissini de Castro <helio@kde.org> - 3.5.0-0.3.beta1
- Update to released beta1

* Tue Jun 30 2015 Helio Chissini de Castro <helio@kde.org> - 3.5.0-0.2.1538dca
- Try to make Fedora Qt creator package more compatible with the rest of the world removing the docs patch
- Make appstream contact pointing to fedora qt-creator admins

* Fri Jun 26 2015 Helio Chissini de Castro <helio@kde.org> - 3.5.0-0.1.1538dca
- Build git package

* Sun Jun 21 2015 Sandro Mani <manisandro@gmail.com> - 3.4.1-3
- Add -translations subpackage

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Sandro Mani <manisandro@gmail.com> - 3.4.1-1
- 3.4.1 release

* Fri May 01 2015 Sandro Mani <manisandro@gmail.com> - 3.4.0-3
- Fix appdata file (#1217757)

* Tue Apr 28 2015 Sandro Mani <manisandro@gmail.com> - 3.4.0-2
- Add patch to correctly call ninja-build (#1216189)

* Thu Apr 23 2015 Sandro Mani <manisandro@gmail.com> - 3.4.0-1
- 3.4.0 release

* Wed Apr 01 2015 Sandro Mani <manisandro@gmail.com> - 3.4.0-0.3.rc1
- 3.4.0 rc1 release

* Thu Mar 19 2015 Sandro Mani <manisandro@gmail.com> - 3.4.0-0.2.beta1
- Re-enable ARM build

* Thu Mar 05 2015 Sandro Mani <manisandro@gmail.com> - 3.4.0-0.1.beta1
- 3.4.0 beta1 release

* Thu Mar 05 2015 Sandro Mani <manisandro@gmail.com> - 3.3.2-1
- 3.3.2 release

* Tue Feb 24 2015 Sandro Mani <manisandro@gmail.com> - 3.3.1-1
- 3.3.1 release
- Use %%license
- Use appstream-util validate-relax
- Split application data to noarch data subpackage
- Sanitize rpaths

* Wed Dec 10 2014 Sandro Mani <manisandro@gmail.com> - 3.3.0-1
- 3.3.0 release

* Thu Nov 27 2014 Sandro Mani <manisandro@gmail.com> - 3.3.0-0.2.rc1
- 3.3.0 rc1 release
- appdata-validate -> appstream-util validate

* Wed Nov 05 2014 Sandro Mani <manisandro@gmail.com> - 3.3.0-0.1.beta1
- 3.3.0 beta1 release

* Mon Oct 13 2014 Sandro Mani <manisandro@gmail.com> - 3.2.2-1
- 3.2.2 release

* Tue Sep 16 2014 Sandro Mani <manisandro@gmail.com> - 3.2.1-1
- 3.2.1 release

* Wed Aug 20 2014 Sandro Mani <manisandro@gmail.com> - 3.2.0-1
- 3.2.0 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Sandro Mani <manisandro@gmail.com> - 3.2.0-0.3.rc1
- 3.2.0 rc1 release

* Tue Jul 29 2014 Sandro Mani <manisandro@gmail.com> - 3.2.0-0.2.beta1
- doc subpackage

* Tue Jul 15 2014 Sandro Mani <manisandro@gmail.com> - 3.2.0-0.1.beta1
- 3.2.0 beta1 release

* Thu Jun 26 2014 Sandro Mani <manisandro@gmail.com> - 3.1.2-1
- 3.1.2 release

* Sun Jun 22 2014 Sandro Mani <manisandro@gmail.com> - 3.1.1-3
- Backport upstream patch to fix dumper with gdb 7.7, see rhbz#1110980

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Sandro Mani <manisandro@gmail.com> - 3.1.1-1
- 3.1.1 release

* Fri Apr 04 2014 Sandro Mani <manisandro@gmail.com> - 3.1.0-0.2.rc1
- 3.1.0 rc1 release

* Tue Mar 25 2014 Sandro Mani <manisandro@gmail.com> - 3.1.0-0.1.beta
- 3.1.0 beta release

* Wed Mar 12 2014 Sandro Mani <manisandro@gmail.com> - 3.0.1-3
- Add appdata file
- ExcludeArch arm due to #1074700

* Wed Mar 05 2014 Sandro Mani <manisandro@gmail.com> - 3.0.1-2
- Build against Qt5

* Thu Feb 06 2014 Sandro Mani <manisandro@gmail.com> - 3.0.1-1
- 3.0.1 stable release
- Fix homepage URL
- Improve description

* Thu Dec 12 2013 Sandro Mani <manisandro@gmail.com> - 3.0.0-1
- 3.0.0 stable release

* Sun Dec 01 2013 Sandro Mani <manisandro@gmail.com> - 3.0.0-0.2.rc1
- 3.0.0 rc1 release

* Wed Oct 23 2013 Jaroslav Reznik <jreznik@redhat.com> - 3.0.0-0.1.beta
- 3.0.0 beta release

* Wed Oct 16 2013 Sandro Mani <manisandro@gmail.com> - 2.8.1-1
- Update to 2.8.1
- Update URL and Source0
- Remove unused (commented) stuff
- Consistently use %%{buildroot}

* Wed Oct 16 2013 Sandro Mani <manisandro@gmail.com> - 2.8.0-6
- Fix icon in desktop file

* Fri Sep 20 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2.8.0-5
- Filter Provides/Requires for private plugin libs (#1003197).
  Let %%install section print an up-to-date filtering list.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.8.0-4
- Perl 5.18 rebuild

* Fri Jul 26 2013 Dan Horák <dan[at]danny.cz> - 2.8.0-3
- build with system botan library (#912367)
- spec cleanup

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.8.0-2
- Perl 5.18 rebuild

* Thu Jul 11 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.8.0-1
- 2.8.0 release

* Mon Jul 01 2013 Jaroslav Reznik <jreznik@redhat.com> - 2.8.0-0.2.rc
- 2.8.0 rc release

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
