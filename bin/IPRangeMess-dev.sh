#!/bin/sh

source `which virtualenvwrapper.sh` 2> /dev/null
if [ "$?" != 0 ]; then
        cd /Users/steve/.virtualenvs/IPRangeMess
        source bin/activate
else
        workon IPRangeMess
fi

cd /Users/steve/Desktop/code/IPRangeMess/web
#/Users/steve/.virtualenvs/IPRangeMess/bin/uwsgi -s /tmp/uwsgi.sock -w application:app -H /Users/steve/.virtualenvs/IPRangeMess/ --chmod-socket=666 --touch-reload /Users/steve/Desktop/code/IPRangeMess/web/application.py
/Users/steve/.virtualenvs/IPRangeMess/bin/uwsgi -s /tmp/uwsgi.sock -w application:app -H /Users/steve/.virtualenvs/IPRangeMess/ --chmod-socket=666 --py-autoreload 1
