#!/bin/sh

trap "kill 0" SIGINT
node ./bodypix/app.js &

python ./virtual_background.py
