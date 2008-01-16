# ExclusiveArch: %{ix86} x86_64

Name:		azureus
Version:	3.0.3.4
Release:	6%{?dist}
Summary:	A BitTorrent Client

Group:		Applications/Internet
License:	GPL
URL:		http://azureus.sourceforge.net

# A cvs snapshot with the build and bouncycastle directories
# removed.
Source0:	azureus3-3.0.3.4.tar.gz

Source1:	azureus.script
Source2:	Azureus.desktop
Source3:	azureus.applications
Source4:	azureus-License.txt

Source5:	azplugins_1.9.jar
Source6:	bdcc_2.2.2.zip

Patch0:		azureus-remove-win32-osx-platforms.patch
Patch2:		azureus-cache-size.patch
Patch3:		azureus-remove-manifest-classpath.patch
Patch8:		azureus-rh-bugzilla-180418.patch
Patch9:		azureus-no-shared-plugins.patch
Patch12:	azureus-no-updates-PluginInitializer.patch
Patch13:	azureus-no-updates-PluginInterfaceImpl.patch
Patch14:	azureus-no-update-manager-AzureusCoreImpl.patch
Patch15:	azureus-no-update-manager-CorePatchChecker.patch
Patch16:	azureus-no-update-manager-CoreUpdateChecker.patch
Patch18:	azureus-no-update-manager-PluginInstallerImpl.patch
Patch19:	azureus-no-update-manager-PluginUpdatePlugin.patch
Patch20:	azureus-no-update-manager-SWTUpdateChecker.patch
Patch22:	azureus-no-update-manager-UpdateMonitor.patch
Patch23:	azureus-no-update-manager-PluginInstallerImpl-2.patch
Patch25:	azureus-no-update-manager-MainStatusBar.patch
Patch27:	azureus-SecureMessageServiceClientHelper-bcprov.patch
Patch28:	azureus-configuration.patch
Patch31:	azureus-fix-menu-MainMenu.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant, jpackage-utils >= 1.5, xml-commons-apis
BuildRequires:  jakarta-commons-cli, log4j
BuildRequires:  libgconf-java
BuildRequires:  bouncycastle >= 1.33-3
BuildRequires:  libswt3-gtk2 >= 3.3.0
Requires:       jakarta-commons-cli, log4j
Requires:	xulrunner
Requires:       libswt3-gtk2 >= 3.3.0
Requires:       libgconf-java
Requires:       bouncycastle >= 1.33-3
Requires:       libgcj >= 4.1.0-0.15
BuildRequires:    java-1.5.0-gcj-devel
BuildRequires:    java-1.7.0-icedtea-devel
Requires:	  java-1.7.0-icedtea
Requires(post):   java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
BuildRequires:    desktop-file-utils
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

%description 
Azureus implements the BitTorrent protocol using java language and
comes bundled with many invaluable features for both beginners and
advanced users.

%prep
%setup -q -n %{name}3
%patch0 -p0
%patch2 -p0
%patch3 -p0
%patch8 -p0
%patch9 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0
%patch16 -p0
%patch18 -p0
%patch19 -p0
%patch20 -p0
%patch22 -p0
%patch23 -p0
%patch25 -p0
%patch27 -p0
%patch28 -p0
%patch31 -p0
cp %{SOURCE4} License.txt

%build
mkdir -p build/libs
build-jar-repository -p build/libs bcprov jakarta-commons-cli log4j gtk2.8 glib0.2
ln -s %{_libdir}/eclipse/swt-gtk-3.3.jar build/libs
find ./ -name osx | xargs rm -r
find ./ -name macosx | xargs rm -r
find ./ -name win32 | xargs rm -r
find ./ -name Win32\* | xargs rm -r
# Remove test code
rm org/gudy/azureus2/ui/swt/test/PrintTransferTypes.java

ant jar

mkdir -p plugins/azplugins
pushd plugins
pushd azplugins
unzip -q %{SOURCE5}
rm -f *.jar `find ./ -name \*class`
find ./ -name \*java | xargs javac -cp %{_libdir}/eclipse/swt-gtk-3.3.jar:../..:.
find ./ -name \*java | xargs rm
jar cvf azplugins_1.9.jar .
popd
popd

unzip -q %{SOURCE6}
pushd plugins
pushd bdcc
unzip *.jar
rm -f *.jar `find ./ -name \*class`
find ./ -name \*java | xargs javac -cp %{_libdir}/eclipse/swt-gtk-3.3.jar:../..:.
find ./ -name \*java | xargs rm
jar cvf bdcc_2.2.2.jar .
popd
popd

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/Azureus2.jar
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/azureus
sed --in-place "s:/usr/lib:%{_libdir}:g" $RPM_BUILD_ROOT%{_bindir}/azureus

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins
install -pm 644 plugins/azplugins/azplugins_1.9.jar $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins/azplugins_1.9.jar
install -pm 644 plugins/azplugins/plugin.properties $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins/plugin.properties

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc
install -pm 644 plugins/bdcc/bdcc_2.2.2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc/bdcc_2.2.2.jar
install -pm 644 plugins/bdcc/plugin.properties $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc/plugin.properties

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a16.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a64.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/azureus.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora 			\
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications	\
	--add-category X-Fedora				\
	%{SOURCE2}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/application-registry
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/application-registry

# Convert line endings...
%{__sed} -i 's/\r//' License.txt
%{__sed} -i 's/\r//' ChangeLog.txt
chmod 644 *.txt

#RPM_OPT_FLAGS="-O0" aot-compile-rpm
aot-compile-rpm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/rebuild-gcj-db
update-desktop-database %{_datadir}/applications
# update icon themes
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%postun
%{_bindir}/rebuild-gcj-db
update-desktop-database %{_datadir}/applications
# update icon themes
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%files
%defattr(-,root,root)
%doc License.txt ChangeLog.txt
%{_datadir}/applications/*
%{_datadir}/application-registry/*
%{_datadir}/pixmaps/azureus.png
%{_datadir}/icons/hicolor/16x16/apps/azureus.png
%{_datadir}/icons/hicolor/32x32/apps/azureus.png
%{_datadir}/icons/hicolor/64x64/apps/azureus.png
%{_bindir}/azureus
%{_datadir}/azureus
%{_libdir}/gcj/*

%changelog
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

* Wed May 29 2006 Anthony Green <green@redhat.com> - 2.4.0.3-0.20060529cvs_1
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
- Be explicit about .png files in %files.

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
