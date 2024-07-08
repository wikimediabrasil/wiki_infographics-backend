import os
import yaml
import mwoauth
import configparser
from flask import Flask, jsonify, request, json, session, redirect, url_for, flash, render_template
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

__dir__ = os.path.dirname(__file__)
app = Flask(__name__)


# ==================================================================================================================== #
# CONFIGURATION
# ==================================================================================================================== #
app.config.update(yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))


# ----- Database configuration ----- #
HOME = os.environ.get('HOME') or ""
replica_path = HOME + '/replica.my.cnf'
if os.path.exists(replica_path):
    config = configparser.ConfigParser()
    config.read(replica_path)
    user_and_password = f"{config['client']['user']}:{config['client']['password']}"
    host_and_database = f"tools.db.svc.wikimedia.cloud/{app.config['DATABASE_NAME']}"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user_and_password}@{host_and_database}"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(HOME, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ----- Translation configuration ----- #
def get_locale(lang=None):
    """
    This function gets the language preferred by the current user
    :param lang: language code ISO 639
    :return: language code preferred by the current user or the best match for it
    """
    if not lang:
        lang = session.get('language', None)

        return lang if not lang else request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/set_locale')
def set_locale():
    """
    This function sets the interface language to the language preferred by the current user
    :return:
    """
    lang = request.args.get('language', None)
    if not lang:
        lang = request.accept_languages.best_match(app.config["LANGUAGES"])

    session["language"] = lang
    return redirect(url_for('home'))


BABEL = Babel(app)
BABEL.init_app(app, locale_selector=get_locale)


# ==================================================================================================================== #
# AUTHENTICATION
# ==================================================================================================================== #
@app.route('/login')
def login():
    """
    This function sends a request to log in the user through oAuth
    """
    consumer_token = mwoauth.ConsumerToken(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    try:
        redirect_, request_token = mwoauth.initiate(app.config['OAUTH_MWURI'], consumer_token)
    except Exception:
        app.logger.exception('mwoauth.initiate failed')
        return redirect(url_for('home'))
    else:
        session['request_token'] = dict(zip(request_token._fields, request_token))
        return redirect(redirect_)


@app.route('/oauth-callback', methods=["GET"])
def oauth_callback():
    """
    This gets the necessary parameters for the login request of the user
    """
    if 'request_token' not in session:
        flash(u'OAuth callback failed. Are cookies disabled?', 'danger')
        return redirect(url_for('home'))

    consumer_token = mwoauth.ConsumerToken(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])

    try:
        access_token = mwoauth.complete(
            app.config['OAUTH_MWURI'],
            consumer_token,
            mwoauth.RequestToken(**session['request_token']),
            request.query_string)
        identity = mwoauth.identify(app.config['OAUTH_MWURI'], consumer_token, access_token)
    except Exception:
        app.logger.exception('OAuth authentication failed')
    else:
        session['access_token'] = dict(zip(access_token._fields, access_token))
        session['username'] = identity['username']
        flash("You were signed in, %s!" % identity["username"], "success")

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """
    This function logs the user out by clearing their session and redirects them to the home page
    """
    session.clear()
    return redirect(url_for('home'))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    # after this innitialize your database in the terminal
    def __str__(self):
        return f"{self.id} {self.content}"


def todo_serializer(todo):
    return {
        "id": todo.id,
        "content": todo.content
    }


@app.route('/', methods=['GET'])
def home():
    username = session.get('username', None)
    return str(username)
    # return render_template('home.html', title='Home', username=username)


@app.route("/api", methods=["GET"])
def index():
    # function is todo_serializer iterable is Todo.query.all()
    return jsonify([*map(todo_serializer, Todo.query.all())])


@app.route("/api/create", methods=["POST"])
def create():
    # convert to python dictonary using  json.loads()
    request_data = json.loads(request.data)
    todo = Todo(content=request_data["content"])

    db.session.add(todo)
    db.session.commit()

    return {'201': "todo created successfully"}


@app.route("/api/<int:id>")
def show(id):
    return jsonify([*map(todo_serializer, Todo.query.filter_by(id=id))])


@app.route("/api/<int:id>", methods=["DELETE"])
def delete(id):
    Todo.query.filter_by(id=id).delete()
    db.session.commit()

    return {'204': "Deleted successfully"}


@app.route("/api/<int:id>", methods=["PUT"])
def update(id):
    request_data = json.loads(request.data)
    # todo = Todo.query.get(id)
    todo = db.session.get(Todo, id)
    if not todo:
        return {"error": "Todo not found"}

    todo.content = request_data.get("content", todo.content)
    db.session.commit()

    return {'200': "Updated successfully"}


if __name__ == '__main__':
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully.")
    app.run(debug=True)
