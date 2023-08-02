from main import db

class Chats(db.Model):
    __tablename__='Chats'
    id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    name=db.Column(db.String,nullable=False)
    messages = db.relationship('Messages',backref='Chat')

class Messages(db.Model):
    __tablename__='Messages'
    id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    content=db.Column(db.String,nullable=False)
    chat_id = db.Column(db.Integer,db.ForeignKey('Chats.id'),nullable=False)
    by_user=db.Column(db.Integer,nullable=False)