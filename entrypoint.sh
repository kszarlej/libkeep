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

  ${PIP_BIN} install -r ${APP_DIR}/requirements.txt --upgrade "${@:1}"
}

function run {
  ${PYTHON_BIN} ${APP_DIR}/run.py "${@:1}"
}

function test_ {
  ${VIRT_DIR}/bin/py.test "${@:1}"
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


case "$1" in

'install')
  install "${@:2}"
  ;;
'test')
  test_ "${@:2}"
  ;;
'run')
  run "${@:2}"
  ;;
'pip')
  pip "$2" "$3"
  ;;
*)
  "${@:1}"
  ;;
esac
