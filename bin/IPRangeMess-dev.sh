#!/usr/bin/env bash

VENV_DIR="${HOME}/.virtualenvs/IPRangeMess"
WEB_DIR="${HOME}/code/IPRangeMess/web"

source `which virtualenvwrapper.sh` 2> /dev/null
if [ "$?" != 0 ]; then
        cd ${VENV_DIR}
        source bin/activate
else
        workon IPRangeMess
fi

cd ${WEB_DIR}
${VENV_DIR}/bin/uwsgi --enable-threads -s /tmp/uwsgi.sock -w application:app -H ${VENV_DIR} --chmod-socket=666 --py-autoreload 1 --touch-reload ${WEB_DIR}/templates/base.html
