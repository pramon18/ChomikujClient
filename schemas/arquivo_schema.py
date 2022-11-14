from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.arquivo import Arquivo

class ArquivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Arquivo
        include_relationships = True
        load_instance = True