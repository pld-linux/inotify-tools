#
# Conditional build:
%bcond_with	doxygen		# build with doxygen support
%bcond_without	static_libs	# don't build static library
#
Summary:	inotify-tools provides a simple interface to inotify
Summary(pl.UTF-8):	inotify-tools dostarcza interfejs do inotify
Name:		inotify-tools
Version:	3.13
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/inotify-tools/%{name}-%{version}.tar.gz
# Source0-md5:	35d7178297390f18bae451e083362acf
URL:		http://inotify-tools.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
inotify-tools is a C library and a set of command-line programs for
Linux providing a simple interface to inotify. These programs can be
used to monitor and act upon filesystem events. The programs are
written in C and have no dependencies other than a Linux kernel
supporting inotify.

%description -l pl.UTF-8
inotify-tools jest zestawem bibliotek i programów napisanych w C
dostarczającym interfejsu do inotify dla Linuksa. Programy te mogą
służyć do monitorowania systemu plików jak również do wykonywania
operacji na podstawie zachodzących w systemie plików zdarzeń. Poza
obsługą inotify w jądrze Linuksa nie są wymagane żadne dodatkowe
zależności.

%package libs
Summary:	Libraries for inotify-tools
Summary(pl.UTF-8):	Biblioteki do inotify-tools
Group:		Libraries

%description libs
Libraries for inotify-tools.

%description libs -l pl.UTF-8
Biblioteki do inotify-tools.

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
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	%{?with_doxygen:--enable-doxygen}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/doc/%{name} $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/inotifywait.1*
%{_mandir}/man1/inotifywatch.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinotifytools.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinotifytools.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinotifytools.so
%{_libdir}/libinotifytools.la
%{_includedir}/inotifytools

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libinotifytools.a
%endif
