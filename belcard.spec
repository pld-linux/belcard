#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Belledonne Communications' vCard 4 parsing library
Summary(pl.UTF-8):	Biblioteka Belledonne Communications do analizy formatu vCard 4
Name:		belcard
Version:	1.0.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://linphone.org/releases/sources/belcard/%{name}-%{version}.tar.gz
# Source0-md5:	35f227dfa46be16d4b7ecfd828e1887e
Patch0:		%{name}-pc.patch
URL:		https://linphone.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	bctoolbox-devel >= 0.0.3
BuildRequires:	bcunit-devel
BuildRequires:	belr-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	xxd
Requires:	bctoolbox >= 0.0.3
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
Requires:	belr-devel
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
%setup -q -n %{name}-%{version}-0
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbelcard.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/belcard-folder
%attr(755,root,root) %{_bindir}/belcard-parser
%attr(755,root,root) %{_bindir}/belcard-unfolder
%attr(755,root,root) %{_libdir}/libbelcard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbelcard.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbelcard.so
%{_includedir}/belcard
%{_pkgconfigdir}/belcard.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbelcard.a
%endif
