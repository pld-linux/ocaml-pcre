#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	PCRE binding for OCaml
Summary(pl.UTF-8):	Wiązania PCRE dla OCamla
Name:		ocaml-pcre
Version:	7.5.0
Release:	1
License:	LGPL v2.1+ with OCaml linking exception
Group:		Libraries
#Source0Download: https://github.com/mmottl/pcre-ocaml/releases
Source0:	https://github.com/mmottl/pcre-ocaml/releases/download/%{version}/pcre-%{version}.tbz
# Source0-md5:	3f91ab553a59b661e5e7debbb876918c
URL:		http://mmottl.github.io/pcre-ocaml/
BuildRequires:	ocaml >= 1:4.12
BuildRequires:	ocaml-dune >= 2.7
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
%setup -q -n pcre-%{version}

%build
dune build --display=verbose

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

dune install --destdir=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/*.mli

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/pcre

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md
%dir %{_libdir}/ocaml/pcre
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllpcre_stubs.so
%{_libdir}/ocaml/pcre/META
%{_libdir}/ocaml/pcre/pcre.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/pcre/pcre.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/pcre/dune-package
%{_libdir}/ocaml/pcre/opam
%{_libdir}/ocaml/pcre/libpcre_stubs.a
%{_libdir}/ocaml/pcre/pcre.cmi
%{_libdir}/ocaml/pcre/pcre.cmt
%{_libdir}/ocaml/pcre/pcre.cmti
%if %{with ocaml_opt}
%{_libdir}/ocaml/pcre/pcre.a
%{_libdir}/ocaml/pcre/pcre.cmx
%{_libdir}/ocaml/pcre/pcre.cmxa
%endif
%{_examplesdir}/%{name}-%{version}
