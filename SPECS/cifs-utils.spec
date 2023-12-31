#% define pre_release rc1
%define pre_release %nil

Name:            cifs-utils
Version:         7.0
Release:         1%{pre_release}%{?dist}
Summary:         Utilities for mounting and managing CIFS mounts

Group:           System Environment/Daemons
License:         GPLv3
URL:             http://linux-cifs.samba.org/cifs-utils/

BuildRequires:   libcap-ng-devel libtalloc-devel krb5-devel keyutils-libs-devel autoconf automake libwbclient-devel pam-devel
BuildRequires:   python3-docutils

Requires:        keyutils
Requires(post):  /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives

Source0:         https://download.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
Patch1:          0001-Use-explicit-usr-bin-python3.patch

%description
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains tools for mounting
shares on Linux using the SMB/CIFS protocol. The tools in this package
work in conjunction with support in the kernel to allow one to mount a
SMB/CIFS share onto a client and use it as if it were a standard Linux
file system.

%package devel
Summary:        Files needed for building plugins for cifs-utils
Group:          Development/Libraries

%description devel
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains the header file
necessary for building ID mapping plugins for cifs-utils.

%package -n pam_cifscreds
Summary:        PAM module to manage NTLM credentials in kernel keyring
Group:          System Environment/Base

%description -n pam_cifscreds
The pam_cifscreds PAM module is a tool for automatically adding
credentials (username and password) for the purpose of establishing
sessions in multiuser mounts.

When a cifs filesystem is mounted with the "multiuser" option, and does
not use krb5 authentication, it needs to be able to get the credentials
for each user from somewhere. The pam_cifscreds module can be used to
provide these credentials to the kernel automatically at login.

%prep
%setup -q -n %{name}-%{version}%{pre_release}
%patch1 -p1

%build
autoreconf -i
%configure --prefix=/usr ROOTSBINDIR=%{_sbindir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/getcifsacl
%{_bindir}/setcifsacl
%{_bindir}/cifscreds
%{_bindir}/smbinfo
%{_bindir}/smb2-quota
%{_sbindir}/mount.cifs
%{_sbindir}/mount.smb3
%{_sbindir}/cifs.upcall
%{_sbindir}/cifs.idmap
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/idmapwb.so
%{_mandir}/man1/getcifsacl.1.gz
%{_mandir}/man1/setcifsacl.1.gz
%{_mandir}/man1/cifscreds.1.gz
%{_mandir}/man1/smbinfo.1.gz 
%{_mandir}/man1/smb2-quota.1.gz
%{_mandir}/man8/cifs.upcall.8.gz
%{_mandir}/man8/cifs.idmap.8.gz
%{_mandir}/man8/mount.cifs.8.gz
%{_mandir}/man8/mount.smb3.8.gz
%{_mandir}/man8/idmapwb.8.gz
%dir %{_sysconfdir}/cifs-utils
%ghost %{_sysconfdir}/cifs-utils/idmap-plugin
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf

%post
/usr/sbin/alternatives --install /etc/cifs-utils/idmap-plugin cifs-idmap-plugin %{_libdir}/%{name}/idmapwb.so 10

%preun
if [ $1 = 0 ]; then
	/usr/sbin/alternatives --remove cifs-idmap-plugin %{_libdir}/%{name}/idmapwb.so
fi

%files devel
%{_includedir}/cifsidmap.h

%files -n pam_cifscreds
%{_libdir}/security/pam_cifscreds.so
%{_mandir}/man8/pam_cifscreds.8.gz

%changelog
* Mon Jan 30 2023 Pavel Filipenský <pfilipen@redhat.com> - 7.0-1
- Update to cifs-utils-7.0
- Resolves: rhbz#2163373

* Thu Dec 12 2019 Sachin Prabhu <sprabhu@redhat.com> - 6.8-3
- Add manual gating tests
- docs: cleanup rst formating
- mount.cifs.rst: document new (no)handlecache mount option
- manpage: update mount.cifs manpage with info about rdma option
- checkopts: add python script to cross check mount options
- mount.cifs.rst: document missing options, correct wrong ones
- checkopts: report duplicated options in man page
- mount.cifs.rst: more cleanups
- mount.cifs.rst: document vers=3 mount option
- mount.cifs.rst: document vers=3.02 mount option
- cifs: Allow DNS resolver key to expire
- mount.cifs: be more verbose and helpful regarding mount errors
- Update mount.cifs with vers=default mount option and SMBv3.0.2
- mount.cifs.rst: update vers=3.1.1 option description
- getcifsacl: Do not go to parse_sec_desc if getxattr fails.
- getcifsacl: Improve help usage and add -h option.
- setcifsacl: fix adding ACE when owner sid in unexpected location
- cifs.upcall: fix a compiler warning
- mount.cifs Add various missing parms from the help text
- mount.cifs: add more options to help message
- mount.cifs: detect GMT format of snapshot version
- Update man page for mount.cifs to add new options
- mount.cifs.rst: mention kernel version for snapshots
- Fix authors and maintainers

* Tue Jul 17 2018 Alexander Bokovoy <abokovoy@redhat.com> - 6.8-2
- Use Python 3 version of rst2man utility for generating man pages

* Tue Apr 10 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.8-1
- update to 6.8 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Jeff Layton <jlayton@redhat.com> - 6.7-5
- more updates, switch to rst for manpages
- update mount.cifs manpage to describe defaults better (BZ#1474539)

* Sun Oct 29 2017 Jeff Layton <jlayton@redhat.com> - 6.7-4
- pull in all patches merged since 6.7 was released

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 02 2017 Jeff Layton <jlayton@redhat.com> - 6.7-1
- update to 6.7 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 07 2016 Jeff Layton <jlayton@redhat.com> - 6.6-1
- update to 6.6 release

* Wed Aug 24 2016 Jeff Layton <jlayton@redhat.com> - 6.5-3
- more cifs.upcall cleanup work

* Wed Aug 24 2016 Jeff Layton <jlayton@redhat.com> - 6.5-2
- clean up and streamline cifs.upcall handling for GSSAPI

* Thu Mar 10 2016 Sachin Prabhu <sprabhu@redhat.com> - 6.5-1
- Update to 6.5 release
- Fix URL to cifs-utils upstream source

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 21 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 6.4-3
- Let package own %%{_sysconfdir}/cifs-utils (RHBZ#1184390).
- Let package own %%{_libdir}/cifs-utils (RHBZ#1184391).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Sachin Prabhu <sprabhu@redhat.com> - 6.4-1
- update to 6.4 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Sachin Prabhu <sprabhu@redhat.com> 6.3-2
- autoconf: allow PAM security install directory to be configurable
- cifs: use krb5_kt_default() to determine default keytab location
- cifskey: better use snprintf()
- cifscreds: better error handling when key_search fails
- cifscreds: better error handling for key_add

* Thu Jan 09 2014 Jeff Layton <jlayton@redhat.com> 6.3-1
- update to 6.3 release

* Fri Dec 13 2013 Jeff Layton <jlayton@redhat.com> 6.2-5
- fix linking of wbclient
- add pam_cifscreds module and manpage

* Mon Oct 14 2013 Jeff Layton <jlayton@redhat.com> 6.2-4
- fix use-after-free in asn1_write

* Fri Oct 11 2013 Jeff Layton <jlayton@redhat.com> 6.2-3
- fixes for bugs reported by coverity:
- update bad bit shift patch with one that patches getcifsacl.c too
- remove some dead code from getcifsacl.c, asn1.c, and data_blob.c
- fix bad handling of allocated memory in del_mtab in mount.cifs.c

* Wed Oct 09 2013 Jeff Layton <jlayton@redhat.com> 6.2-2
- fix bad bit shift in setcifsacl.c

* Fri Oct 04 2013 Jeff Layton <jlayton@redhat.com> 6.2-1
- update to 6.2 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Jeff Layton <jlayton@redhat.com> 6.1-3
- allow setcifsacl to work if plugin can't be loaded (bz#984087)

* Mon Jul 15 2013 Jeff Layton <jlayton@redhat.com> 6.1-2
- Convert idmapping plugin symlink to use alternatives system (bz#984088)

* Tue Jul 02 2013 Jeff Layton <jlayton@redhat.com> 6.1-1
- update to 6.1 release

* Mon Mar 25 2013 Jeff Layton <jlayton@redhat.com> 6.0-1
- update to 6.0 release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Jeff Layton <jlayton@redhat.com> 5.9-3
- comment fixes in cifsidmap.h

* Sun Jan 13 2013 Jeff Layton <jlayton@redhat.com> 5.9-2
- fix regression in credential file handling

* Mon Jan 07 2013 Jeff Layton <jlayton@redhat.com> 5.9-1
- update to 5.9
- move mount.cifs to /usr/sbin per new packaging guidelines
- add -devel package to hold cifsidmap.h

* Sun Nov 11 2012 Jeff Layton <jlayton@redhat.com> 5.8-1
- update to 5.8

* Wed Nov 07 2012 Jeff Layton <jlayton@redhat.com> 5.7-3
- update to latest patches queued for 5.8. More idmapping and ACL tool fixes.

* Sun Nov 04 2012 Jeff Layton <jlayton@redhat.com> 5.7-2
- update to latest patches queued for 5.8. Mostly idmapping and ACL tool fixes.

* Tue Oct 09 2012 Jeff Layton <jlayton@redhat.com> 5.7-1
- update to 5.7

* Fri Aug 24 2012 Jeff Layton <jlayton@redhat.com> 5.6-2
- update to current upstream head

* Thu Jul 26 2012 Jeff Layton <jlayton@redhat.com> 5.6-1
- update to 5.6

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Jeff Layton <jlayton@redhat.com> 5.5-2
- remove -Werror flag
- enable PIE and RELRO

* Wed May 30 2012 Jeff Layton <jlayton@redhat.com> 5.5-1
- update to 5.5

* Wed Apr 25 2012 Jeff Layton <jlayton@redhat.com> 5.4-2
- rebuild to fix dependencies due to libwbclient changes

* Wed Apr 18 2012 Jeff Layton <jlayton@redhat.com> 5.4-1
- update to 5.4
- add patch to fix up more warnings

* Mon Mar 19 2012 Jeff Layton <jlayton@redhat.com> 5.3-4
- fix tests for strtoul success (bz# 800621)

* Wed Feb 08 2012 Jeff Layton <jlayton@redhat.com> 5.3-3
- revert mount.cifs move. It's unnecessary at this point.

* Wed Feb 08 2012 Jeff Layton <jlayton@redhat.com> 5.3-2
- move mount.cifs to /usr/sbin per new packaging guidelines

* Sat Jan 28 2012 Jeff Layton <jlayton@redhat.com> 5.3-1
- update to 5.3

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Jeff Layton <jlayton@redhat.com> 5.2-2
- add /etc/request-key.d files

* Fri Dec 09 2011 Jeff Layton <jlayton@redhat.com> 5.2-1
- update to 5.2

* Fri Sep 23 2011 Jeff Layton <jlayton@redhat.com> 5.1-1
- update to 5.1
- add getcifsacl and setcifsacl to package

* Fri Jul 29 2011 Jeff Layton <jlayton@redhat.com> 5.0-2
- mount.cifs: fix check_newline retcode check (bz# 726717)

* Wed Jun 01 2011 Jeff Layton <jlayton@redhat.com> 5.0-1
- update to 5.0

* Mon May 16 2011 Jeff Layton <jlayton@redhat.com> 4.9-2
- mount.cifs: pass unadulterated device string to kernel (bz# 702664)

* Fri Mar 04 2011 Jeff Layton <jlayton@redhat.com> 4.9-1
- update to 4.9

* Tue Feb 08 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-4
- mount.cifs: reenable CAP_DAC_READ_SEARCH when mounting (bz# 675761)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-2
- mount.cifs: don't update mtab if it's a symlink (bz# 674101)

* Fri Jan 21 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-1
- update to 4.8.1

* Sat Jan 15 2011 Jeff Layton <jlayton@redhat.com> 4.8-1
- update to 4.8

* Tue Oct 19 2010 Jeff Layton <jlayton@redhat.com> 4.7-1
- update to 4.7

* Fri Jul 30 2010 Jeff Layton <jlayton@redhat.com> 4.6-1
- update to 4.6

* Tue Jun 01 2010 Jeff Layton <jlayton@redhat.com> 4.5-2
- mount.cifs: fix parsing of cred= option (BZ#597756)

* Tue May 25 2010 Jeff Layton <jlayton@redhat.com> 4.5-1
- update to 4.5

* Thu Apr 29 2010 Jeff Layton <jlayton@redhat.com> 4.4-3
- mount.cifs: fix regression in prefixpath patch

* Thu Apr 29 2010 Jeff Layton <jlayton@redhat.com> 4.4-2
- mount.cifs: strip leading delimiter from prefixpath

* Wed Apr 28 2010 Jeff Layton <jlayton@redhat.com> 4.4-1
- update to 4.4

* Sat Apr 17 2010 Jeff Layton <jlayton@redhat.com> 4.3-2
- fix segfault when address list is exhausted (BZ#583230)

* Fri Apr 09 2010 Jeff Layton <jlayton@redhat.com> 4.3-1
- update to 4.3

* Fri Apr 02 2010 Jeff Layton <jlayton@redhat.com> 4.2-1
- update to 4.2

* Tue Mar 23 2010 Jeff Layton <jlayton@redhat.com> 4.1-1
- update to 4.1

* Mon Mar 08 2010 Jeff Layton <jlayton@redhat.com> 4.0-2
- fix bad pointer dereference in IPv6 scopeid handling

* Wed Mar 03 2010 Jeff Layton <jlayton@redhat.com> 4.0-1
- update to 4.0
- minor specfile fixes

* Fri Feb 26 2010 Jeff Layton <jlayton@redhat.com> 4.0-1rc1
- update to 4.0rc1
- fix prerelease version handling

* Mon Feb 08 2010 Jeff Layton <jlayton@redhat.com> 4.0a1-1
- first RPM package build

