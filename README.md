[![Build Status](https://travis-ci.org/autoconstruccion/autoconstruccion.svg?branch=master)](https://travis-ci.org/autoconstruccion/autoconstruccion)

# Autoconstruccion

Autoconstruccion project at H4ckademy

by Creepy Coconuts

## Requirements:

* Python 3.4
* See requirements.txt & requirements-dev.txt



KWOWN ISSUES

* On Gnu/Debian jessie it's need to do a workarround to install the virtual environment,
because pip it's not included with python3 package.

Further information at
http://askubuntu.com/questions/488529/pyvenv-3-4-error-returned-non-zero-exit-status-1

 	pypthon3 -m venv --without-pip ./venv
	source venvdir/bin/activate
	curl https://bootstrap.pypa.io/get-pip.py | python
	deactivate



HOW TO RUN

First activate your virtual environment or create it init-dev-end.sh and then launch the server

    source ./venv/bin/activate
    python server_app/run.py

By default the server is running at localhost on port 5000
    http://127.0.0.1:5000


