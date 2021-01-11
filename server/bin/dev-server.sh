#!/bin/bash
################################################################################
source ./venv/bin/activate

CARTARO_DOC_PATH=$HOME/Documents/Cartaro FLASK_APP=cartaro exec flask run -p 7777
