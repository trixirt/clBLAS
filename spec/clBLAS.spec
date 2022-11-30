%global commit0 cf9113982fdfc994297d372785ce76eb80911af2
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%bcond_with check

Summary:        An OpenCL BLAS library
Name:           clBLAS
License:        ASL 2.0
Version:        2.12
Release:        1%{?dist}

URL:            https://github.com/clMathLibraries/clBLAS
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

Group:          Development/Libraries
ExclusiveArch:  x86_64

BuildRequires:  blas-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ocl-icd-devel
%if %{with check}
BuildRequires:  boost-static
%endif

%description
The primary goal of clBLAS is to make it easier for developers
to utilize the inherent performance and power efficiency benefits
of heterogeneous computing. clBLAS interfaces do not hide nor
wrap OpenCL interfaces, but rather leaves OpenCL state management
to the control of the user to allow for maximum performance and
flexibility. The clBLAS library does generate and enqueue
optimized OpenCL kernels, relieving the user from the task of
writing, optimizing and maintaining kernel code themselves.

%package devel
Summary: An OpenCL BLAS library

%description devel
The primary goal of clBLAS is to make it easier for developers
to utilize the inherent performance and power efficiency benefits
of heterogeneous computing. clBLAS interfaces do not hide nor
wrap OpenCL interfaces, but rather leaves OpenCL state management
to the control of the user to allow for maximum performance and
flexibility. The clBLAS library does generate and enqueue
optimized OpenCL kernels, relieving the user from the task of
writing, optimizing and maintaining kernel code themselves.

%prep
%setup -q -n %{name}-%{commit0}

%build
cd src
%cmake -DCMAKE_INSTALL_PREFIX=/usr \
%if %{without check}       
       -DBUILD_TEST=OFF -DBUILD_KTEST=OFF
%endif

%cmake_build

%install
mkdir -p %{buildroot}%{_datadir}/%{name}/doc
cp LICENSE %{buildroot}%{_datadir}/%{name}
cp README.md %{buildroot}%{_datadir}/%{name}
cp -r doc/* %{buildroot}%{_datadir}/%{name}/doc
cd src
%cmake_install

%if %{with check}
%check
export LD_LIBRARY_PATH=$PWD/src/redhat-linux-build/library; ./src/redhat-linux-build/staging/test-medium
%endif

%files
%dir %{_datadir}/%{name}
%license %{_datadir}/%{name}/LICENSE
%doc %{_datadir}/%{name}/README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_bindir}/clBLAS-tune
%doc %{_datadir}/%{name}/doc/
%{_includedir}/cl*.h
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Nov 24 2022 Tom Rix <trix@redhat.com> - 2.12-1
- Initial release
