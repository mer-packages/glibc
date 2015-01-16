# temporary needed for debuginfo change in rpm package
%define _unpackaged_files_terminate_build 0
%define glibcsrcdir eglibc-2.15
### glibc.spec.in follows:
%define run_glibc_tests 0
%define multiarcharches %{ix86} x86_64



Summary: Embedded GLIBC (EGLIBC) is a variant of the GNU C Library (GLIBC)
Name: glibc
Version: 2.15
Release: 1

# GPLv2+ is used in a bunch of programs, LGPLv2+ is used for libraries.
# Things that are linked directly into dynamically linked programs
# and shared libraries (e.g. crt files, lib*_nonshared.a) have an additional
# exception which allows linking it into any kind of programs or shared
# libraries without restrictions.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System/Libraries
URL: http://www.eglibc.org/
Source0: http://archive.ubuntu.com/ubuntu/pool/main/e/eglibc/eglibc_2.15.orig.tar.gz
Source11: build-locale-archive.c
Patch0: eglibc_2.15-0ubuntu10.9.diff.gz
Patch1: glibc-arm-alignment-fix.patch
Patch2: glibc-arm-runfast.patch
Patch3: glibc-2.13-no-timestamping.patch
Patch4: glibc-2.14.1-elf-rtld.c.1.diff
Patch5: glibc-2.14.1-ldso-rpath-prefix-option.2.diff
Patch6: eglibc-2.15-nsswitchconf-location.3.diff
Patch7: glibc-2.14.1-nscd-socket-location.4.diff
Patch8: glibc-2.14.1-ldso-nodefaultdirs-option.5.diff
Patch9: eglibc-2.15-mips-async-unwind.patch
Patch10: eglibc-2.15-mips-no-n32-n64.patch
Patch11: glibc-2.14-locarchive-fedora.patch
Patch13: eglibc-2.15-use-usrbin-localedef.patch
Patch14: eglibc-2.15-fix-neon-libdl.patch
Patch15: eglibc-2.15-shlib-make.patch
Patch16: glibc-2.15-confstr-strdup.patch
Patch17: eglibc-2.15-libc_message-nobacktrace.patch
Patch18: eglibc-2.15-avoid_infinite_loop.patch

Provides: ldconfig
# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)
Requires: glibc-common = %{version}-%{release}

# This is a short term need until everything is rebuilt in armhf
%ifarch armv7hl armv7nhl armv7tnhl
Provides: ld-linux.so.3
Provides: ld-linux.so.3(GLIBC_2.4)
%endif

# Require libgcc in case some program calls pthread_cancel in its %%post
Requires(pre): libgcc
# This is for building auxiliary programs like memusage, nscd
# For initial glibc bootstraps it can be commented out
#BuildRequires: gd-devel libpng-devel zlib-devel texinfo
BuildRequires:  zlib-devel texinfo
BuildRequires: sed >= 3.95, libcap-devel, gettext
#BuildRequires: /bin/ps, /bin/kill, /bin/awk, procps
BuildRequires: gawk,  util-linux, quilt
# This gcc >= 3.2 is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildRequires: gcc >= 3.2
%define enablekernel 2.6.32
%ifarch %{ix86}
%ifarch i486
%define _target_cpu	i486
%else
%define _target_cpu	i686
%endif
%endif
%ifarch i386
%define nptl_target_cpu i486
%else
%define nptl_target_cpu %{_target_cpu}
%endif

# Need AS_NEEDED directive
# Need --hash-style=* support
BuildRequires: binutils >= 2.19.51.0.10
BuildRequires: gcc >= 3.2.1-5
BuildRequires: elfutils >= 0.72
BuildRequires: rpm >= 4.2-0.56

%define __find_provides %{_builddir}/%{glibcsrcdir}/find_provides.sh
%define _filter_GLIBC_PRIVATE 1

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

%package devel
Summary: Object files for development using standard C libraries
Group: Development/Libraries
Requires(pre): /sbin/install-info
Requires(pre): %{name}-headers
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

%package static
Summary: C library static libraries for -static linking
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

%package headers
Summary: Header files for development using standard C libraries
Group: Development/Libraries
Provides: %{name}-headers(%{_target_cpu})
%ifarch x86_64
# If both -m32 and -m64 is to be supported on AMD64, x86_64 glibc-headers
# have to be installed, not i586 ones.
Obsoletes: %{name}-headers(i586)
Obsoletes: %{name}-headers(i686)
%endif
Requires(pre): kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}-%{release}
BuildRequires: kernel-headers >= 2.6.22

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2003a
Group: System/Base

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

%package -n nscd
Summary: A Name Service Caching Daemon (nscd)
Group: System/Daemons
Requires(pre): /usr/sbin/useradd, /usr/sbin/userdel, sh-utils

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well.

%package utils
Summary: Development utilities from GNU C library
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.


%prep
%setup -q -n %{glibcsrcdir} %{?glibc_release_unpack}
%patch0 -p1
%patch1 -p1
%ifarch %{arm}
%patch2 -p1
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%if 0%{?qemu_user_space_build}
%patch13 -p1
%patch14 -p1
%endif
%patch15 -p1
%patch16 -p2 -R 
%patch17 -p1
%patch18 -p1

# Not well formatted locales --cvm
sed -i "s|^localedata/locale-eo_EO.diff$||g" debian/patches/series
sed -i "s|^localedata/locale-ia.diff$||g" debian/patches/series
# This screws up armv6, as it doesn't have ARMv7 instructions/Thumb2
%ifarch armv6l
sed -i "s|^arm/local-linaro-cortex-strings.diff$||g" debian/patches/series
%endif
QUILT_PATCHES=debian/patches quilt push -a

cat > find_provides.sh <<EOF
#!/bin/sh
/usr/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh
touch `find . -name configure`
touch locale/programs/*-kw.h

%build
GCC=gcc
GXX=g++
echo %{ix86}
%ifarch %{ix86}
%ifarch i486
BuildFlags="-march=i486"
%else
BuildFlags="-march=core2 -mtune=atom"
%endif
%endif

%ifnarch %{arm}
BuildFlags="$BuildFlags -fasynchronous-unwind-tables"
%endif

EnableKernel="--enable-kernel=%{enablekernel}"
echo "$GCC" > Gcc
AddOns=`echo */configure | sed -e 's!/configure!!g;s!\(linuxthreads\|nptl\|rtkaio\|powerpc-cpu\)\( \|$\)!!g;s! \+$!!;s! !,!g;s!^!,!;/^,\*$/d'`

%ifarch %{arm} mipsel
AddOns=,ports$AddOns
%endif

#%ifarch armv7tnhl
# workaround for a potential compiler bug using -mfpu=neon (gcc 4.6 2013.01)
#BuildFlags="$BuildFlags -mfpu=vfpv3-d16"
#%endif

build_nptl()
{
builddir=build-%{nptl_target_cpu}-$1
shift
rm -rf $builddir
mkdir $builddir ; cd $builddir
echo libdir=/usr/lib > configparms
echo slibdir=/lib >> configparms
echo BUILD_CC=gcc >> configparms
%ifarch mipsel
build_CFLAGS="$BuildFlags -g -O1 $*"
%else
build_CFLAGS="$BuildFlags -g -O3 $*"
%endif
../configure CC="$GCC" CXX="$GXX" CFLAGS="$build_CFLAGS" \
	--prefix=%{_prefix} \
	--enable-add-ons=nptl$AddOns --without-cvs $EnableKernel \
	--with-headers=%{_prefix}/include --enable-bind-now \
	--with-tls --with-__thread  \
%ifnarch %{arm}
	--build %{nptl_target_cpu}-%{_vendor}-linux \
	--host %{nptl_target_cpu}-%{_vendor}-linux \
%else
%ifarch armv7hl armv7tnhl armv7nhl
        --build %{nptl_target_cpu}-%{_vendor}-linux-gnueabihf \
        --host %{nptl_target_cpu}-%{_vendor}-linux-gnueabihf \
%else
        --build %{nptl_target_cpu}-%{_vendor}-linux-gnueabi \
        --host %{nptl_target_cpu}-%{_vendor}-linux-gnueabi \
%endif
%endif
%ifarch %{multiarcharches}
	--enable-multi-arch \
%endif
	--disable-profile --enable-experimental-malloc 
make %{?_smp_mflags} -r CFLAGS="$build_CFLAGS" 

cd ..
}

build_nptl linuxnptl

$GCC -Os -static -o build-locale-archive %SOURCE11 \
  ./build-%{nptl_target_cpu}-linuxnptl/locale/locarchive.o \
  ./build-%{nptl_target_cpu}-linuxnptl/locale/md5.o \
  -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
  -L./build-%{nptl_target_cpu}-linuxnptl -I./locale

%install
GCC=`cat Gcc`

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make -j1 install_root=$RPM_BUILD_ROOT install -C build-%{nptl_target_cpu}-linuxnptl PARALLELMFLAGS=
%ifnarch %{auxarches}
cd build-%{nptl_target_cpu}-linuxnptl && \
  make %{?_smp_mflags} install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd` && \
  cd ..
%endif

librtso=`basename $RPM_BUILD_ROOT/%{_lib}/librt.so.*`


# Remove the files we don't want to distribute
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libNoVersion*
rm -f $RPM_BUILD_ROOT/%{_lib}/libNoVersion*

if [ -d $RPM_BUILD_ROOT%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p $RPM_BUILD_ROOT%{_infodir}
  mv -f $RPM_BUILD_ROOT%{_prefix}/info/* $RPM_BUILD_ROOT%{_infodir}
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info
fi

gzip -9nvf $RPM_BUILD_ROOT%{_infodir}/libc*

ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libbsd.a

install -p -m 644 nss/nsswitch.conf $RPM_BUILD_ROOT/etc/nsswitch.conf

mkdir -p $RPM_BUILD_ROOT/etc/default
install -p -m 644 nis/nss $RPM_BUILD_ROOT/etc/default/nss

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT/etc

# Don't include ld.so.cache
rm -f $RPM_BUILD_ROOT/etc/ld.so.cache

# Include ld.so.conf
echo 'include /etc/ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
> $RPM_BUILD_ROOT/etc/ld.so.cache
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
> $RPM_BUILD_ROOT/etc/sysconfig/nscd

# Include %{_prefix}/%{_lib}/gconv/gconv-modules.cache
> $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache

strip -g $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.o

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}
cp -a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.a \
  $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}/
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}/*_p.a
# Now strip debugging info from static libraries
pushd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
for i in *.a; do
  if [ -f $i ]; then
    case "$i" in
    *_p.a) ;;
    *) strip -g -R .comment $i ;;
    esac
  fi
done
popd

# Hardlink identical locale files together
%ifnarch %{auxarches}
#From 2.11, removed hardlink
olddir=`pwd`
pushd ${RPM_BUILD_ROOT}%{_prefix}/lib/locale
rm locale-archive || :
# Intentionally we do not pass --alias-file=, aliases will be added
# by build-locale-archive.
# note that due to qemu-arm emulation behaviour, we need to break this up into multiple invocations.  
# see BMC 10526.

localedef_bin="$olddir/build-%{nptl_target_cpu}-linuxnptl/elf/ld.so --library-path $olddir/build-%{nptl_target_cpu}-linuxnptl/ $olddir/build-%{nptl_target_cpu}-linuxnptl/locale/localedef"

%if 0%{?qemu_user_space_build}
if [ -f /usr/bin/localedef ]; then
    localedef_bin=/usr/bin/localedef
fi
%endif

find . -name '*_*' -maxdepth 1 | xargs -r -n10 -P1 --verbose $localedef_bin --prefix ${RPM_BUILD_ROOT} --add-to-archive

rm -rf *_*
mv locale-archive{,.tmpl}
popd
%endif

%ifarch armv7hl armv7tnhl armv7nhl
ln -s /lib/ld-linux-armhf.so.3 ${RPM_BUILD_ROOT}/lib/ld-linux.so.3
%endif


rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss-*.so.1

# Ugly hack for buggy rpm
ln -f ${RPM_BUILD_ROOT}%{_sbindir}/iconvconfig{,.%{_target_cpu}}

rm -f $RPM_BUILD_ROOT/etc/gai.conf

# In F7+ this is provided by rpcbind rpm
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# BUILD THE FILE LIST
{
  find $RPM_BUILD_ROOT \( -type f -o -type l \) \
       \( \
	 -name etc -printf "%%%%config " -o \
	 -name gconv-modules \
	 -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " -o \
	 -name gconv-modules.cache \
	 -printf "%%%%verify(not md5 size mtime) " \
	 , \
	 ! -path "*/lib/debug/*" -printf "/%%P\n" \)
  find $RPM_BUILD_ROOT -type d \
       \( -path '*%{_prefix}/share/*' ! -path '*%{_infodir}' -o \
	  -path "*%{_prefix}/include/*" -o \
	  -path "*%{_prefix}/lib/locale/*" \
       \) -printf "%%%%dir /%%P\n"
} | {

  # primary filelist
  SHARE_LANG='s|.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo|%lang(\1) &|'
  LIB_LANG='s|.*/lib/locale/\([^/_]\+\)|%lang(\1) &|'
  # rpm does not handle %lang() tagged files hardlinked together accross
  # languages very well, temporarily disable
  LIB_LANG=''
  sed -e "$LIB_LANG" -e "$SHARE_LANG" \
      -e '\,/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\),d' \
      -e '\,/%{_lib}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > rpm.filelist

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}
mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}

grep '%{_infodir}' < rpm.filelist | grep -v '%{_infodir}/dir' > devel.filelist
grep '%{_prefix}/include/gnu/stubs-[32164]\+\.h' < rpm.filelist >> devel.filelist || :

grep '%{_prefix}/include' < rpm.filelist |
  egrep -v '%{_prefix}/include/(linuxthreads|gnu/stubs-[32164]+\.h)' \
	> headers.filelist

sed -i -e '\|%{_prefix}/%{_lib}/lib.*_p.a|d' \
       -e '\|%{_prefix}/include|d' \
       -e '\|%{_infodir}|d' rpm.filelist

grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist \
  | grep '/lib\(\(c\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  > static.filelist
grep '%{_prefix}/%{_lib}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.so' < rpm.filelist >> devel.filelist

sed -i -e '\|%{_prefix}/%{_lib}/lib.*\.a|d' \
       -e '\|%{_prefix}/%{_lib}/.*\.o|d' \
       -e '\|%{_prefix}/%{_lib}/lib.*\.so|d' \
       -e '\|%{_prefix}/%{_lib}/linuxthreads|d' \
       -e '\|nscd|d' rpm.filelist

grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
#grep '%{_prefix}/lib/locale' < rpm.filelist | grep -v /locale-archive.tmpl >> common.filelist
#grep '%{_prefix}/libexec/pt_chown' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
grep '%{_prefix}/share' < rpm.filelist | \
  grep -v '%{_prefix}/share/zoneinfo' >> common.filelist

sed -i -e '\|%{_prefix}/bin|d' \
       -e '\|%{_prefix}/lib/locale|d' \
       -e '\|%{_prefix}/libexec/pt_chown|d' \
       -e '\|%{_prefix}/sbin/[^gi]|d' \
       -e '\|%{_prefix}/share|d' rpm.filelist

> nosegneg.filelist

echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist
echo '%{_prefix}/sbin/nscd' > nscd.filelist

cat > utils.filelist <<EOF
%{_prefix}/%{_lib}/libmemusage.so
%{_prefix}/%{_lib}/libpcprofile.so
#%{_prefix}/bin/memusage
#%{_prefix}/bin/memusagestat
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

# /etc/localtime
rm -f $RPM_BUILD_ROOT/etc/localtime
cp -f $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime
#ln -sf ..%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime

rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp
touch -r timezone/northamerica $RPM_BUILD_ROOT/etc/ld.so.conf
touch -r timezone/northamerica $RPM_BUILD_ROOT/etc/localtime
touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT/etc/rpc


# the last bit: more documentation
rm -rf documentation
mkdir documentation
cp crypt/README.ufc-crypt documentation/README.ufc-crypt
cp timezone/README documentation/README.timezone
cp ChangeLog{,.15,.16} documentation
bzip2 -9 documentation/ChangeLog*
cp posix/gai.conf documentation/

%if 0%{run_glibc_tests}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================
cd build-%{nptl_target_cpu}-linuxnptl
( make %{?_smp_mflags} -k check PARALLELMFLAGS=-s 2>&1
  sleep 10s
  teepid="`ps -eo ppid,pid,command | awk '($1 == '${parent}' && $3 ~ /^tee/) { print $2 }'`"
  [ -n "$teepid" ] && kill $teepid
) | tee check.log || :
cd ..
echo ====================TESTING DETAILS=================
for i in `sed -n 's|^.*\*\*\* \[\([^]]*\.out\)\].*$|\1|p' build-*-linux*/check.log`; do
  echo =====$i=====
  cat $i || :
  echo ============
done
echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

%endif

pushd $RPM_BUILD_ROOT/usr/%{_lib}/
$GCC -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
rm libpthread.a
ar rcs libpthread.a libpthread.o
rm libpthread.o
popd


rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%ifarch %{auxarches}

echo Cutting down the list of unpackaged files
>> debuginfocommon.filelist
sed -e '/%%dir/d;/%%config/d;/%%verify/d;s/%%lang([^)]*) //;s#^/*##' \
    common.filelist devel.filelist static.filelist headers.filelist \
    utils.filelist nscd.filelist debuginfocommon.filelist |
(cd $RPM_BUILD_ROOT; xargs --no-run-if-empty rm -f 2> /dev/null || :)

%else

mkdir -p $RPM_BUILD_ROOT/var/{db,run}/nscd
touch $RPM_BUILD_ROOT/var/{db,run}/nscd/{passwd,group,hosts,services}
touch $RPM_BUILD_ROOT/var/run/nscd/{socket,nscd.pid}
%endif

%ifnarch %{auxarches}
> $RPM_BUILD_ROOT/%{_prefix}/lib/locale/locale-archive
%endif

install -m 700 build-locale-archive $RPM_BUILD_ROOT/usr/sbin/build-locale-archive

mkdir -p $RPM_BUILD_ROOT/var/cache/ldconfig
> $RPM_BUILD_ROOT/var/cache/ldconfig/aux-cache

%postun -p /sbin/ldconfig

%post devel
%install_info %{_infodir}/libc.info.gz %{_infodir}/dir

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%preun devel
if [ "$1" = 0 ]; then
  %install_info --delete %{_infodir}/libc.info.gz %{_infodir}/dir
fi

%post utils -p /sbin/ldconfig

%postun utils -p /sbin/ldconfig

%post common -p /usr/sbin/build-locale-archive

%pre -n nscd
/usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
  -c "NSCD Daemon" -u 28 nscd > /dev/null 2>&1 || :

%postun -n nscd
if [ $1 = 0 ] ; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
if [ "$1" -ge "1" ]; then
  service nscd condrestart > /dev/null 2>&1 || :
fi


%files -f rpm.filelist
%defattr(-,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/localtime
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%ifarch armv7hl armv7tnhl armv7nhl 
/lib/ld-linux.so.3
%endif
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_prefix}/%{_lib}/gconv
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS CONFORMANCE
%doc COPYING COPYING.LIB README.libm LICENSES
%doc hesiod/README.hesiod


%ifnarch %{auxarches}
%files -f common.filelist common
%defattr(-,root,root)
%dir %{_prefix}/lib/locale
%attr(0644,root,root) %verify(not md5 size mtime) %{_prefix}/lib/locale/locale-archive.tmpl
%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/lib/locale/locale-archive
%dir %attr(755,root,root) /etc/default
%verify(not md5 size mtime) %config(noreplace) /etc/default/nss
%attr(4711,root,root) %{_prefix}/libexec/pt_chown
%doc documentation/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f static.filelist static
%defattr(-,root,root)

%files -f headers.filelist headers
%defattr(-,root,root)

%files -f utils.filelist utils
%defattr(-,root,root)

%files -f nscd.filelist -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%dir %attr(0755,root,root) /var/run/nscd
%dir %attr(0755,root,root) /var/db/nscd
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/services
%ghost %config(missingok,noreplace) /etc/sysconfig/nscd
%endif

