#!/bin/bash
################################################################################
source ./venv/bin/activate
# FLASK_APP=cartaro-server.py exec flask run -p 4242
exec flask run -p 4242
# echo $$ > server.pid
# cat server.pid
# echo "---==Server Started==---"
