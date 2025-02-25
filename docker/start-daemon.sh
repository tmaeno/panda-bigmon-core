#!/bin/sh

BIGMON_SERVICE=$1

ln -fs /data/bigmon/config/*-httpd.conf /etc/httpd/conf.d/

if [ -f /etc/grid-security/hostkey.pem ]; then
    echo "host certificate is already created."
elif [ -f /opt/bigmon/etc/cert/hostkey.pem ]; then
    echo "mount /opt/bigmon/etc/cert/hostkey.pem to /etc/grid-security/hostkey.pem"
    ln -fs /opt/bigmon/etc/cert/hostkey.pem /etc/grid-security/hostkey.pem
    ln -fs /opt/bigmon/etc/cert/hostcert.pem /etc/grid-security/hostcert.pem
else
    echo "Host certificate not found. will generate a self-signed one."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -subj "/C=US/DC=IDDS/OU=computers/CN=$(hostname -f)" \
        -keyout /data/bigmon/config/hostkey.pem \
        -out /data/bigmon/config/hostcert.pem
    ln -fs /data/bigmon/config/hostcert.pem /etc/grid-security/hostcert.pem
    ln -fs /data/bigmon/config/hostkey.pem /etc/grid-security/hostkey.pem
fi

# setup intermediate certificate
if [ ! -f /etc/grid-security/chain.pem ]; then
  if [ -f /opt/bigmon/etc/cert/chain.pem ]; then
    ln -fs /opt/bigmon/etc/cert/chain.pem /etc/grid-security/chain.pem
  elif [ -f /etc/grid-security/hostcert.pem ]; then
    ln -fs /etc/grid-security/hostcert.pem /etc/grid-security/chain.pem
  fi
fi

if [ "${BIGMON_SERVICE}" == "all" ]; then
  echo "starting bigmon http service"
  /usr/sbin/httpd
else
  exec "$@"
fi

trap : TERM INT; sleep infinity & wait
