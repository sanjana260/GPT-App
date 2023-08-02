from flask import Flask,render_template,request,redirect
from process import *
import os
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(os.getcwd(),"database.sqlite3")
db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()

@app.route("/<int:chat_id>",methods=['GET','POST'])
def chat(chat_id):
    chats= db.session.query(Chats).all()
    print(chats)
    if(request.method=="POST"):
        print("message received")
        content = request.form.get('input')
        print(content)
        message = Messages(content=content,chat_id = chat_id,by_user=1)
        db.session.add(message)
        db.session.commit()
        response = message_response(message)
        response_message = Messages(content=response,chat_id = chat_id,by_user=0)
        db.session.add(response_message)
        db.session.commit()
    chat = db.session.query(Chats).filter_by(id=chat_id).first()
    print(chat.messages)
    return render_template('chat.html',chat=chat,chats=chats,chat_id=chat.id)

@app.route("/",methods=['GET','POST'])
def home():
    chats= db.session.query(Chats).all()
    print(chats)
    return render_template('chat.html',chats=chats,chat_id='null')

@app.route("/new_chat",methods=['GET'])
def new_chat():
    chat = Chats(name="Untitled")
    db.session.add(chat)
    db.session.commit()
    return redirect(f'/{chat.id}')

@app.route("/change_chat_name/<name>/<int:chat_id>",methods=['GET'])
def change_name(name,chat_id):
    chat = db.session.query(Chats).filter_by(id=chat_id).first()
    chat.name=name 
    db.session.add(chat)
    db.session.commit()
    return f'/{chat_id}'

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000)
    db.create_all()

