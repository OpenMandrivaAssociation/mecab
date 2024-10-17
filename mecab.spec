%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		mecab
Summary:	Yet Another Part-of-Speech and Morphological Analyzer
Version:	0.994
Release:	2
License:	LGPLv2+
Group:		System/Internationalization
URL:		https://mecab.sourceforge.jp/
Source0:	http://sourceforge.net/projects/mecab/files/%{name}/%{version}/%{name}-%{version}.tar.gz
Conflicts:	%{_lib}mecab1 < 0.99

%description
Yet Another Part-of-Speech and Morphological Analyzer.

%package -n 	%{libname}
Summary:	Mecab shared library
Group:		System/Libraries

%description -n %{libname}
Mecab shared library.

%package -n	%{develname}
Summary:	Headers of %{name} for development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
mecab development package.

%prep
%setup -q
mv doc/doxygen .
find . -name \*.cpp -print0 | xargs -0 chmod 0644
find . -name \*.h -print0 | xargs -0 chmod 0644

# compiler flags fix
sed -i.flags \
	-e '/-O3/s|CFLAGS=\"\(.*\)\"|CFLAGS=\${CFLAGS:-\1}|' \
	-e '/-O3/s|CXXFLAGS=\"\(.*\)\"|CXXFLAGS=\${CFLAGS:-\1}|' \
	-e '/MECAB_LIBS/s|-lstdc++||' \
	configure

# multilib change
sed -i.multilib \
	-e 's|@prefix@/lib/mecab|%{_libdir}/mecab|' \
	mecab-config.in mecabrc.in

%build
%configure2_5x
# remove rpath from libtool
sed -i.rpath \
	-e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
	libtool
%make

%install
%makeinstall_std

%files
%doc AUTHORS COPYING README doc/
%{_bindir}/mecab
%{_mandir}/*/mecab.1*
%config(noreplace) %{_sysconfdir}/mecabrc
%{_libdir}/mecab

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_bindir}/mecab-config
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so

