Summary:	PCRE binding for OCaml
Summary(pl):	Wi±zania PCRE dla OCamla
Name:		ocaml-pcre
Version:	4.26.3
Release:	1
License:	LGPL
Group:		Libraries
Vendor:		Markus Mottl <markus@oefai.at>
URL:		http://www.ai.univie.ac.at/~markus/ocaml_sources/
Source0:	http://www.ai.univie.ac.at/~markus/ocaml_sources/pcre-ocaml-%{version}.tar.bz2
BuildRequires:	pcre-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This OCaml-library interfaces the PCRE (Perl-compatibility regular
expressions) library which is written in C. It can be used for
matching regular expressions which are written in "Perl"-style.

This package contains files needed to run bytecode executables using
this library.

%description -l pl
Biblioteka zawarta w tym pakiecie umo¿liwia korzystanie z biblioteki
PCRE (wyra¿enia regularne kompatybilne z Perlem), która jest z kolei
napisana w C. Mo¿e byæ ona u¿ywana do dopasowywania wyra¿eñ
regularnych napisanym w ,,stylu Perla''.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
u¿ywaj±cych tej biblioteki.

%package devel
Summary:	PCRE binding for OCaml - development part
Summary(pl):	Wi±zania PCRE dla OCamla - cze¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This OCaml-library interfaces the PCRE (Perl-compatibility regular
expressions) library which is written in C. It can be used for
matching regular expressions which are written in "Perl"-style.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
Biblioteka zawarta w tym pakiecie umo¿liwia korzystanie z biblioteki
PCRE (wyra¿enia regularne kompatybilne z Perlem), która jest z kolei
napisana w C. Mo¿e byæ ona u¿ywana do dopasowywania wyra¿eñ
regularnych napisanym w ,,stylu Perla''.

Pakiet ten zawiera pliki niezbêdne do tworzenia programów u¿ywaj±cych
tej biblioteki.

%prep
%setup -q -n pcre-ocaml-%{version}

%build

%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags} -fPIC -DPIC" all opt

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install OCAML_LIB_INSTALL=$RPM_BUILD_ROOT%{_libdir}/ocaml/pcre
install lib/pcre.cmx $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre
rm -f $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/*.mli
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s pcre/dll*.so .)

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# Makefiles there ain't usable
rm -f $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*/Makefile

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre
(grep -v 'linkopts = ' META
 echo 'linkopts = ""'
 echo 'directory = "+pcre"'
 ) > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre/META

gzip -9nf lib/*.mli README Changes

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/pcre
%attr(755,root,root) %{_libdir}/ocaml/pcre/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc *.gz lib/*.gz
%{_libdir}/ocaml/pcre/*.cm[ixa]*
%{_libdir}/ocaml/pcre/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/pcre
