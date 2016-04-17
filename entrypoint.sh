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

  ${PIP_BIN} install -r ${APP_DIR}/requirements.txt --upgrade "${@:2}"
}

function run {
  ${PYTHON_BIN} ${APP_DIR}/run.py "${@:2}"
}

function test_ {
  echo "testing"
}


case "$1" in

'install')
  install
  ;;
'test')
  test_
  ;;
'print')
  echo $DEBUG
  ;;
'run')
  run
  ;;
*)
  "${@:1}"
  ;;
esac
