#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9 
%undefine	with_ocaml_opt
%endif

Summary:	PCRE binding for OCaml
Summary(pl.UTF-8):	Wiązania PCRE dla OCamla
Name:		ocaml-pcre
Version:	7.1.5
Release:	3
License:	LGPL v2.1+ with OCaml linking exception
Group:		Libraries
Source0:	https://github.com/mmottl/pcre-ocaml/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	28e40ad63fe2d568aa47ff460d3f9d3a
URL:		http://mmottl.github.io/pcre-ocaml/
BuildRequires:	ocaml >= 1:3.12
BuildRequires:	ocaml-findlib >= 1.5
BuildRequires:	pcre-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
This OCaml-library interfaces the PCRE (Perl-compatibility regular
expressions) library which is written in C. It can be used for
matching regular expressions which are written in "Perl"-style.

This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
Biblioteka zawarta w tym pakiecie umożliwia korzystanie z biblioteki
PCRE (wyrażenia regularne kompatybilne z Perlem), która jest z kolei
napisana w C. Może być ona używana do dopasowywania wyrażeń
regularnych napisanym w ,,stylu Perla''.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	PCRE binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania PCRE dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This OCaml-library interfaces the PCRE (Perl-compatibility regular
expressions) library which is written in C. It can be used for
matching regular expressions which are written in "Perl"-style.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Biblioteka zawarta w tym pakiecie umożliwia korzystanie z biblioteki
PCRE (wyrażenia regularne kompatybilne z Perlem), która jest z kolei
napisana w C. Może być ona używana do dopasowywania wyrażeń
regularnych napisanym w ,,stylu Perla''.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n pcre-ocaml-%{version}

%build
# not autoconf configure
./configure \
	--prefix=%{_prefix} \
	--docdir=$(pwd)/doc

%{__make} -j1 all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -DPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib/pcre,stublibs}

%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/*.mli

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre
echo 'directory = "+pcre"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre/META

# useless in rpm
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.owner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES.txt README.md
%dir %{_libdir}/ocaml/pcre
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllpcre_stubs.so
%{_libdir}/ocaml/pcre/pcre.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/pcre/pcre.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc lib/*.mli
%{_libdir}/ocaml/pcre/libpcre_stubs.a
%{_libdir}/ocaml/pcre/pcre.annot
%{_libdir}/ocaml/pcre/pcre.cmi
%{_libdir}/ocaml/pcre/pcre.cmt
%{_libdir}/ocaml/pcre/pcre.cmti
%if %{with ocaml_opt}
%{_libdir}/ocaml/pcre/pcre.a
%{_libdir}/ocaml/pcre/pcre.cmx
%{_libdir}/ocaml/pcre/pcre.cmxa
%{_libdir}/ocaml/pcre/pcre_compat.cmx
%endif
%{_libdir}/ocaml/site-lib/pcre
%{_examplesdir}/%{name}-%{version}
