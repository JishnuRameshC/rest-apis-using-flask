from flask import request
from flask_restful import Resource, reqparse, abort
import uuid
from db import stores


class StoreResource(Resource):
    def get(self, store_id):
        try:
            # You presumably would want to include the store's items here too
            # More on that when we look at databases
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

class StoreListResource(Resource):
    def get(self):
        return list(stores.values())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Name cannot be blank.")
        args = parser.parse_args()

        for store in stores.values():
            if args["name"] == store["name"]:
                abort(400, message="Store already exists.")

        store_id = uuid.uuid4().hex
        store = {"id": store_id, "name": args["name"]}
        stores[store_id] = store

        return store, 201
