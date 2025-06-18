from flask import Blueprint, jsonify,request,abort
from app.models.message import Message
from .. import db
from ..schemas.message_schema import MessageSchema

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

messages_bp = Blueprint('messages', __name__)

@messages_bp.route("/", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([msg.to_dict() for msg in messages])

# Rota para obter uma mensagem por id
@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return jsonify(message.to_dict()), 200

# Rota para criar uma nova mensagem
@messages_bp.route('/', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or 'content' not in data:
        abort(400, description="Campo 'content' é obrigatório.")
    autor_padrao = 1
    new_message = Message(content=data['content'], autor=autor_padrao)
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201

# Rota para atualizar uma mensagem existente
@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.get_json()
    if not data or 'content' not in data:
        abort(400, description="Campo 'content' é obrigatório.")
    if "autor" in data and data["autor"] != message.autor:
        return jsonify({"erro": "O autor da mensagem não pode ser alterado."}), 400
    message.content = data['content']
    db.session.commit()
    
    return jsonify(message.to_dict()), 200

# Rota para deletar uma mensagem
@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return '', 204