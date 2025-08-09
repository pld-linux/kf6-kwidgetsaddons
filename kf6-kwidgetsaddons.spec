#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.17
%define		qtver		5.15.2
%define		kfname		kwidgetsaddons

Summary:	Large set of desktop widgets
Name:		kf6-%{kfname}
Version:	6.17.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	238a7cb973629f9d6207fbd80e3a2a43
Patch0:		failed-tests.patch
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6UiTools-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
This repository contains add-on widgets and classes for applications
that use the Qt Widgets module. If you are porting applications from
KDE Platform 4 "kdeui" library, you will find many of its classes
here.

Provided are action classes that can be added to toolbars or menus, a
wide range of widgets for selecting characters, fonts, colors,
actions, dates and times, or MIME types, as well as platform-aware
dialogs for configuration pages, message boxes, and password requests.

Further widgets and classes can be found in other KDE frameworks. For
a full list, please see
<https://projects.kde.org/projects/frameworks/>


%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_PYTHON_BINDINGS=OFF \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6WidgetsAddons.so.6
%attr(755,root,root) %{_libdir}/libKF6WidgetsAddons.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/kwidgetsaddons6widgets.so
%{_datadir}/qlogging-categories6/kwidgetsaddons.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KWidgetsAddons
%{_libdir}/cmake/KF6WidgetsAddons
%{_libdir}/libKF6WidgetsAddons.so
