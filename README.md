# IPRange_Mess
The Mess, the IP Protocol

## Important Notes /!\

### Working offline (aka. No Internetz)
When developing with Flask-Bootstrap or Flask-Moment make sure to either cache the the JS files or do an offline installl.
Once the Internet is gone, and you do a hard refresh, it tries to re-download these files from the Web.

### uWSGI et al.

There are a few ways to run, test, debug a Flask project.
By far the easiest is to use the internal WSGI interface and just not bother about it. For performance and cleanliness reasons you might want to use a web browser to relay the WSGI calls.
The solution proposed in this project, works for me. There might be better and more elegant ways to implement such a "server-side" schim. If there is, please let me know.

## Install dev env
This assumes you are near the root of this repository.

```
cd ~
mkdir code ; cd code
git clone https://github.com/SteveClement/IPRangeMess.git
cd IPRangeMess
```

### OSX
```
pip install virtualenv
virtualenv -p python3 app/venv
source ~/code/IPRangeMess/app/venv/bin/activate
brew install mysql
brew install --with-gunzip --with-http2 --with-libressl nginx
pip install -U -r requirements/dev.txt
```

### Ubuntu/Debian Linux
```
sudo apt install nginx python3-pip libmysqlclient-dev mysql-server virtualenv
pip3 install virtualenv
virtualenv -p python3 app/venv
source ~/code/IPRangeMess/app/venv/bin/activate
pip3 install -U -r requirements/dev.txt
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
        set $homeWebDir /Users/steve/code/IPRangeMess/app;
        set $virtualEnvDir /Users/steve/code/IPRangeMess/app/venv;

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
            uwsgi_param UWSGI_CALLABLE application;
            #uwsgi_param UWSGI_MODULE application;
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

