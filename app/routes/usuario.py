from flask import Blueprint, jsonify, request, abort
from email_validator import validate_email,EmailNotValidError
from app.models.usuario import Usuario 
from .. import db
from ..schemas.usuario_Schema import usuarioSchema

usuarios_bp = Blueprint('usuarios', __name__)
usuario_schema = usuarioSchema()
usuarios_schema = usuarioSchema(many=True)

# Rota para obter todos os usuários
@usuarios_bp.route("/", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.order_by(Usuario.created_at.desc()).all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

# Rota para obter um usuário por ID
@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify(usuario.to_dict()), 200

# Rota para criar um novo usuário
@usuarios_bp.route('/', methods=['POST'])
def create_usuario():
    data = request.get_json()
    if Usuario.query.filter_by(email=data['email']).first():
         abort(400, description="email ja existente")
    
    if not data or 'nome' not in data or len(data['nome']) < 1:
        abort(400, description="Campo 'nome' é obrigatório.")
    
    try:
        emailcheck = validate_email(data[email])
        email = emailcheck.normalized
    except EmailNotValidError as e :
        abort(400,description =e)
    
    novo_usuario = Usuario(nome=data['nome'],email=data['email'], senha = data['senha'])
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify(novo_usuario.to_dict()), 201

# Rota para atualizar um usuário existente
@usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    data = request.get_json()
    if not data or 'nome' not in data:
        abort(400, description="Campo 'nome' é obrigatório.")
    
    usuario.nome = data['nome']
    usuario.email = data['email']
    usuario.senha = data['senha']
    db.session.commit()
    
    return jsonify(usuario.to_dict()), 200

# Rota para deletar um usuário
@usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return '', 204
