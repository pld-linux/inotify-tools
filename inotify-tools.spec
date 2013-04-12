#
# Conditional build:
%bcond_with	doxygen		# build with doxygen support
%bcond_without	static_libs	# don't build static library
#
Summary:	inotify-tools provides a simple interface to inotify
Summary(pl.UTF-8):	inotify-tools dostarcza interfejs do inotify
Name:		inotify-tools
Version:	3.14
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://github.com/downloads/rvoicilas/inotify-tools/%{name}-%{version}.tar.gz
# Source0-md5:	b43d95a0fa8c45f8bab3aec9672cf30c
URL:		http://inotify-tools.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
inotify-tools is a C library and a set of command-line programs for
Linux providing a simple interface to inotify. These programs can be
used to monitor and act upon filesystem events. The programs are
written in C and have no dependencies other than a Linux kernel
supporting inotify.

%description -l pl.UTF-8
inotify-tools jest zestawem składającym się z biblioteki C oraz
działających z linii poleceń programów, zapewniających prosty
interfejs do systemu inotify w Linuksie. Programy te mogą służyć do
monitorowania systemu plików jak również do wykonywania operacji na
podstawie zachodzących w systemie plików zdarzeń. Poza obsługą inotify
w jądrze Linuksa nie są wymagane żadne dodatkowe zależności.

%package libs
Summary:	Shared inotify-tools library
Summary(pl.UTF-8):	Biblioteka współdzielona inotify-tools
Group:		Libraries

%description libs
Shared inotify-tools library.

%description libs -l pl.UTF-8
Biblioteka współdzielona inotify-tools.

%package devel
Summary:	Header files for inotify-tools library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki inotify-tools
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for inotify-tools library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki inotify-tools.

%package static
Summary:	Static inotify-tools library
Summary(pl.UTF-8):	Statyczna biblioteka dla inotify-tools
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static inotify-tools library.

%description static -l pl.UTF-8
Statyczna biblioteka inotify-tools.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static%{!?with_static_libs:=no} \
	%{?with_doxygen:--enable-doxygen}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc in -devel
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/inotifywait
%attr(755,root,root) %{_bindir}/inotifywatch
%{_mandir}/man1/inotifywait.1*
%{_mandir}/man1/inotifywatch.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinotifytools.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinotifytools.so.0

%files devel
%defattr(644,root,root,755)
%doc libinotifytools/src/doc/html/*
%attr(755,root,root) %{_libdir}/libinotifytools.so
%{_libdir}/libinotifytools.la
%{_includedir}/inotifytools

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libinotifytools.a
%endif
