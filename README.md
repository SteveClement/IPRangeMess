# IPRange_Mess
The Mess, the IP Protocol

## Install dev env
This assumes you are near the root of this repository.

```
cd ~
mkdir code ; cd code
git clone https://github.com/SteveClement/IPRangeMess.git
cd IPRangeMess/web
```

### OSX
```
pip install virtualenv
mkdir ~/.virtualenvs
virtualenv ~/.virtualenvs/IPRangeMess
source ~/.virtualenvs/IPRangeMess/bin/activate
pip install Flask flask-mysqldb uwsgi
brew install --with-gunzip --with-http2 --with-libressl nginx
brew install mysql
```

### Ubuntu/Debian Linux
```
sudo apt install nginx python3-pip libmysqlclient-dev mysql-server
pip3 install virtualenv
mkdir ~/.virtualenvs
virtualenv ~/.virtualenvs/IPRangeMess
source ~/.virtualenvs/IPRangeMess/bin/activate
pip3 install Flask flask-mysqldb uwsgi
```

## nginx

### OSX
Default Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  nginx

#### /usr/local/etc/nginx/nginx.conf
```
        set $homeWebDir /Users/steve/code/IPRangeMess/web
        set $virtualEnvDir /Users/steve/.virtualenvs/IPRangeMess

        location /static {
                alias $homeWebDir/static;
                    }

        location / {
            root   html;
            index  index.html index.htm;
            include uwsgi_params;
            uwsgi_pass unix:/tmp/uwsgi.sock;
            uwsgi_param UWSGI_PYHOME $virtualEnvDir;
            uwsgi_param UWSGI_CHDIR $homeWebDir;
            uwsgi_param UWSGI_MODULE application;
            uwsgi_param UWSGI_CALLABLE app;
        }
```

## run

```
~/code/IPRangeMess/bin/IPRangeMess-dev.sh
```

## Notes
services(snmp, ssh, mysql, PRIMARY KEY id)


### IP Addresses in MySQL
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

