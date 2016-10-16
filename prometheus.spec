#
# spec file for package prometheus
#
%define  debug_package %{nil}

Name:      prometheus
Summary:   Monitoring system and time series database
Version:   %{ver}
Release:   %{rel}%{?dist}
Vendor:    Prometheus Developers <prometheus-developers@googlegroups.com>
Packager:  Julien Pivotto <roidelapluie@inuits.eu>
License:   Apache-2.0
Group:     System/Monitoring
URL:       https://prometheus.io/
Buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
Buildarch: x86_64
Source:    https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz

%description
Prometheus is a systems and service monitoring system. It collects metrics
from configured targets at given intervals, evaluates rule expressions,
displays the results, and can trigger alerts if some condition is observed
to be true.

%prep
%setup -n %{name}-%{version}.linux-amd64

%build

%install
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
mv NOTICE LICENSE %{buildroot}/usr/share/doc/%{name}-%{version}
mkdir -p %{buildroot}/var/lib/%{name}
mkdir -p %{buildroot}/usr/share/%{name}
mv consoles console_libraries %{buildroot}/usr/share/%{name}
mkdir -p %{buildroot}/usr/bin
mv prometheus promtool %{buildroot}/usr/bin
mkdir -p %{buildroot}/etc/prometheus
touch %{buildroot}/etc/prometheus/htpasswd
mv prometheus.yml %{buildroot}/etc/prometheus



%files
%doc /usr/share/doc/%{name}-%{version}
%defattr(755,root,root,755)
/usr/bin/promtool
/usr/bin/prometheus
/usr/share/%{name}
%defattr(640,prometheus,prometheus,755)
/var/lib/%{name}
%dir /etc/prometheus
%config(noreplace) /etc/prometheus/prometheus.yml
%ghost%config(noreplace) /etc/prometheus/htpasswd

%pre
getent group prometheus > /dev/null || \
  groupadd -r prometheus || :
getent passwd prometheus > /dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
     -c "prometheus" prometheus || :


%changelog
* Wed Oct 12 2016 Julien Pivotto <roidelapluie@inuits.eu> - 1.2.1-1
 - Initial spec file
