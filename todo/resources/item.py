# Importa el módulo uuid para generar identificadores únicos universales
import uuid
# Importa la clase MethodView de flask.views
from flask.views import MethodView
# Importa la clase Blueprint y la función abort de flask_smorest
from flask_smorest import Blueprint, abort

# Importa los esquemas ItemSchema e ItemUpdateSchema desde el archivo schemas.py
from schemas import ItemSchema, ItemUpdateSchema
# Importa la variable items desde el archivo db.py
from db import items

# Crea un objeto Blueprint llamado "Items" con descripción "Operations on items"
blp = Blueprint("Items", "items", description="Operations on items")

# Define una ruta "/item/<string:item_id>" dentro del Blueprint
@blp.route("/item/<string:item_id>")
# Define una clase llamada Item que hereda de MethodView
class Item(MethodView):
    # Define un método GET con decorador de respuesta 200 y esquema ItemSchema
    @blp.response(200, ItemSchema)
    # Define la función get que toma un parámetro item_id
    def get(self, item_id):
        try:
            # Intenta devolver el item correspondiente al item_id proporcionado
            return items[item_id]
        except KeyError:
            # Si el item no se encuentra, aborta la solicitud con código de error 404 y un mensaje
            abort(404, message="Item not found.")

    # Define un método DELETE
    def delete(self, item_id):
        try:
            # Intenta eliminar el item correspondiente al item_id proporcionado
            del items[item_id]
            # Si se elimina con éxito, devuelve un mensaje de confirmación
            return {"message": "Item deleted."}
        except KeyError:
            # Si el item no se encuentra, aborta la solicitud con código de error 404 y un mensaje
            abort(404, message="Item not found.")

    # Define un método PUT con decoradores para validar el esquema de actualización del item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # Define la función put que toma item_data y item_id como parámetros
    def put(self, item_data, item_id):
        try:
            # Intenta obtener el item correspondiente al item_id proporcionado
            item = items[item_id]
            # Fusiona (actualiza) el item existente con los datos del item_data proporcionado
            item |= item_data
            # Devuelve el item actualizado
            return item
        except KeyError:
            # Si el item no se encuentra, aborta la solicitud con código de error 404 y un mensaje
            abort(404, message="Item not found.")

# Define una ruta "/item" dentro del Blueprint
@blp.route("/item")
# Define una clase llamada ItemList que hereda de MethodView
class ItemList(MethodView):
    # Define un método GET para obtener una lista de todos los items
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # Devuelve todos los items como valores del diccionario items
        return items.values()

    # Define un método POST para crear un nuevo item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    # Define la función post que toma item_data como parámetro
    def post(self, item_data):
        # Itera sobre todos los items existentes para verificar si ya existe un item con los mismos datos
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                # Si ya existe un item con los mismos datos, aborta la solicitud con código de error 400 y un mensaje
                abort(400, message=f"Item already exists.")

        # Genera un nuevo ID único para el nuevo item
        item_id = uuid.uuid4().hex
        # Crea un nuevo item combinando los datos proporcionados con el nuevo ID generado
        item = {**item_data, "id": item_id}
        # Agrega el nuevo item al diccionario de items
        items[item_id] = item

        # Devuelve el nuevo item creado
        return item