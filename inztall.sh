#!/bin/bash

BIN_PATH="/usr/local/bin"

if [[ ! $1 ]]
then
  echo "No file to inztall."
  echo
  echo "Usage: inztall <path> <name>"
  echo
  echo "inztalls path to $BIN_PATH"
  echo "name is optional"
  echo "inztall can inztall itself"
  exit
fi

if [[ $(basename $0) == $(basename $1) ]]
    then
    UNINSTALL_PATH=$BIN_PATH/un${1%.*}
fi

NAME=${1%.*}
[[ $2 ]] && NAME=${2%.*}
INSTALL_PATH=$BIN_PATH/$NAME
TOOL=$(pwd)/$1


if [[ $(basename $0) == "uninztall" ]]
    then
    rm $INSTALL_PATH && echo "Uninstalled $INSTALL_PATH"
    [[ $UNINSTALL_PATH ]] && rm $UNINSTALL_PATH && echo "Uninstalled $UNINSTALL_PATH"
    exit $?
fi

[[ ! -L $INSTALL_PATH ]] && chmod a+x $TOOL && ln -s "$TOOL" "$INSTALL_PATH" && echo "Installed $TOOL to $INSTALL_PATH" || echo "$INSTALL_PATH already installed"
if [[ $UNINSTALL_PATH ]]
    then
    [[ ! -L $UNINSTALL_PATH ]] && ln -s "$TOOL" "$UNINSTALL_PATH" && echo "Installed $TOOL to $UNINSTALL_PATH" || echo "$UNINSTALL_PATH already installed"
fi