import uuid  # Importa el módulo uuid para generar identificadores únicos
from flask.views import MethodView  # Importa la clase MethodView de Flask para definir vistas basadas en clases
from flask_smorest import Blueprint, abort  # Importa Blueprint y abort de Flask-Smorest para definir rutas y manejar errores
from db import stores  # Importa la variable stores desde el módulo db, que probablemente contiene información sobre tiendas
from schemas import StoreSchema  # Importa la clase StoreSchema desde el módulo schemas para validar y serializar datos

# Crea un objeto Blueprint llamado "Stores" con la descripción "Operations on stores"
blp = Blueprint("Stores", "stores", description="Operaciones en tiendas")

# Define una ruta "/store/<string:store_id>" y una vista asociada llamada Store
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    # Define un método GET para obtener los detalles de una tienda
    @blp.response(200, StoreSchema)  # Define la respuesta esperada como un objeto StoreSchema
    def get(cls, store_id):
        try:
            # Intenta devolver los detalles de la tienda con el ID proporcionado
            return stores[store_id]  # Devuelve los detalles de la tienda con el ID proporcionado
        except KeyError:
            abort(404, message="Tienda no encontrada.")  # Aborta la solicitud con un código de error 404 si la tienda no se encuentra

    # Define un método DELETE para eliminar una tienda
    def delete(cls, store_id):
        try:
            del stores[store_id]  # Elimina la tienda con el ID proporcionado
            return {"message": "Tienda eliminada."}  # Devuelve un mensaje de éxito
        except KeyError:
            abort(404, message="Tienda no encontrada.")  # Aborta la solicitud con un código de error 404 si la tienda no se encuentra

# Define una ruta "/store" y una vista asociada llamada StoreList
@blp.route("/store")
class StoreList(MethodView):
    # Define un método GET para obtener la lista de todas las tiendas
    @blp.response(200, StoreSchema(many=True))  # Define la respuesta esperada como una lista de objetos StoreSchema
    def get(cls):
        return stores.values()  # Devuelve los valores de todas las tiendas almacenadas

    # Define un método POST para agregar una nueva tienda
    @blp.arguments(StoreSchema)  # Valida y deserializa los datos de entrada usando StoreSchema
    @blp.response(201, StoreSchema)  # Define la respuesta esperada como un objeto StoreSchema
    def post(cls, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"La tienda ya existe.")  # Aborta la solicitud con un código de error 400 si la tienda ya existe

        store_id = uuid.uuid4().hex  # Genera un ID único para la nueva tienda
        store = {**store_data, "id": store_id}  # Crea un diccionario que representa la nueva tienda
        stores[store_id] = store  # Agrega la nueva tienda al diccionario de tiendas

        return store  # Devuelve los detalles de la nueva tienda