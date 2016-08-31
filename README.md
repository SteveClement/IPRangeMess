# IPRange_Mess
The Mess, the IP Protocol

## Install dev env

This assumes you are in the root of this repository.

```
pip install virtualenv
cd web
virtualenv venv
source venv/bin/activate
brew install --with-gunzip --with-http2 --with-libressl nginx
```

### nginx

Default Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  nginx

/usr/local/etc/nginx/nginx.conf
```
        location /static {
                alias /usr/local/IPRangeMess/web/static;
                    }

        location / {
            root   html;
            index  index.html index.htm;
            include uwsgi_params;
            uwsgi_pass unix:/tmp/uwsgi.sock;
            uwsgi_param UWSGI_PYHOME /Users/steve/Desktop/code/IPRangeMess/web/venv;
            uwsgi_param UWSGI_CHDIR /Users/steve/Desktop/code/IPRangeMess/web;
            uwsgi_param UWSGI_MODULE application;
            uwsgi_param UWSGI_CALLABLE app;
        }
```

## run

~/Desktop/code/IPRangeMess/bin/uwsgi -s /tmp/uwsgi.sock -w application:app -H ./venv/ --chmod-socket=666

## Notes

services(snmp, ssh, mysql, PRIMARY KEY id)

Since IPv4 addresses are 4 byte long, you could use an INT (UNSIGNED) that has exactly 4 bytes:

`ipv4` INT UNSIGNED
And INET_ATON and INET_NTOA to convert them:

INSERT INTO `table` (`ipv4`) VALUES (INET_ATON("127.0.0.1"));
SELECT INET_NTOA(`ipv4`) FROM `table`;
For IPv6 addresses you could use a BINARY instead:

`ipv6` BINARY(16)
And use PHP’s inet_pton and inet_ntop for conversion:

'INSERT INTO `table` (`ipv6`) VALUES ("'.mysqli_real_escape_string(inet_pton('2001:4860:a005::68')).'")'
'SELECT `ipv6` FROM `table`'
$ipv6 = inet_pton($row['ipv6']);
