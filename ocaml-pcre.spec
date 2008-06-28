%define		ocaml_ver	1:3.09.2
Summary:	PCRE binding for OCaml
Summary(pl.UTF-8):	Wiązania PCRE dla OCamla
Name:		ocaml-pcre
Version:	5.12.2
Release:	4
License:	LGPL
Group:		Libraries
Source0:	http://www.ocaml.info/ocaml_sources/pcre-ocaml-%{version}.tar.bz2
# Source0-md5:	dbe759392f1c1d22cb96b9136ebf4ec4
URL:		http://www.ocaml.info/home/ocaml_sources.html#toc13
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-findlib
BuildRequires:	pcre-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%{__make} all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -DPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib/pcre,stublibs}

%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

install lib/pcre.cmx $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/*.mli

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# Makefiles there ain't usable
rm -f $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*/Makefile

mv $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre/
echo 'directory = "+pcre"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre/META

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README Changes
%dir %{_libdir}/ocaml/pcre
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc lib/*.mli
%{_libdir}/ocaml/pcre/*.cm[ixa]*
%{_libdir}/ocaml/pcre/*.a
%{_libdir}/ocaml/site-lib/pcre
%{_examplesdir}/%{name}-%{version}
