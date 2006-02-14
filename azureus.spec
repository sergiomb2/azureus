Name:           azureus
Version:        2.4.0.0
Release:        0.20060209cvs_1%{?dist}
Summary:        A BitTorrent Client

Group:          Applications/Internet
License:        GPL
URL:            http://azureus.sourceforge.net

# A cvs snapshot with the build and bouncycastle directories
# removed.
Source0:        azureus2-cvs-20060209.tar.gz

Source1:        azureus.script
Source2:        Azureus.desktop
Source3:        azureus.applications
Source4:        azureus-License.txt
Source5:        azureus-ChangeLog.txt

Source6:	azplugins_1.8.8.jar
Source7:	bdcc_2.2.2.zip

Patch0:         azureus-remove-win32-osx-platforms.patch
Patch1:         azureus-remove-win32-PlatformManagerUpdateChecker.patch
Patch2:         azureus-cache-size.patch
Patch3:         azureus-remove-manifest-classpath.patch
Patch4:         azureus-ConfigSectionPlugins-swt-3.1.patch
Patch5:         azureus-Messages-swt-3.1.patch
Patch6:         azureus-TableView-swt-3.1.patch
Patch7:         azureus-themed.patch
Patch8:         azureus-rh-bugzilla-180418.patch
Patch9:         azureus-no-shared-plugins.patch
Patch10:        azureus-no-install-remove-plugins.patch
Patch11:        azureus-no-restart.patch
Patch12:        azureus-no-updates-PluginInitializer.patch
Patch13:        azureus-no-updates-PluginInterfaceImpl.patch
Patch14:        azureus-no-update-manager-AzureusCoreImpl.patch
Patch15:        azureus-no-update-manager-CorePatchChecker.patch
Patch16:        azureus-no-update-manager-CoreUpdateChecker.patch
Patch17:        azureus-no-update-manager-MainWindow.patch
Patch18:        azureus-no-update-manager-PluginInstallerImpl.patch
Patch19:        azureus-no-update-manager-PluginUpdatePlugin.patch
Patch20:        azureus-no-update-manager-SWTUpdateChecker.patch
#Patch21:        azureus-no-update-manager-TableView.patch
Patch22:        azureus-no-update-manager-UpdateMonitor.patch
Patch23:        azureus-no-update-manager-PluginInstallerImpl-2.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant, jpackage-utils >= 1.5, xml-commons-apis
BuildRequires:  jakarta-commons-cli, libswt3-gtk2, log4j, gnu-crypto
BuildRequires:  libgconf-java
Requires:       jakarta-commons-cli, libswt3-gtk2, log4j, gnu-crypto
Requires:       libgconf-java
Requires:       libgcj >= 4.1.0-0.15
BuildRequires:    java-gcj-compat-devel >= 1.0.31
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
%setup -q -n %{name}2
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p0
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0
%patch16 -p0
%patch17 -p0
%patch18 -p0
%patch19 -p0
%patch20 -p0
#%patch21 -p0
%patch22 -p0
%patch23 -p0
cp %{SOURCE4} License.txt
cp %{SOURCE5} ChangeLog.txt

%build
mkdir -p build/libs
build-jar-repository build/libs jakarta-commons-cli swt-gtk-3.1.1 log4j gnu-crypto gtk2.8 glib0.2
ln -s /usr/share/java/gcj-endorsed/bcprov-131.jar build/libs
find ./ -name osx | xargs rm -r
find ./ -name macosx | xargs rm -r
find ./ -name [Ww]in32\* | xargs rm -r
# Remove test code
rm org/gudy/azureus2/ui/swt/test/PrintTransferTypes.java

ant jar

mkdir -p plugins/azplugins
cd plugins/azplugins
unzip -q %{SOURCE6}
rm -f *.jar `find ./ -name \*class`
find ./ -name \*java | xargs javac -cp `build-classpath swt-gtk-3.1.1`:../..:.
find ./ -name \*java | xargs rm
jar cvf azplugins_1.8.8.jar .
cd ../..

unzip -q %{SOURCE7}
cd plugins/bdcc
unzip *.jar
rm -f *.jar `find ./ -name \*class`
find ./ -name \*java | xargs javac -cp `build-classpath swt-gtk-3.1.1`:../..:.
find ./ -name \*java | xargs rm
jar cvf bdcc_2.2.2.jar .
cd ../..

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/Azureus2.jar
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/azureus

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins
install -pm 644 plugins/azplugins/azplugins_1.8.8.jar $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins/azplugins_1.8.8.jar
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
