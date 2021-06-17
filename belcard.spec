#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Belledonne Communications' vCard 4 parsing library
Summary(pl.UTF-8):	Biblioteka Belledonne Communications do analizy formatu vCard 4
Name:		belcard
Version:	4.5.20
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/belcard/-/tags
Source0:	https://gitlab.linphone.org/BC/public/belcard/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	6c0ebca77e42cc8591bc2c895458e3ef
Patch0:		%{name}-static.patch
URL:		https://linphone.org/
BuildRequires:	bctoolbox-devel >= 0.0.3
BuildRequires:	bcunit-devel
BuildRequires:	belr-devel >= 4.5.0
BuildRequires:	cmake >= 3.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	xxd
Requires:	bctoolbox >= 0.0.3
Requires:	belr >= 4.5.0
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
Requires:	bctoolbox-devel >= 0.0.3
Requires:	belr-devel >= 4.5.0
Requires:	libstdc++-devel >= 6:4.7

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
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_datadir}/belcard/cmake/belcardTargets.cmake

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
%attr(755,root,root) %{_bindir}/belcard_tester
%attr(755,root,root) %{_libdir}/libbelcard.so.1
%{_datadir}/belcard_tester
# dirs should belong to belr?
%dir %{_datadir}/belr
%dir %{_datadir}/belr/grammars
%{_datadir}/belr/grammars/vcard_grammar

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbelcard.so
%{_includedir}/belcard
%{_pkgconfigdir}/belcard.pc
%dir %{_datadir}/belcard
%{_datadir}/belcard/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbelcard.a
%endif
