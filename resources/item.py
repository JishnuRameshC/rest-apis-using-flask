from flask import request
from flask_restful import Resource, reqparse, abort
import uuid
from db import items

class ItemResource(Resource):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("price", type=float)
        args = parser.parse_args()

        try:
            item = items[item_id]
            item |= args
            return item
        except KeyError:
            abort(404, message="Item not found.")

class ItemListResource(Resource):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("price", type=float, required=True)
        parser.add_argument("store_id", type=str, required=True)
        args = parser.parse_args()

        for item in items.values():
            if (
                args["name"] == item["name"]
                and args["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**args, "id": item_id}
        items[item_id] = item

        return item, 201


