# Deploy on OpenShift of autoconstruccion Flask app

## Prerequisites

You will need a working rhc command app paired with your OpenShift account, see [1].
Also a bash like console, a text editor and git.

## Create the OpenShift app and prepare repository

- Create the autoconstruccion gear.

```bash
$ rhc app-create autoconstruccion python-3.3 postgresql-9.2
```

- Clone the gear repo to your computer

```bash
$ rhc git-clone autoconstruccion
```

Once cloned the autoconstruccion folder should look like this:

```bash
$ tree -a -L 1
```
```
.
├── .git
├── .openshift
├── requirements.txt
├── setup.py
└── wsgi.py
```

- Remove the default files provided by the python cartridge.

```bash
$ git rm requirements.txt setup.py wsgi.py
$ git commit -am "Remove default files"
```

- Add the autoconstruccion repo as a submodule.

```bash
$ git submodule add https://github.com/autoconstruccion/autoconstruccion.git autoconstruccion
$ git commit -am "Add autoconstruccion repo as a submodule"
```

## Create the configuration for the app

- Create a config file for the autoconstruccion app

```bash
$ touch config.py
```

- Edit the file to include the desired configuration. In this case we propagate exceptions to be logged on the OpenShift
log and set the SQLALCHEMY_DATABASE_URI to use Postgres configured ion the cartridge.

```python
import os

# propagate exceptions so OpenShift Logs be aware of.
PROPAGATE_EXCEPTIONS=True

SQLALCHEMY_DATABASE_URI="postgresql://{}:{}@{}:{}/autoconstruccion".format(os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME'), os.getenv('OPENSHIFT_POSTGRESQL_DB_PASSWORD'), os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST'), os.getenv('OPENSHIFT_POSTGRESQL_DB_PORT') )
```

- Add to the git repo

```bash
$ git add config.py
$ git commit -m "Add app configuration"
```

- *The database must exists before execute the deploy* in this case it's not necessary as 'autoconstruccion'
is the name of the app and a 'autoconstruccion' db is automatically created.

To create the Postgres database log to the remote app console:
```bash
$ rhc ssh autoconstruccion
```
On remote console run ```psql``` and execute this command:
```sql
=# CREATE DATABASE autoconstruccion;
```
Use ```\q``` command to exit psql.


## Create the deployment scripts

OpenShift deploys works with action hooks files that are stored in the ```.openshift/action_hooks``` folder.

The available build hooks are: pre_build, build, deploy, & post_deploy. For OpenShift to execute this files must be
in the correct folder and must be executables.

```bash
$ touch .openshift/action_hooks/pre_build .openshift/action_hooks/build .openshift/action_hooks/deploy
$ chmod +x .openshift/action_hooks/pre_build .openshift/action_hooks/build .openshift/action_hooks/deploy
```

### Set environment variables in pre_built script

Most of the configuration on OpenShift it's done by environment variables. We need to tell to the python cartridge
where our requirements.txt and wsgi file are. This is done by setting the OPENSHIFT_PYTHON_REQUIREMENTS_PATH and
OPENSHIFT_PYTHON_WSGI_APPLICATION.

Setting environment variables on OpenShift is a little tricky and it's not well documented. You can set with the
```rhc env``` command but you have to take care with character scape and var interpretation by your local console.
Also if you finally set the correct value to the env. variable if this depends on another env. var. is not evaluated correctly.

If you set the env. vars in a build script with ```export``` or ```declare -x``` bash commands the vars are not passed
to other scripts environment.

The best way we've come so far is to create the env. vars as files from build script. OpenShift store the default
values of environment variables in files which name is the env. var name and the content of the file is the value.
The files are stored in ```.env/user_vars``` folder in OpenShift app home directory.

For example, or pre_build file set the env. vars and looks like this:

```bash
#!/bin/bash
echo "** pre_build: Creating env variables"
cd ${OPENSHIFT_HOMEDIR}/.env/user_vars
echo "${OPENSHIFT_REPO_DIR}autoconstruccion/requirements.txt" > OPENSHIFT_PYTHON_REQUIREMENTS_PATH
echo "${OPENSHIFT_REPO_DIR}autoconstruccion/server_app/autoconstruccion.wsgi" > OPENSHIFT_PYTHON_WSGI_APPLICATION
echo "${OPENSHIFT_REPO_DIR}config.py" > AUTOCONSTRUCCION_APP_CONFIG_FILE
```

When the env vars are setting that way the files are created with read-write permissions to root, but if the env var are
created with ```rhc env``` the files are created only with read permission.

### Build virtualenv and app.

The virtualenv creation and requirements install are manage by the python cartridge if the OPENSHIFT_PYTHON_REQUIREMENTS_PATH
is correctly define. So we only need to install the autoconstruccion app in editable mode for the package load well
the templates and other non python files. '--no-cache-dir' option it's used with pip because by default uses a path for .cache folder that don't hace write rights.

Our build script is looks like:

```bash
#!/bin/bash
echo "** build: Activating virtualenv"
source $VIRTUAL_ENV/bin/activate
#echo "** build: Installing app requirements"
#pip install -r ${OPENSHIFT_REPO_DIR}/autoconstruccion/requirements.txt --no-cache-dir
echo "** build: Installing Autoconstruccion app"
pip install -e ${OPENSHIFT_REPO_DIR}/autoconstruccion/server_app --upgrade --no-cache-dir
```

### Deploy app and do database migrations.

The OpenShift server find the wsgi application with the OPENSHIFT_PYTHON_WSGI_APPLICATION en var that we previously set.
The last part to our deployment is to upgrade the database to the current point in the migration scripts,
this is done by the ```alembic``` command.

```bash
#!/bin/bash
echo "** deploy: Starting db migration, upgrading.."
source $VIRTUAL_ENV/bin/activate
cd ${OPENSHIFT_REPO_DIR}/autoconstruccion/server_app
alembic upgrade head
```

### Edit the build scripts and commit files.

After editing the build files to include the content above we update the repo.

```bash
$ git add .openshift/action_hooks/build .openshift/action_hooks/deploy .openshift/action_hooks/pre_build
$ git commit -m "Add build scripts"
```

### Add markers to our deployment

OpenShift allows markers to set different deployment options, see [2] (17.3). We choose to force_clean_build and pip_install.
To do this simply create files thar are named like the markers in ```.openshift/markers``` folder and add to the repo.

```bash
$ touch .openshift/markers/pip_install
$ touch .openshift/markers/force_clean_build
$ git add .openshift/markers/pip_install .openshift/markers/force_clean_build
$ git commit -m "Add deployment markers"
```

## Deploy our app.

The last step it's to push the repository to OpenShift to start the deploy:

```bash
 $ git push origin master
```

If all goes well we should obtain this message:
```
remote: Deployment completed with status: success
```

And that's it.

## References

[1] https://developers.openshift.com/en/getting-started-debian-ubuntu.html

[2] https://docs.openshift.org/origin-m4/oo_cartridge_guide.html#python

[3] https://developers.openshift.com/en/managing-environment-variables.html

[4] https://developers.openshift.com/en/managing-action-hooks.html


