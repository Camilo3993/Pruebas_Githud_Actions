# Importamos las clases Schema y fields del módulo marshmallow
from marshmallow import Schema, fields

# Definimos una clase llamada ItemSchema que hereda de Schema
class ItemSchema(Schema):
    # Definimos un campo 'id' que será de tipo string y se utilizará solo para dumping (no se incluirá en la carga)
    id = fields.Str(dump_only=True)
    # Definimos un campo 'name' que será de tipo string y es requerido
    name = fields.Str(required=True)
    # Definimos un campo 'price' que será de tipo float y es requerido
    price = fields.Float(required=True)
    # Definimos un campo 'store_id' que será de tipo string y es requerido
    store_id = fields.Str(required=True)

# Definimos una clase llamada ItemUpdateSchema que hereda de Schema
class ItemUpdateSchema(Schema):
    # Definimos un campo 'name' que será de tipo string
    name = fields.Str()
    # Definimos un campo 'price' que será de tipo float
    price = fields.Float()

# Definimos una clase llamada StoreSchema que hereda de Schema
class StoreSchema(Schema):
    # Definimos un campo 'id' que será de tipo string y se utilizará solo para dumping (no se incluirá en la carga)
    id = fields.Str(dump_only=True)
    # Definimos un campo 'name' que será de tipo string y es requerido
    name = fields.Str(required=True)