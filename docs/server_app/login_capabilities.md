# Use of Flask-Login

This app uses FlaskLogin plugin, this file shows little tips on how to use it in view functions and templates.

See docs: https://flask-login.readthedocs.org/en/latest/


## use on templates

use current_user proxy available on any template.

```jinja2
{% if current_user.is_authenticated %}
  Hi {{ current_user.name }}!
{% endif %}
```


## use on views

https://flask-login.readthedocs.org/en/latest/#flask.ext.login.current_user

```python
from flask_login import login_required, current_user

@app.route("/settings")
@login_required
def settings():
    user = current_user
    pass
```
