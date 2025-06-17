from .. import ma
from marshmallow import fields, validate
from ..models.usuario import Usuario

class usuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True  
        fields = ("id", "content", "created_at")  # mantém a ordem do modelo
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Length(min=1, max=140))
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=140))
    senha = fields.Str(required=True, validate=validate.Length(min=1, max=140))
    created_at = fields.DateTime(dump_only=True)