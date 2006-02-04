Name:           azureus
Version:        2.3.0.6
Release:        23%{?dist}
Summary:        A BitTorrent Client

Group:          Applications/Internet
License:        GPL
URL:            http://azureus.sourceforge.net

# This is just the upstream Azureus_2.3.0.6_source.zip file with 
# the crypto code removed (org/bouncycastle).
Source0:        Azureus_2.3.0.6_source_nocrypto.zip

Source1:        azureus.script
Source2:        Azureus.desktop
Source3:        azureus.applications
Source4:        azureus-License.txt
Source5:        azureus-ChangeLog.txt

Patch0:         azureus-sun.misc.Cleaner.patch
Patch1:         azureus-sun.misc.Signal.patch
Patch2:         azureus-java.beans.XMLEncoder.patch
Patch3:         azureus-remove-win32-osx-platforms.patch
Patch4:         azureus-remove-win32-PlatformManagerUpdateChecker.patch
Patch5:         azureus-jessie.patch
Patch6:         azureus-GKR.patch
Patch7:         azureus-ConfigurationManager-improvement.patch
Patch8:         azureus-base64.patch
Patch9:         azureus-no-bouncycastle.patch
Patch10:        azureus-cache-size.patch
Patch11:        azureus-remove-manifest-classpath.patch
Patch12:        azureus-themed.patch
Patch13:        azureus-no-shared-plugins.patch
Patch14:        azureus-no-shared-plugins2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant, jpackage-utils >= 1.5, xml-commons-apis
BuildRequires:  jakarta-commons-cli, libswt3-gtk2 >= 3.1.2, log4j, gnu-crypto, libgtk-java, glib-java
Requires:       jakarta-commons-cli, libswt3-gtk2 >= 3.1.2, log4j, gnu-crypto, libgtk-java, glib-java
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
%setup -q -c %{name}-%{version}
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
cp %{SOURCE4} License.txt
cp %{SOURCE5} ChangeLog.txt

%build
mkdir -p build/libs
build-jar-repository build/libs jakarta-commons-cli swt-gtk-3.1.2 log4j gnu-crypto gtk2.8 glib0.2
find ./ -name osx | xargs rm -r
find ./ -name macosx | xargs rm -r
find ./ -name [Ww]in32\* | xargs rm -r
# Remove the BouncyCastle security manager.
rm org/gudy/azureus2/core3/security/impl/SESecurityManagerBC.java
# Remove test code
rm org/gudy/azureus2/ui/console/multiuser/TestUserManager.java
rm org/gudy/azureus2/ui/swt/test/PrintTransferTypes.java
ant jar

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_javadir}/Azureus2.jar
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/azureus

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
%{_javadir}/*.jar
%{_libdir}/gcj/*

%changelog
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
