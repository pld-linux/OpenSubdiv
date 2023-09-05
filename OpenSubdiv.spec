# TODO: CUDA support on bcond
#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Open-Source subdivision surface library
Summary(pl.UTF-8):	Mająca otwarte źródła biblioteka podpodziału powierzchni
Name:		OpenSubdiv
Version:	3.5.1
%define	tagver	%(echo %{version} | tr . _)
Release:	1
License:	Modified Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/PixarAnimationStudios/OpenSubdiv/tags
Source0:	https://github.com/PixarAnimationStudios/OpenSubdiv/archive/v%{tagver}/%{name}-%{tagver}.tar.gz
# Source0-md5:	15a2e1df83463116a37309156e138e43
Patch0:		%{name}-tbb.patch
URL:		https://github.com/PixarAnimationStudios/OpenSubdiv
BuildRequires:	OpenCL-devel >= 1.1
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	clew-devel
BuildRequires:	cmake >= 3.12
BuildRequires:	glew-devel
BuildRequires:	glfw-devel >= 3.0.0
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	ptex-devel >= 2.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tbb-devel >= 4.0
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	docutils
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenSubdiv is a set of open source libraries that implement high
performance subdivision surface (subdiv) evaluation on massively
parallel CPU and GPU architectures. This codepath is optimized for
drawing deforming subdivs with static topology at interactive
framerates. The resulting limit surface matches Pixar's Renderman to
numerical precision.

%description -l pl.UTF-8
OpenSubdiv to zestaw mających otwarte źródła bibliotek z implementacją
wyznaczania powierzchni podpodziału w architekturach dużego
zrównoleglenia na CPU i GPU. Ścieżki kodu są zoptymalizowane pod kątem
rysowania zniekształconych podpodziałów ze statyczną topologią z
interaktywną częstotliwością. Wynikowe powierzchnie ograniczające są
zgodne z oprogramowaniem Pixar Renderman z dokładnością do precyzji
numerycznej.

%package devel
Summary:	Header files for OpenSubdiv libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek OpenSubdiv
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:5

%description devel
Header files for OpenSubdiv libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek OpenSubdiv.

%package static
Summary:	Static OpenSubdiv libraries
Summary(pl.UTF-8):	Statyczne biblioteki OpenSubdiv
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenSubdiv libraries.

%description static -l pl.UTF-8
Statyczne biblioteki OpenSubdiv.

%package apidocs
Summary:	API documentation for OpenSubdiv libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek OpenSubdiv
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for OpenSubdiv libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek OpenSubdiv.

%prep
%setup -q -n %{name}-%{tagver}
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_apidocs:-DNO_DOC=ON} \
	-DNO_EXAMPLES=ON \
	-DNO_GLEW=OFF \
	-DNO_REGRESSION=ON \
	-DNO_TUTORIALS=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt NOTICE.txt README.md
%attr(755,root,root) %{_libdir}/libosdCPU.so.%{version}
%attr(755,root,root) %{_libdir}/libosdGPU.so.%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libosdCPU.so
%attr(755,root,root) %{_libdir}/libosdGPU.so
%{_includedir}/opensubdiv
%{_libdir}/cmake/OpenSubdiv

%files static
%defattr(644,root,root,755)
%{_libdir}/libosdCPU.a
%{_libdir}/libosdGPU.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/opensubdiv
%endif
