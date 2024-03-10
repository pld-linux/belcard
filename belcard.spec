#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Belledonne Communications' vCard 4 parsing library
Summary(pl.UTF-8):	Biblioteka Belledonne Communications do analizy formatu vCard 4
Name:		belcard
Version:	5.3.29
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/belcard/-/tags
Source0:	https://gitlab.linphone.org/BC/public/belcard/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	1e05ff8d67569ef4a6c132239d3732d5
URL:		https://linphone.org/
BuildRequires:	bctoolbox-devel >= 5.3.0
BuildRequires:	bcunit-devel
BuildRequires:	belr-devel >= 5.3.0
BuildRequires:	cmake >= 3.22
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	xxd
Requires:	bctoolbox >= 5.3.0
Requires:	belr >= 5.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Belcard is a C++ library to manipulate VCard standard format.

%description -l pl.UTF-8
Belcard to biblioteka C++ do operacji na danych w standardzie VCard.

%package devel
Summary:	Header files for BelCard library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki BelCard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bctoolbox-devel >= 5.3.0
Requires:	belr-devel >= 5.3.0
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for BelCard library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki BelCard.

%package static
Summary:	Static BelCard library
Summary(pl.UTF-8):	Statyczna biblioteka BelCard
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static BelCard library.

%description static -l pl.UTF-8
Statyczna biblioteka BelCard.

%prep
%setup -q

%build
%if %{with static_libs}
%cmake -B builddir-static \
	-DBUILD_SHARED_LIBS=OFF \
	-DENABLE_UNIT_TESTS=OFF \
	-DENABLE_TOOLS=OFF

%{__make} -C builddir-static
%endif

%cmake -B builddir

%{__make} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# missing from cmake
test ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/belcard.pc
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -e 's,@CMAKE_INSTALL_PREFIX@,%{_prefix},' \
	-e 's,@PROJECT_NAME@,belcard,' \
	-e 's,@PROJECT_VERSION@,%{version},' \
	-e 's,@CMAKE_INSTALL_FULL_LIBDIR@,%{_libdir},' \
	-e 's,@LIBS_PRIVATE@,-lbelr -lbctoolbox,' \
	-e 's,@CMAKE_INSTALL_FULL_INCLUDEDIR@,%{_includedir},' \
	belcard.pc.in >$RPM_BUILD_ROOT%{_pkgconfigdir}/belcard.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/belcard-folder
%attr(755,root,root) %{_bindir}/belcard-parser
%attr(755,root,root) %{_bindir}/belcard-unfolder
%attr(755,root,root) %{_bindir}/belcard-tester
%attr(755,root,root) %{_libdir}/libbelcard.so.1
%{_datadir}/belcard-tester
%{_datadir}/belr/grammars/vcard_grammar

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbelcard.so
%{_includedir}/belcard
%{_pkgconfigdir}/belcard.pc
%dir %{_datadir}/BelCard
%{_datadir}/BelCard/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbelcard.a
%endif
