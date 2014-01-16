#
# spec file for package polkit-qt-1
# Based on:
# https://build.opensuse.org/package/view_file/devel:ARM:AArch64:12.3/polkit-qt-1/polkit-qt-1.spec
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define debug_package_requires libpolkit-qt-1-0 = %{version}-%{release}

Name:           polkit-qt-1
Version:        0.99.1
Release:        14
License:        LGPL-2.1+
Summary:        PolicyKit Library Qt Bindings
Url:            https://github.com/hawaii-desktop/polkit-qt-1
Group:          Development/Libraries/KDE
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  cmake
BuildRequires:  calligra-extra-cmake-modules
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(polkit-backend-1)
BuildRequires:  pkgconfig(polkit-agent-1)

%description
Polkit-qt-1 aims to make it easy for Qt developers to take advantage of
PolicyKit API. It is a convenience wrapper around QAction and
QAbstractButton that lets you integrate those two components easily
with PolicyKit.

%package -n libpolkit-qt-1-1
License:        LGPL-2.1+
Summary:        PolicyKit Library Qt Bindings
Group:          Development/Libraries/KDE
Provides:       libpolkit-qt0 = 0.9.3
Obsoletes:      libpolkit-qt0 < 0.9.3

%description -n libpolkit-qt-1-1
Polkit-qt aims to make it easy for Qt developers to take advantage of
PolicyKit API. It is a convenience wrapper around QAction and
QAbstractButton that lets you integrate those two components easily
with PolicyKit.

%package -n libpolkit-qt-1-devel
License:        LGPL-2.1+
Summary:        PolicyKit Library Qt Bindings
Group:          Development/Libraries/KDE
Requires:       libpolkit-qt-1-1 = %{version}
Requires:       polkit-devel
Provides:       libpolkit-qt-devel = 0.9.3
Obsoletes:      libpolkit-qt-devel < 0.9.3

%description -n libpolkit-qt-1-devel
Polkit-qt aims to make it easy for Qt developers to take advantage of
PolicyKit API. It is a convenience wrapper around QAction and
QAbstractButton that lets you integrate those two components easily
with PolicyKit.

%prep
%setup -q

%build
%cmake .
make

%install
%make_install

%post -n libpolkit-qt-1-1 -p /sbin/ldconfig

%postun -n libpolkit-qt-1-1 -p /sbin/ldconfig

%files -n libpolkit-qt-1-devel
%defattr(-,root,root)
%doc AUTHORS README
%{_includedir}/polkit-qt-1/
%{_libdir}/pkgconfig/polkit-qt*
%{_libdir}/libpolkit-qt-gui-1.so
%{_libdir}/libpolkit-qt-core-1.so
%{_libdir}/libpolkit-qt-agent-1.so
%{_libdir}/cmake/PolkitQt-1/

%files -n libpolkit-qt-1-1
%defattr(-,root,root)
%{_libdir}/libpolkit-qt-gui-1.so.*
%{_libdir}/libpolkit-qt-core-1.so.*
%{_libdir}/libpolkit-qt-agent-1.so.*
