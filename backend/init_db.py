from backend.app import app, db
from backend.app import Todo


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    print("Database tables created")
    todo = Todo(content="I need to eat")
    second_todo = Todo(content="I need to learn Flask")
    print("Content added")
    db.session.add(todo)
    db.session.add(second_todo)
    db.session.commit()
    print("Data committed")