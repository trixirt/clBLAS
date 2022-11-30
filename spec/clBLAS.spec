# Use CL_DEVICE_TYPE_ALL for all samples.
%global commit0 7ec40a205abdc7ae7d0b771136b578b89f75f0fb
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20170323

%bcond_with check
%bcond_with pocl

Summary:        An OpenCL BLAS library
Name:           clBLAS
License:        Apache-2.0 and Public Domain
Version:        2.12
Release:        2.%{?date0}git%{?shortcommit0}%{?dist}

URL:            https://github.com/clMathLibraries/clBLAS
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
# Silence warnings, specify using OpenCL 1.2
Patch0:         0001-cmake-set-opencl-version-to-1.2.patch
# Fix printf overflow warnings
Patch1:         0002-format-overflow-fixes.patch

Group:          Development/Libraries
ExclusiveArch:  x86_64

BuildRequires:  blas-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ocl-icd-devel
%if %{with check}
BuildRequires:  boost-static
BuildRequires:  gtest
%endif
%if %{with pocl}
BuildRequires:  pocl
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
%autosetup -p1 -n %{name}-%{commit0}

%build
cd src
%cmake \
      -Wno-dev \
%if %{without check}
      -DBUILD_TEST=OFF -DBUILD_KTEST=OFF
%else
      -DBUILD_SAMPLE=ON
%endif

%cmake_build

%install
mkdir -p %{buildroot}%{_datadir}/%{name}/doc
cp -p LICENSE %{buildroot}%{_datadir}/%{name}
cp -p README.md %{buildroot}%{_datadir}/%{name}
cp -rp doc/* %{buildroot}%{_datadir}/%{name}/doc
# remove outdated performance docs
rm -rf %{buildroot}%{_datadir}/%{name}/doc/performance
cd src
%cmake_install

%if %{with check}
%check
export LD_LIBRARY_PATH=$PWD/src/%{__cmake_builddir}/library; $PWD/src/%{__cmake_builddir}/samples/example_sgemm
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
* Sun Dec 04 2022 Tom Rix <trix@redhat.com> - 2.12-2.20170323git7ec40a2
- Fix package review issues

* Thu Nov 24 2022 Tom Rix <trix@redhat.com> - 2.12-1
- Initial release
