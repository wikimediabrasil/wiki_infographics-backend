from flask import Flask, jsonify, request, json
from waitress import serve
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text, nullable=False)

  # after this innitialize your database in theterminal
  def __str__(self):
    return f"{self.id} {self.content}"
  
# Enable CORS for all routes
CORS(app)

# Enable debug mode
app.debug = True 

def todo_serializer(todo):
  return {
    "id": todo.id,
    "content": todo.content
  }

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


if __name__ == "__main__":
  print("Server has started..") 
  serve(app, host="0.0.0.0", port=8000)