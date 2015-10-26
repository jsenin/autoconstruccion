from flask import Flask
from flask import render_template, request , session




app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'mifootieneunbar'
app.config['WTF_CSRF_ENABLED'] = False



@app.route('/')
def hello_world():
    name = __name__
    return render_template('index.html', name=name)


def add( data ):
    projects = session.get('projects', [])
    projects.append( {'name': data['name'], 'description': data['description'] } )
    session['projects'] = projects

def find_all ():

    if session:       
        return session.get('projects', None)



@app.route('/project/', methods=['POST', 'GET'])
def project():
    error = None

    if request.method == 'POST':
        add(request.form)

    projects = find_all()
    return render_template('index.html', error=error, projects=projects )


if __name__ == '__main__':
    app.run()





