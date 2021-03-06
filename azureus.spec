%global     _newname Vuze

Name:       azureus
Version:    5.7.6.0
%global     uversion  %(foo=%{version}; echo ${foo//./})
Release:    6%{?dist}
Epoch:      1
Summary:    A BitTorrent Client

#Exception for using Eclipse SWT
#http://wiki.vuze.com/w/Vuze_License
License:    GPLv2+ with exceptions

URL:        http://azureus.sourceforge.net

Source0:    http://downloads.sourceforge.net/azureus/%{_newname}_%{uversion}_source.zip
Source2:    Azureus.desktop
Source3:    azureus.applications

# ant build script from Azureus-4.3.0.6 with patches included:
# - azureus-remove-manifest-classpath.patch
# - azureus-4.2.0.4-java5.patch
Source4: build.xml

Patch1: azureus-no-shared-plugins.patch
Patch2: azureus-SecureMessageServiceClientHelper-bcprov.patch
Patch6: azureus-5.7.5.0-no-bundled-apache-commons.patch
Patch7: azureus-5.7.0.0-startupScript.patch
Patch8: azureus-5.7.5.0-no-bundled-json.patch
Patch9: azureus-5.7.5.0-no-bundled-bouncycastle.patch
Patch10: azureus-5.6.0.0-fix_compile.patch
Patch11: vuze-5.3.0.0-disable-updaters.patch
# On 2018-07-01, Tom Callaway was able to contact Allan Crooks by email.
# Allan gave explicit permission for his files (PluginState.java, PluginStateImpl.java)
# to be used under GPLv2+.
# See also: https://github.com/BiglySoftware/BiglyBT/pull/559
Patch12: azureus-5.7.6.0-relicense-allan-crooks-files.patch

BuildRequires:  ant
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  xml-commons-apis
BuildRequires:  apache-commons-cli
BuildRequires:  junit
BuildRequires:  apache-commons-lang
BuildRequires:  bouncycastle >= 1.33-3
BuildRequires:  json_simple
%if 0%{?fedora}
BuildRequires:  log4j12
BuildRequires:  eclipse-swt >= 3.5
%else
BuildRequires:  log4j
BuildRequires:  rh-eclipse46-eclipse-swt >= 3.5
%endif
BuildRequires:  junit
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  desktop-file-utils

Requires:       apache-commons-cli
Requires:       apache-commons-lang
%if 0%{?fedora}
Requires:       log4j12
Requires:       eclipse-swt >= 3.5
%else
Requires:       log4j
Requires:       rh-eclipse46-eclipse-swt >= 3.5
%endif
Requires:       bouncycastle >= 1.33-3
Requires:       java >= 1:1.6.0
Requires:       json_simple
Requires(post):  desktop-file-utils
Requires(postun):   desktop-file-utils

Provides:   vuze = %{version}-%{release}

BuildArch:  noarch


%description
Azureus (now %{_newname}) implements the BitTorrent protocol using java
and comes bundled with many invaluable features for both beginners and
advanced users.

%prep
%setup -q -c

cp %{SOURCE4} .

# Convert line endings...
sed -i 's/\r//' ChangeLog.txt
chmod 644 *.txt

#remove bundled libs
rm -r org/apache
rm -r org/bouncycastle
rm -r org/json
rm -r org/gudy/bouncycastle
#rm -fR org/pf

rm org/gudy/azureus2/ui/swt/osx/CarbonUIEnhancer.java
rm org/gudy/azureus2/ui/swt/osx/Start.java
rm org/gudy/azureus2/ui/swt/win32/Win32UIEnhancer.java

# nuke this file to avoid any confusion of licensing
rm -rf org/gudy/azureus2/ui/console/multiuser/TestUserManager.java

#hacks to org.eclipse.swt.widgets.Tree2 don't compile.
rm -fR org/eclipse

%patch1 -p1 -b .no-shared-plugins
%patch2 -p1 -b .nobcprov
%patch6 -p1 -b .no-bundled-apache-commons
%patch7 -p1 -b .startupScript
%patch8 -p1 -b .no-bundled-json
%patch9 -p1 -b .no-bundled-bouncycastle
%patch10 -p1 -b .fix_compile
%patch11 -p1 -b .disable_updaters
%patch12 -p1 -b .gplv2orlater

%if 0%{?rhel}
sed -i 's/log4j-1/log4j/g' org/gudy/azureus2/platform/unix/startupScript
%endif

%build
mkdir -p build/libs

%global log4j_ver %{nil}
%if 0%{?fedora} > 20
%global log4j_ver 12-1.2.17
%endif

build-jar-repository -p build/libs bcprov apache-commons-cli log4j%{log4j_ver} \
  junit apache-commons-lang json_simple

%if 0%{?rhel}
#. /opt/rh/rh-java-common/enable
#ln -s /opt/rh/devtoolset-4/root/usr/lib64/eclipse/swt.jar build/libs
#scl enable rh-eclipse46 bash
ln -s /opt/rh/rh-eclipse46/root/usr/lib64/eclipse/swt.jar build/libs 
%else
#ppc seems to have eclipse-swt.ppc64 installed so libdir can't be used
if [ -e /usr/lib/eclipse/swt.jar ];then
  ln -s /usr/lib/eclipse/swt.jar build/libs
else
  ln -s /usr/lib64/eclipse/swt.jar build/libs
fi
%endif

ant jar

%install
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/Azureus2.jar

install -p -D -m 0755 org/gudy/azureus2/platform/unix/startupScript $RPM_BUILD_ROOT%{_bindir}/azureus

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a16.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a64.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/azureus.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir ${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE2}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/application-registry
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/application-registry

%if 0%{?rhel}
mkdir $RPM_BUILD_ROOT%{_datadir}/java
ln -s /opt/rh/devtoolset-4/root/usr/lib64/eclipse/swt.jar $RPM_BUILD_ROOT%{_datadir}/java
%endif


%post
update-desktop-database %{_datadir}/applications
# update icon themes
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%postun
update-desktop-database %{_datadir}/applications
# update icon themes
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%files
%doc ChangeLog.txt
%license GPL.txt
%{_datadir}/applications/*
%{_datadir}/application-registry/*
%{_datadir}/pixmaps/azureus.png
%{_datadir}/icons/hicolor/16x16/apps/azureus.png
%{_datadir}/icons/hicolor/32x32/apps/azureus.png
%{_datadir}/icons/hicolor/64x64/apps/azureus.png
%{_bindir}/azureus
%{_datadir}/azureus
%if 0%{?rhel}
%{_datadir}/java/swt.jar
%endif


%changelog
* Sat May 11 2019 Sérgio Basto <sergio@serjux.com> - 1:5.7.6.0-6
- Add Epoch 1

* Sat May 11 2019 Sérgio Basto <sergio@serjux.com> - 5.7.6.0-5
- Remove Group tag

* Sat May 11 2019 Sérgio Basto <sergio@serjux.com> - 5.7.6.0-4
- Use rh-eclipse46

* Sun Oct 21 2018 Sérgio Basto <sergio@serjux.com> - 5.7.6.0-3
- Steps to build in epel7 with Devtoolset-4

* Tue Sep 25 2018 Sérgio Basto <sergio@serjux.com> - 5.7.6.0-2
- Fix License

* Sun Nov 05 2017 Sérgio Basto <sergio@serjux.com> - 5.7.6.0-1
- Update azureus to 5.7.6.0

* Sun Aug 20 2017 Sérgio Basto <sergio@serjux.com> - 5.7.5.0-4
- Enable SWT_GTK3 and Wayland

* Sun May 28 2017 Sérgio Basto <sergio@serjux.com> - 5.7.5.0-3
- Add to Azureus.desktop magnet links

* Sat Mar 25 2017 Sérgio Basto <sergio@serjux.com> - 5.7.5.0-2
- rebuilt

* Mon Mar 13 2017 Sérgio Basto <sergio@serjux.com> - 5.7.5.0-1
- Update azureus to 5.7.5.0

* Wed Dec 21 2016 Sérgio Basto <sergio@serjux.com> - 5.7.4.0-2
- improvement of include swt jar , drop requires for Fedora <= 20

* Tue Nov 22 2016 Sérgio Basto <sergio@serjux.com> - 5.7.4.0-1
- New upstream release, 5.7.4.0

* Sun Aug 14 2016 Sérgio Basto <sergio@serjux.com> - 5.7.3.0-1
- Update azureus to 5.7.3.0

* Mon May 23 2016 Sérgio Basto <sergio@serjux.com> - 5.7.2.0-1
- Update azureus to 5.7.2.0

* Mon May 23 2016 Sérgio Basto <sergio@serjux.com> - 5.7.1.0-2
- Add vuze-5.3.0.0-disable-updaters.patch

* Sat Feb 27 2016 Sérgio Basto <sergio@serjux.com> - 5.7.1.0-1
- Update to 5.7.1.0

* Tue Dec 08 2015 Sérgio Basto <sergio@serjux.com> - 5.7.0.0-1
- Update to 5.7.0.0

* Fri Aug 07 2015 Sérgio Basto <sergio@serjux.com> - 5.6.2.0-1
- Update to 5.6.2.0

* Fri Jun 26 2015 Sérgio Basto <sergio@serjux.com> - 5.6.1.2-2
- Use the correct log4j (the old log4j-1) and fix "Could not find log4j" when
  log4j 2.0 is not installed.

* Tue Jun 09 2015 Sérgio Basto <sergio@serjux.com> - 5.6.1.2-1
- Update to 5.6.1.2

* Wed Jun 03 2015 Sérgio Basto <sergio@serjux.com> - 5.6.1.0-1
- Update to 5.6.1.0

* Mon May 25 2015 Sérgio Basto <sergio@serjux.com> - 5.6.0.0-3
-  Remove Encoding from desktop file

* Tue May 05 2015 Sérgio Basto <sergio@serjux.com> - 5.6.0.0-2
- Drop patch1 and patch7 and use file build.xml already patched.

* Tue May 05 2015 Sérgio Basto <sergio@serjux.com> - 5.6.0.0-1
- Update to Azureus-5.6.0.0
- New patches for no-bundled-apache-commons, stupid-invalid-characters,
    startupScript and fix_compile (which also has modifications)

* Wed Feb 25 2015 David Juran <djuran@redhat.com> - 5.5.0.0-4
- Use licence tag

* Sun Dec 14 2014 Sérgio Basto <sergio@serjux.com> - 5.5.0.0-2
- Use JAVA_ARGS="-Xmx256m" on startupScript .
- Drop patch azureus-cache-size.patch .
- Fix in better way invalid characters.
- Make it possible build for Fedora 20 and lower.

* Mon Nov 24 2014 David Juran <djuran@redhat.com> - 5.5.0.0-1
- Upgrade to Vuze-5.5.0.0

* Wed Nov 12 2014 David Juran <djuran@redhat.com> - 5.4.0.0-3
- Fix Desktop file (as suggested by Sergio Monteiro Basto)

* Tue Nov 11 2014 David Juran <djuran@redhat.com> - 5.4.0.0-2
- Make it build

* Sat Oct 11 2014 David Juran <djuran@redhat.com> - 5.4.0.0-1
- Back out ProgrammersFriend replacement, the entire license issue is a mess.
- Upgrade to Vuze-5.4.0.0

* Mon Jul 07 2014 David Juran <djuran@redhat.com> - 5.3.0.0-6
- Fix License tag
- Remove dependency on ProframmersFriend library

* Tue Jun 10 2014 Alexander Kurtakov <akurtako@redhat.com> 5.3.0.0-5
- Use log4j12.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 David Juran <djuran@redhat.com> - 5.3.0.0-3
- Do not force BouncyCastle Provider

* Mon Mar 03 2014 David Juran <djuran@redhat.com> - 5.3.0.0-2
- Remove bundled BouncyCastle (Bz 820117)

* Tue Feb 11 2014 David Juran <djuran@redhat.com> - 5.3.0.0-1
- Upgrade to azureus-5.3.0.0

* Sun Feb 09 2014 Sérgio Basto <sergio@serjux.com> - 5.2.0.0-4
- Unbundle json (Bz 820117)

* Thu Feb 06 2014 David Juran <djuran@redhat.com> - 5.2.0.0-3
- Fix warning re: /usr/share/azureus not beeing writable (Sergio Monteiro Basto)
- Revert limiting java heap size (Bz1040625)

* Thu Jan 09 2014 David Juran <djuran@redhat.com> - 5.2.0.0-1
- update startup script (Bz1040625)

* Sun Dec 08 2013 David Juran <djuran@redhat.com> - 5.2.0.0-1
- upgrade to 5.2.0.0

* Sat Oct 05 2013 David Juran <djuran@redhat.com> - 5.1.0.0-1
- upgrade to 5.1.0.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Alexander Kurtakov <akurtako@redhat.com> 5.0.0.0-1
- Update to 5.0.0.0.
- Remove unused patches.

* Sun Mar 17 2013 David Juran <djuran@redhat.com> - 4.9.0.0-1
- upgrade to 4.9.0.0

* Sat Feb 23 2013 David Juran <djuran@redhat.com> - 4.8.1.2-3
- removed bundeled apache-commons (BZ 820117)

* Sun Feb 10 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 4.8.1.2-2
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Sun Dec 30 2012 David Juran <djuran@redhat.com> - 4.8.1.2-1
- upgrade to Vuze 4.8.1.2
- provides Vuze

* Sat Nov 10 2012 David Juran <djuran@redhat.com> - 4.8.0.0-1
- upgrade to 4.8.0.0

* Sun Oct 14 2012 David Juran <djuran@redhat.com> - 4.7.2.0-1
- upgrade to 4.7.2.0

* Sat Aug 11 2012 David Juran <david@juran.se> - 4.7.1.2-2
- change jakarta-commons-cli requirement to apache-commons-cli (Bz 818490)

* Sat Aug 11 2012 David Juran <david@juran.se> - 4.7.1.2-1
- upgrade to 4.7.1.2

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr  4 2012 David Juran <djuran@redhat.com> - 4.7.0.2-1
- upgrade to azureus 4.7.0.2

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 David Juran <djuran@redhat.com> - 4.7.0.0-1
- upgrade to azureus 4.7.0.0

* Sat Aug 27 2011 David Juran <djuran@redhat.com> - 4.6.0.4-4
- fix character encoding for java 7

* Thu Aug 25 2011 David Juran <djuran@redhat.com> - 4.6.0.4-3
- Fix installation of plugins (Bz 540638)

* Mon Apr 18 2011 David Juran <djuran@redhat.com> - 4.6.0.4-2
- use webkit instead of xulrunner, works around Bz 674838

* Sat Apr  2 2011 David Juran <djuran@redhat.com> - 4.6.0.4-1
- upgrade to Vuze 4.6.0.4

* Thu Feb 10 2011 David Juran <djuran@redhat.com> - 4.6.0.2-1
- upgrade to Vuze 4.6.0.2
- clean up not needed patches

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 David Juran <david@juran.se> - 4.6.0.0-2
- fix path to apache-commons-cli in start script
- fix path to xulrunner

* Sun Jan 23 2011 David Juran <djuran@redhat.com> - 4.6.0.0-1
- upgrade to 4.6.0.0

* Tue Dec  7 2010 David Juran <djuran@redhat.com> - 4.5.1.0-2
- jakarta-commons-cli changed to apache-commons-cli (Bz 661057)

* Thu Oct  7 2010 David Juran <djuran@redhat.com> - 4.5.1.0-1
- upgrade to 4.5.1.0

* Wed Sep  8 2010 David Juran <djuran@redhat.com> - 4.5.0.4-1
- upgrade to 4.5.0.4

* Wed Aug 25 2010 Alexander Kurtakov <akurtako@redhat.com> 4.5.0.2-2
- Remove libgconf-java false BR/R.
- Use global instead of define.

* Wed Aug 18 2010 David Juran <david@juran.se> - 4.5.0.2-1
- upgrade to 4.5.0.2

* Thu Aug  5 2010 David Juran <david@juran.se> - 4.5.0.0-1
- upgrade to 4.5.0.0

* Fri Feb 12 2010 David Juran <djuran@redhat.com> - 4.3.1.4-1
- upgrade to 4.3.1.4

* Mon Jan 18 2010 David Juran <djuran@redhat.com> - 4.3.0.6-1
- update to 4.3.0.6

* Sun Dec  13 2009 David Juran <djuran@redhat.com> - 4.3.0.4-3
- fix build, even on ppc
- apply -s to all patches

* Tue Dec  1 2009 David Juran <djuran@redhat.com> - 4.3.0.4-1
- upgrade to 4.3.0.4

* Thu Nov 19 2009 David Juran <djuran@redhat.com> - 4.3.0.0-1
- upgrade to azureus-4.3.0.0

* Sun Sep  13 2009 David Juran <djuran@redhat.com> - 4.2.0.8-2
- revive the no-updates patches (Bz515131)
- fix start-script to work when /usr/share/azureus/plugins/ is empty

* Sat Sep 12 2009 David Juran <djuran@redhat.com> - 4.2.0.8-1
- Upgrade to 4.2.0.8

* Tue Aug  4 2009 David Juran <david@juran.se> - 4.2.0.4-2
- Fix Bz 515228 properly

* Wed Jul 29 2009 David Juran <david@juran.se> - 4.2.0.4-1
- Upgrade to 4.2.0.4
- Fix SWT dir on x86_64 (Bz 515228)
- fix rpmlint warnings

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 18 2009 Conrad Meyer <konrad@tylerc.org> - 4.0.0.4-3
- Apply Bart Vanbrabant's patch to azureus.script to start
  correctly on 64-bit (rhbz#490774).

* Thu Feb 26 2009 Conrad Meyer <konrad@tylerc.org> - 4.0.0.4-2
- Upstream uses internal things from sun's jre, so we need
  openjdk.

* Thu Feb 26 2009 Conrad Meyer <konrad@tylerc.org> - 4.0.0.4-1
- New version, new breakage. Patches 50-56 added.
- Dropped a lot of patches that don't apply to the new azureus.
- Make noarch (drop gcj support).

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 01 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-17
- Updated release.
- Changed swt-gtk-3.3.jar links to swt.jar.
- Updated libswt3-gtk2 requirements to eclipse-swt.
- Resolves: rhbz#465051

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.4.2-16
- fix license tag
- fix cache-size patch to apply with fuzz=0

* Wed Mar 26 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-14
- Fixed azureus.script to set GRE_PATH properly on 64-bit.

* Thu Mar 20 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-13
- Fixed typo.
- Updated Release.

* Tue Mar 18 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-12
- Fixed typo.
- Updated Release.

* Thu Mar 13 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-11
- Updated release.
- Updated JAVA_HOME in azureus.script.
- Changed java-1.7.0-icedtea requirements to java-1.6.0-openjdk.

* Thu Feb 21 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-10
- Updated release.
- Updated azureus.script

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.4.2-9
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-8
- Updated azplugins jar to 2.1.6

* Tue Jan 29 2008 Lillian Angel <langel@redhat.com> - 3.0.4.2-7
- Upgraded to azureus version 3.0.4.2
- Removed azureus-no-update-manager-MainStatusBar.patch.
- Removed azureus-rh-bugzilla-180418.patch.
- Updated azureus-no-update-manager-UpdateMonitor.patch.
- Updated azureus-remove-manifest-classpath.patch.
- Resolves rhbz#430607

* Wed Jan 16 2008 Lillian Angel <langel@redhat.com> - 3.0.3.4-6
- Removed azureus-themed.patch

* Wed Jan 02 2008 Lillian Angel <langel@redhat.com> - 3.0.3.4-5
- Updated script to set version.
- Updated release.
- Added new patch.
- Resolves: rhbz#427257

* Thu Dec 20 2007 Lillian Angel <langel@redhat.com> - 3.0.3.4-4
- Updated script to use new xulrunner-1.9pre
- Updated release.

* Wed Dec 12 2007 Lillian Angel <langel@redhat.com> - 3.0.3.4-3
- Changed firefox requirement to xulrunner.
- Adusted script accordingly.

* Fri Dec  7 2007 Lillian Angel <langel@redhat.com> - 3.0.3.4-2
- Removed ExcludeArch.
- Updated Release.
- Added firefox as a requirement for the browser support.
- Moved JAVA_HOME to script.
- Added MOZILLA_FIVE_HOME to script.
- Updated LD_LIBRARY_PATH in script.

* Mon Dec  3 2007 Lillian Angel <langel@redhat.com> - 3.0.3.4-1
- Upgrade to 3.0.3.4.
- ExcludeArch ppc and ppc64 because of IcedTea.
- Resolves: rhbz#376111
- Resolves: rhbz#321581
- Resolves: rhbz#371521
- Resolves: rhbz#372931
- Resolves: rhbz#235751
- Resolves: rhbz#247295

* Thu Oct 25 2007 Ben Konrath <bkonrath@redhat.com> - 2.5.0.4-4
- Use swt.jar instead of swt-gtk-3.3.jar in wrapper script.

* Thu Oct  4 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 2.5.0.4-3
- Build against swt 3.3.
- Update startup script.
- Resolves: rhbz#296911

* Thu Mar 29 2007 Anthony Green <green@redhat.com> 2.5.0.4-2
- Upgrade to 2.5.0.4.

* Wed Mar 28 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 2.5.0.0-12
- Remove gnu-crypto build and runtime requirements.
- Do not include gnu-crypto in classpath.

* Tue Dec 19 2006 Anthony Green <green@redhat.com> 2.5.0.0-11
- Fix bcprov link for build.

* Sun Dec 17 2006 Anthony Green <green@redhat.com> 2.5.0.0-10
- Update azureus.script to use unversioned bcprov jar file.

* Mon Nov 06 2006 Andrew Overholt <overholt@redhat.com> 2.5.0.0-9
- Use new swt jar location.

* Sat Oct 28 2006 Anthony Green <green@redhat.com> 2.5.0.0-8
- Force bcprov-1.33.jar onto the CLASSPATH in azureus.script so it
  will run on non-gcj java alternatives.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.5.0.0-7
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Anthony Green <green@redhat.com> - 2.5.0.0-2
- Fix release tag.

* Mon Sep 18 2006 Anthony Green <green@redhat.com> - 2.5.0.0-1.5
- Rebuild.

* Wed Aug 30 2006 Anthony Green <green@redhat.com> - 2.5.0.0-1.4
- Rebuild with new aot-compile-rpm.

* Sat Aug 26 2006 Anthony Green <green@redhat.com> - 2.5.0.0-1.2
- Don't exclude ppc.

* Sat Aug 26 2006 Anthony Green <green@redhat.com> - 2.5.0.0-1.1
- Update sources.

* Sun Aug 13 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060730cvs_1
- Update release.

* Sat Jul 29 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_8
- Fix swt jar reference for plugins builds.

* Sat Jul 29 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_7
- Enable ppc builds.  Fix classpath with -p option to build-jar-repository.

* Sat Jul 29 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_6
- Temporarily disable ppc builds.

* Sat Jul 29 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_5
- Fix patch with absolute path.

* Sat Jul 29 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_4
- Turn optimization back on.  gcc has been fixed.

* Tue Jul 18 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_3
- Work around swt installation problem.

* Sat Jul  8 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_2
- Updated sources.
- Build against swt 3.2.  Update startup script.  Remove swt 3.1.1 patches.
- Build against bouncycastle 1.33 package.  Add the following patches to work 
  with bouncycastle 1.33 out of the box: 
  azureus-SecureMessageServiceClientHelper-bcprov.patch,
  azureus-UDPConnectionSet-bcprov.patch, azureus-CryptoHandlerECC-bcprov.patch, 
  azureus-CryptoSTSEngineImpl-bcprov.patch
- Build with -O0 to avoid gcc bugzilla 19505.

* Sun Jul  2 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060702cvs_1
- Updated sources.

* Sun Jun  4 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060604cvs_1
- Updated sources.
- Update azplugins jar file.

* Mon May 29 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060529cvs_1
- Updated sources.
- Re-enable close button on tabs in nativetabs patch.
- Use proper ChangeLog.txt file.

* Wed May 03 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060503cvs_1
- Updated sources.

* Mon Apr 24 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060328cvs_5
- Two patches from Stephan Michels: nativetabs (for native GTK+ tabs), and 
an updated azureus-themed.patch to work around GCC PR 27271.

* Thu Apr 06 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060328cvs_4
- Yet another correction to LD_LIBRARY_PATH.  Bugzilla #186152.

* Mon Apr 03 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060328cvs_3
- One more correction to LD_LIBRARY_PATH.  Bugzilla #186152.

* Sat Apr 01 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060328cvs_2
- Set LD_LIBRARY_PATH for Sun java alternative.  Bugzilla #186152.
- Remove pushd/popd noise from startup script.

* Tue Mar 28 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060328cvs_1
- Update sources.
- Fix bcprov jar file reference.

* Mon Feb 13 2006 Anthony Green <green@redhat.com> - 2.4.0.0-0.20060207cvs_1
- Remove absolute path from azureus-no-updates-PluginInterfaceImpl.patch.

* Fri Feb 10 2006 Anthony Green <green@redhat.com> - 2.4.0.0-0.20060207cvs
- Update cvs sources.  Boost version number.
- Move all jar files to /usr/share/azureus.
- Add azplugins and bdcc.
- Remove update and restart menu items.
- Disable all updating.

* Thu Feb  9 2006 Anthony Green <green@redhat.com> - 2.3.0.7-2.20060207cvs
- Add libgconf dependency.

* Thu Feb  9 2006 Anthony Green <green@redhat.com> - 2.3.0.7-1.20060207cvs
- Replace absolute paths in swt-3.1 patches with relative paths.

* Thu Feb  9 2006 Anthony Green <green@redhat.com> - 2.3.0.7-0.20060207cvs
- Fix release number.

* Thu Feb  9 2006 Anthony Green <green@redhat.com> - 2.3.0.7-0
- Move to 2.3.0.7 snapshot (or will it be 2.4.0.0?).
- Many related changes.
- Remove ability to install plugins.

* Sat Feb  4 2006 Anthony Green <green@redhat.com> - 2.3.0.6-23
- Fix thinko in last revision.

* Sat Feb  4 2006 Anthony Green <green@redhat.com> - 2.3.0.6-22
- Update libswt3-gtk2 requirements in spec file and azureus.script.

* Fri Jan 27 2006 Anthony Green <green@redhat.com> - 2.3.0.6-21
- Add azureus-no-shared-plugins.patch.
- Add azureus-no-shared-plugins2.patch.

* Fri Jan 27 2006 Anthony Green <green@redhat.com> - 2.3.0.6-20
- Remove junit reference from startup script.

* Wed Jan 25 2006 Anthony Green <green@redhat.com> - 2.3.0.6-19
- Theme CoolBar icons with azureus-themed.patch.
- Add libgtk-java and glib-java dependencies to spec file.
- Add gtk2.8 and glib0.2 to azureus.script.
- Add missing semi-colon to Azureus.desktop.

* Sat Jan 21 2006 Anthony Green <green@redhat.com> - 2.3.0.6-17
- Use "$@" instead of $* in azureus.script (thanks ivazquez).
- Improve .desktop file.

* Sat Jan 21 2006 Anthony Green <green@redhat.com> - 2.3.0.6-17
- Use "$@" instead of $* in azureus.script (thanks ivazquez).
- Improve .desktop file.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-15
- Remove PrintTransferTypes, which is unused and not 64-bit clean.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-14
- Remove junit from build-jar-repository.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-13
- Drop the junit dependencies.
- Delete unused test code.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-12
- Convert line endings with sed, not dos2unix.
- Add BuildRequires for desktop-file-utils.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-11
- Add Requires(post/postun): desktop-file-utils.
- Install .desktop file with desktop-file-install.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-10
- Fix post and postun desktop integration.
- Add MimeType to .desktop file.
- Add comment about SOURCE0.
- Install files with install, not cp.
- Fix permissions on doc files.
- Add BuildRequires xml-commons-apis.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-9
- Require libgcj with the latest fixes for running Azureus.
- Be explicit about .png files in files-section.

* Wed Jan 18 2006 Anthony Green <green@redhat.com> - 2.3.0.6-8
- Remove bouncycastle from build-classpath in startup script.
- Remove exclusive arch.
- Remove classpath from manifest.
- Add License.txt and ChangeLog.txt.

* Tue Jan 17 2006 Anthony Green <green@redhat.com> - 2.3.0.6-7
- Add azureus-cache-size.patch

* Tue Jan 17 2006 Anthony Green <green@redhat.com> - 2.3.0.6-6
- Experimental build with no bouncycastle dependency.

* Mon Jan 16 2006 Chris Chabot <chabot@xs4all.nl> - 2.3.0.6-5
- Changed file section so package doesn't end up owning
  standard directories.

* Sun Jan 15 2006 Anthony Green <green@redhat.com> - 2.3.0.6-4
- Remove bouncycastle crypto from zipball.
- Add bouncycastle build- and runtime dependencies.
- Desktop integration work.

* Sun Dec 18 2005 Anthony Green <green@redhat.com> - 2.3.0.6-3
- Add azureus-ConfigurationManager-improvement.patch

* Sat Dec 17 2005 Anthony Green <green@redhat.com> - 2.3.0.6-2
- Add azureus-remove-win32-PlatformManagerUpdateChecker.patch

* Sat Dec 17 2005 Anthony Green <green@redhat.com> - 2.3.0.6-1
- Created.
