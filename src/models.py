from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    tasks = db.relationship('Task')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<Usuario %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable =False)
    done = db.Column(db.Boolean, nullable=False)
    usuario_username = db.Column(db.String(20), db.ForeignKey('usuario.username'), nullable=False)
    usuario = db.relationship('Usuario')

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '<Task (label:%r , done:%r)>' % self.label, self.done

    def serialize(self):
        return {
            "label": self.label,
            "done": self.done,
        }

    