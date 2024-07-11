from datetime import timedelta
import os
import mwoauth
import secrets
from flask import Flask, jsonify, request, json, session, redirect,render_template
from waitress import serve
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', "supersecretkey")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///example.db')
app.config['OAUTH_MWURI'] = os.getenv('OAUTH_MWURI')
app.config['CONSUMER_KEY'] = os.getenv('CONSUMER_KEY')
app.config['CONSUMER_SECRET'] = os.getenv('CONSUMER_SECRET')
app.config['FRONTEND_URL'] = os.getenv('FRONTEND_URL')

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  
app.config['SESSION_COOKIE_SECURE'] = True     


db = SQLAlchemy(app)
CORS(app, supports_credentials=True, origins=[app.config['FRONTEND_URL']])
app.debug = os.getenv('FLASK_ENV') == 'development'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f"{self.id} {self.content}"

def todo_serializer(todo):
    return {"id": todo.id, "content": todo.content}

@app.before_request
def require_login():
    # List of routes that do not require authentication
    public_routes = ('index', 'login', 'logout', 'oauth_callback', 'static')
    
    # Allow access if the endpoint is in the public_routes list or username is set
    if request.endpoint not in public_routes and 'username' not in session:
        return jsonify({"error": "Authentication required. Please log in."}), 401

@app.route("/login")
def login():
    consumer_token = mwoauth.ConsumerToken(app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"])
    try:
        redirect_url, request_token = mwoauth.initiate(app.config["OAUTH_MWURI"], consumer_token)
    except Exception:
        app.logger.exception("mwoauth.initiate failed")
        return jsonify({"error": "OAuth initiation failed"}), 500
    else:
        session["request_token"] = dict(zip(request_token._fields, request_token))
        return jsonify({"redirect_url": redirect_url})

@app.route("/oauth-callback")
def oauth_callback():
    if "request_token" not in session:
        return jsonify({"error": "OAuth callback failed. Are cookies disabled?"}), 400

    consumer_token = mwoauth.ConsumerToken(app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"])
    try:
        access_token = mwoauth.complete(
            app.config["OAUTH_MWURI"],
            consumer_token,
            mwoauth.RequestToken(**session["request_token"]),
            request.query_string
        )
        identity = mwoauth.identify(app.config["OAUTH_MWURI"], consumer_token, access_token)
    except Exception:
        app.logger.exception("OAuth authentication failed or already authenticated")
        return jsonify({"error": "OAuth authentication failed or already authenticated"}), 500
    else:
        session["access_token"] = dict(zip(access_token._fields, access_token))
        session["username"] = identity["username"]

    # Render the completion template
    return render_template("auth_complete.html")

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"msg": "logged out successfully"})

@app.route("/user-info")
def get_user_info():
    username = session.get("username", None)
    if username:
        return jsonify({"username": username})
    
    return jsonify({"msg": "Please Authenticate, go to the /login route"}), 401


@app.route("/api", methods=["GET"])
def get_all():
    todos = [todo_serializer(todo) for todo in Todo.query.all()]
    username = session.get("username", None)
    greetings = {
        "FIRST_MSG": "Welcome to the TODO app!",
        "SECOND_MSG": "Have a productive day!"
    }
    todos.extend([
        {"content": greetings.get("FIRST_MSG"), "id": 4},
        {"content": greetings.get("SECOND_MSG", "my default"), "id": 5}
    ])
    # todos.append({"username": username})
    return jsonify(todos)

@app.route("/api/create", methods=["POST"])
def create():
    request_data = json.loads(request.data)
    todo = Todo(content=request_data["content"])
    db.session.add(todo)
    db.session.commit()
    return jsonify({'msg': "Todo created successfully"}), 201

@app.route("/api/<int:id>", methods=["GET"])
def show(id):
    return jsonify(todo_serializer(Todo.query.get_or_404(id)))

@app.route("/api/<int:id>", methods=["DELETE"])
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'msg': "Deleted successfully"}), 204

@app.route("/api/<int:id>", methods=["PUT"])
def update(id):
    request_data = json.loads(request.data)
    todo = db.session.get(Todo, id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    todo.content = request_data.get("content", todo.content)
    db.session.commit()
    return jsonify({'msg': "Updated successfully"}), 200

if __name__ == "__main__":
    port = 8000
    print(f"Server has started..@port:{port}")
    serve(app, host="0.0.0.0", port=port)
