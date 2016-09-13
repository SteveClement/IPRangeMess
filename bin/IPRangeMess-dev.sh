#!/usr/bin/env bash

VENV_DIR="${HOME}/code/IPRangeMess/app/venv"
ROOT_DIR="${HOME}/code/IPRangeMess"

source `which virtualenvwrapper.sh` 2> /dev/null
if [ "$?" != 0 ]; then
  cd ${VENV_DIR}
  source bin/activate
else
  workon IPRangeMess
fi

cd ${ROOT_DIR}
${VENV_DIR}/bin/uwsgi uwsgi_application.ini
