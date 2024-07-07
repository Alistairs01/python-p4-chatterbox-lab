from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)



@app.route('/messages', methods=['GET', 'POST'])

def get_messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]

        response = make_response(jsonify(messages), 200)
        return response
    

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(username=data('username'), body=data('body'))
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()
        response = make_response(jsonify(message_dict), 201)
        return response
    

@app.route('/messages/<int:message_id>', methods=['GET', 'PATCH', 'DELETE'])

def get_one_message(message_id):

    message = Message.query.filter_by(id=message_id).first()

    if request.method == 'GET':
        if message == None:
            response = make_response(jsonify({"message": "Message not found"}), 404)
            return response
        
        message_dict = message.to_dict()
        response = make_response(jsonify(message_dict), 200)
        return response

    elif request.method == 'PATCH':

        if message == None:
            response = make_response(jsonify({"message": "Message not found"}), 404)
            return response
        message = Message.query.get_or_404(message_id)
        data = request.get_json()
        message.username = data.get('username', message.username)
        message.body = data.get('body', message.body)
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(jsonify(message_dict), 200)
        return response

    elif request.method == 'DELETE':
        message = Message.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5555)
