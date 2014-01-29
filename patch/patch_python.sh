#!/bin/bash

ARGPARSE=/usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Versions/2.7/lib/python2.7/argparse.py

/bin/cp $ARGPARSE $ARGPARSE.bak
/usr/bin/patch $ARGPARSE < issue9351.patch
