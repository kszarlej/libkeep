#!/bin/bash

VIRT_DIR=${APP_DIR}/.virtualenv

if [ "$DEBUG" = 1 ]
then
  PYTHON_BIN=${VIRT_DIR}/bin/python3
  PIP_BIN=${VIRT_DIR}/bin/pip3
else
  PYTHON_BIN=python3
  PIP_BIN=pip3
fi


function install {
  if [ "$DEBUG" = "1" ]
  then
    pip3 install virtualenv && \
      virtualenv $VIRT_DIR
  fi

  ${PIP_BIN} install -r ${APP_DIR}/requirements.txt --upgrade $@
}

function run {
  ${PYTHON_BIN} ${APP_DIR}/run.py $@
}

function install_and_run {
  install
  run
}

function test_once {
  ${VIRT_DIR}/bin/py.test $@
}

function test_watch {
  source ${VIRT_DIR}/bin/activate
  ptw $@
}

function pip {
  ${PIP_BIN} install "$1"

  REQUIREMENTS_FILE=''
  if [ "$2" == "--save" ]
  then
    local REQUIREMENTS_FILE=requirements.txt
  elif [ "$2" == "--save-dev" ]
  then
    local REQUIREMENTS_FILE=requirements.dev.txt
  fi

  local INSTALLED=`${PIP_BIN} freeze | grep "$1"`
  if [ -n "$REQUIREMENTS_FILE" ] && ! grep -q "$INSTALLED" "$REQUIREMENTS_FILE"
  then
    echo $INSTALLED >> ${APP_DIR}/${REQUIREMENTS_FILE}
    echo "requirements saved in ${REQUIREMENTS_FILE} file"
  fi
}


$@
