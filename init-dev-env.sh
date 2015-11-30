#!/bin/bash 

APP_DIR='server_app'
PYTHON=$(which python3)
PYTHON_MAYOR_REQUIRED=3
PYTHON_MINOR_REQUIRED=4


function require_python_mayor_minor_version_installed {

    major=$(${PYTHON} -c 'import sys; print(sys.version_info[0])');
    minor=$(${PYTHON} -c 'import sys; print(sys.version_info[1])');

    if ! ( [[ ${PYTHON_MAYOR_REQUIRED} == $major ]] && [[ ${PYTHON_MINOR_REQUIRED} == $minor ]] ); then
        install_error "Python ${PYTHON_MAYOR_REQUIRED}.${PYTHON_MINOR_REQUIRED} is required";
    fi;

}

function install_error {
    echo $1 
    exit 1;
}

function install_venv_and_pip_at_debian_as_workaround {
        echo "module venv fails, maybe this is beacause debiand and ubuntu has a pip issue "
        echo "http://askubuntu.com/questions/488529/pyvenv-3-4-error-returned-non-zero-exit-status-1"
        echo "trying to install with a workaround"
        ${PYTHON} -m venv --without-pip venv
        source venv/bin/activate
        curl https://bootstrap.pypa.io/get-pip.py | python
        deactivate

}
# create virtual environment
function install_venv  {
    ${PYTHON} -m venv ./venv 1&> /dev/null

    if [[ $? != 0 ]]; then
        install_venv_and_pip_at_debian_as_workaround
    fi; 

    if [ ! -e ./venv/bin/activate ]; then
        install_error "venv not installed";
    fi;

}

function require_python_pip {

    PYTHON=$(which python3);

    PIP="${PYTHON} -m pip"
    if $( ${PIP} | grep -i 'No module' ); then
        install_error 'PIP module not present.'
    fi ;

}

function install_requirements {
    echo "### Installing requirements"

    source ./venv/bin/activate

    PIP=$(which pip);
    ${PIP} install -r requirements-dev.txt 
    ${PIP} install -r requirements.txt

    deactivate
}

function install_app {
    echo "### Installing app in development mode"
    source ./venv/bin/activate

    pip install -e ./server_app --upgrade -v

    deactivate
}

function configure_database {
    mkdir -p ./${APP_DIR}/instance 
    touch ./${APP_DIR}/instance/config.py

    source ./venv/bin/activate
    cd server_app
    alembic upgrade head
    cd ..
    # python server_app/create_db.py
}

require_python_mayor_minor_version_installed ${PYTHON_MAYOR_REQUIRED} ${PYTHON_MINOR_REQUIRED}
install_venv
require_python_pip
install_requirements
install_app
configure_database 
