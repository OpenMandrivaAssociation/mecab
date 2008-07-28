%define version		0.96
%define release		%mkrel 3

%define libname_orig lib%{name}
%define libname %mklibname %{name}1
%define develname %mklibname -d %{name}

Name:		mecab
Summary:	Yet Another Part-of-Speech and Morphological Analyzer
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Internationalization
URL:		http://mecab.sourceforge.jp/
Source0:	http://prdownloads.sourceforge.jp/mecab/18364/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:		%{libname} = %{version}
BuildRequires:		automake1.8

%description
Yet Another Part-of-Speech and Morphological Analyzer.


%package -n 	%{libname}
Summary:	Mecab library
Group:		System/Internationalization
Provides:	%{libname_orig} = %{version}-%{release}
Obsoletes:	libmecab0
Provides:	libmecab0

%description -n %{libname}
mecab library.

%package -n	%{develname}
Summary:	Headers of %{name} for development
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Obsoletes:	libmecab0-devel
Provides:	libmecab0-devel
Obsoletes:	%{libname}-devel

%description -n %{develname}
mecab development package.


%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# multiarch policy
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/mecab-config

# remove multiarch-dispatch to avoid conflict
rm -f %{buildroot}/%{_bindir}/multiarch-dispatch

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files
%defattr(-,root,root)
%doc AUTHORS COPYING README doc/
%multiarch %{multiarch_bindir}/mecab-config
%{_bindir}/mecab-config
%{_bindir}/mecab
%{_mandir}/*/mecab.1*
%config(noreplace) %{_sysconfdir}/mecabrc

%files -n %{libname}
%defattr(-, root, root)
%doc COPYING
%{_libdir}/*.so.1.0.0
%attr(755, root, root) %{_libdir}/mecab
%{_libdir}/mecab/*

%files -n %{develname}
%defattr(-,root,root)
%doc COPYING
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.1


