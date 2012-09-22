Summary:	PCRE binding for OCaml
Summary(pl.UTF-8):	Wiązania PCRE dla OCamla
Name:		ocaml-pcre
Version:	7.0.2
Release:	1
License:	LGPL v2.1+ with OCaml linking exception
Group:		Libraries
# see it to get commit id of particular release
#Source0Download: https://bitbucket.org/mmottl/pcre-ocaml
Source0:	https://bitbucket.org/mmottl/pcre-ocaml/get/00e2295ec90d.tar.bz2
# Source0-md5:	8cdc4f56a7effd98f4e2343d996a7074
URL:		https://bitbucket.org/mmottl/pcre-ocaml
BuildRequires:	ocaml >= 1:3.12
BuildRequires:	ocaml-findlib >= 1.3.1
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
%setup -q -n mmottl-pcre-ocaml-00e2295ec90d

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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/*.mli

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

mv $RPM_BUILD_ROOT%{_libdir}/ocaml/pcre/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre
echo 'directory = "+pcre"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/pcre/META

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES.txt README.md
%dir %{_libdir}/ocaml/pcre
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllpcre_stubs.so
%{_libdir}/ocaml/stublibs/dllpcre_stubs.so.owner

%files devel
%defattr(644,root,root,755)
%doc lib/*.mli
%{_libdir}/ocaml/pcre/libpcre_stubs.a
%{_libdir}/ocaml/pcre/pcre.a
%{_libdir}/ocaml/pcre/pcre.cm[ixa]*
%{_libdir}/ocaml/site-lib/pcre
%{_examplesdir}/%{name}-%{version}
