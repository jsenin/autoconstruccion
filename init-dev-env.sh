#!/bin/bash

app='autoconstruccion'

python="python"
major=$($python  -c 'import sys; print(sys.version_info[0])')

if [ $major -eq 2 ]
then
    python='python3'
    major=$($python  -c 'import sys; print(sys.version_info[0])')
    if [ $major -ge 3 ]
    then echo
    else
        echo "Python 3 it's mandatory"
        exit
    fi
fi

minor=$($python -c 'import sys; print(sys.version_info[1])')
if [ $minor -lt 4 ]
    then
        echo "Minimun Python version supported it's 3.4"
        exit
fi

echo "Using Python:" $python_version
echo $($python -V)

# create virtual environment
mkdir venv
$python -m venv ./venv

if [[ $? != 0 ]]; then
	echo "module venv fails, maybe this is beacause debiand and ubuntu has a pip issue "
	echo "http://askubuntu.com/questions/488529/pyvenv-3-4-error-returned-non-zero-exit-status-1"
	echo "trying to install with a workaround"
	$python -m venv --without-pip ./venv
	source venvdir/bin/activate
	curl https://bootstrap.pypa.io/get-pip.py | python
	deactivate

fi ;

source ./venv/bin/activate

pip="$python -m pip"
if $( cat $pip | grep-i 'No module' ); then
	echo "necesitas instalar pip"
fi ;
 
echo $($pip -V)

$pip install -r requirements-dev.txt
$pip install -r requirements.txt

#mkdir ./$app

# make development config file
mkdir ./$app/instance
touch ./$app/instance/config.py


