%global kf5_version 5.105.0

Name: opt-kf5-kwallet
Version: 5.105.0
Release: 1%{?dist}
Summary: KDE Frameworks 5 Tier 3 solution for password management

License: LGPLv2+
URL:     https://invent.kde.org/frameworks/kwallet
Source0: %{name}-%{version}.tar.bz2

Patch1: 0001-Disable-X11.patch

%global __requires_exclude ^libqca-qt5.*$|^libkwalletbackend5.*$
%{?opt_kf5_default_filter}

BuildRequires:  opt-qca-qt5-devel

BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
#BuildRequires: qgpgme-devel
BuildRequires: libgcrypt-devel
BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel

BuildRequires: opt-kf5-kconfig-devel >= %{kf5_version}
BuildRequires: opt-kf5-kconfigwidgets-devel >= %{kf5_version}
BuildRequires: opt-kf5-kcoreaddons-devel >= %{kf5_version}
BuildRequires: opt-kf5-kdbusaddons-devel >= %{kf5_version}
#BuildRequires: opt-kf5-kdoctools-devel >= %{kf5_version}
BuildRequires: opt-kf5-ki18n-devel >= %{kf5_version}
BuildRequires: opt-kf5-kiconthemes-devel >= %{kf5_version}
BuildRequires: opt-kf5-knotifications-devel >= %{kf5_version}
BuildRequires: opt-kf5-kservice-devel >= %{kf5_version}
BuildRequires: opt-kf5-kwidgetsaddons-devel >= %{kf5_version}
BuildRequires: opt-kf5-kwindowsystem-devel >= %{kf5_version}
BuildRequires: opt-kf5-rpm-macros

# optional gpgme suppot
#BuildRequires:  cmake(Gpgmepp)

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires: opt-kf5-kconfigwidgets >= %{kf5_version}
Requires: opt-kf5-kcoreaddons >= %{kf5_version}
Requires: opt-kf5-kdbusaddons >= %{kf5_version}
Requires: opt-kf5-kservice >= %{kf5_version}
Requires: opt-kf5-kwidgetsaddons >= %{kf5_version}
Requires: opt-qt5-qtbase-gui
# gpg support ui
#Requires:       pinentry-gui

%description
KWallet is a secure and unified container for user passwords.

%package        libs
Summary:        KWallet framework libraries
%{?opt_kf5_default_filter}
Requires:       %{name} = %{version}-%{release}
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
Requires: opt-kf5-kconfig >= %{kf5_version}
Requires: opt-kf5-ki18n >= %{kf5_version}
Requires: opt-kf5-knotifications >= %{kf5_version}
Requires: opt-kf5-kwindowsystem >= %{kf5_version}
%description    libs
Provides API to access KWallet data from applications.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../

%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%find_lang %{name} --all-name --with-man


%check
export CTEST_OUTPUT_ON_FAILURE=1
make test ARGS="--output-on-failure --timeout 30" -C %{_target_platform} ||:


%files
%doc README.md
%license LICENSES/*.txt
%{_opt_kf5_datadir}/qlogging-categories5/kwallet*
%{_opt_kf5_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_opt_kf5_bindir}/kwalletd5
%{_opt_kf5_datadir}/kservices5/kwalletd5.desktop
%{_opt_kf5_datadir}/applications/org.kde.kwalletd5.desktop
%{_opt_kf5_datadir}/knotifications5/kwalletd5.notifyrc
%{_opt_kf5_bindir}/kwallet-query
#{_mandir}/man1/kwallet-query.1*
%{_opt_kf5_datadir}/locale/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_opt_kf5_libdir}/libKF5Wallet.so.*
%{_opt_kf5_libdir}/libkwalletbackend5.so.*

%files devel
%{_opt_kf5_datadir}/dbus-1/interfaces/kf5_org.kde.KWallet.xml

%{_opt_kf5_includedir}/KF5/KWallet/
%{_opt_kf5_libdir}/cmake/KF5Wallet/
%{_opt_kf5_libdir}/libKF5Wallet.so
%{_opt_kf5_libdir}/libkwalletbackend5.so
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_KWallet.pri
