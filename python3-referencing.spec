#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	referencing
Summary:	JSON Referencing + Python
Summary(pl.UTF-8):	Odnośniki JSON + Pyton
Name:		python3-%{module}
Version:	0.36.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/referencing/
Source0:	https://files.pythonhosted.org/packages/source/r/referencing/%{module}-%{version}.tar.gz
# Source0-md5:	9d116186b2c5225c4e55254b94b2cd8e
URL:		https://pypi.org/project/referencing/
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-build
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-attrs >= 22.2.0
BuildRequires:	python3-jsonschema
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-subtests
BuildRequires:	python3-rpds-py >= 0.7.0
%if "%{py3_ver}" != "3.13"
BuildRequires:	python3-typing_extensions >= 4.4.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_json_schema_spec
BuildRequires:	python3-url-py
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An implementation-agnostic implementation of JSON reference
resolution.

%description -l pl.UTF-8
Niezależne od implementacji rozwiązywanie odwolań do specyfikacji
JSON.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests} || %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-ext
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-ext" suite
%endif

%if %{with doc}
%{__make} -C docs html \
	PYTHONPATH=$PWD/build-3-ext \
	SPHINXBUILD=sphinx-build-3 \
	SPHINXOPTS="-Dcache_path=%{py3_sitescriptdir}/sphinx_json_schema_spec/_cache"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/referencing/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/*.pyi
%{py3_sitescriptdir}/%{module}/py.typed
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
