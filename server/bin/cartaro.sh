#!/bin/bash
################################################################################
source ./venv/bin/activate

FLASK_APP=cartaro exec flask $*
