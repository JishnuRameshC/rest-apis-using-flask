from flask import Flask, request
from flask_restful import abort
from db import stores,items
import uuid


app = Flask(__name__)


@app.get('/store')
def get_all_stores():
    return {"stores":list(stores.values())}

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort (404,message = "Store not found ")


@app.post('/store')
def create_store():
    store_data = request.get_json()

    # Check if 'name' is included in the JSON payload
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in JSON payload.")
        # return {"message": "Bad request. Ensure 'name' is included in JSON payload."}, 400

    # Check if a store with the same name already exists
    for existing_store in stores.values():
        if store_data["name"] == existing_store["name"]:
            abort(409, message="Store already exists.")
            # return {"message": "Store already exists."}, 409

    # If the store does not exist, create a new store
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201




@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Item deleted successfully"}
    except KeyError:
        abort (404,message = "Store not found ")
        # return {"message": "Item Not fount"},404


@app.get('/item')
def get_all_items():
    return {"items":list(items.values())}


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort (404,message = "Item not found ")
        # return {"message": "Item Not fount"},404


@app.post('/item')
def create_item():
    item_data = request.get_json()

    # checking if "price", "store_id" and "name" are included in the JSON payload
    if (
        "price" not in item_data 
        or "store_id" not in item_data 
        or "name" not in item_data
    ):
        abort(400, message = "Bad request. Ensure 'price', 'name' and 'store_id are included in the JSON payload")
        # return {"message": "BAD request"}, 400
    
    # Checking if an item with the same name and store_id already exists
    for item in items.values():
        if(
            item_data["name"] == item ["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message= "item already exits. ")
            # return {"message": "item already exits"}, 400
        
    # Checking if the specified store_id exists in the stores dictionary
    if item_data["store_id"] not in stores:
        abort(400, message= "store_id does not exist. ")
        # return {"message": "Store_id not found"}, 400

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item,201


@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted successfully"}
    except KeyError:
        abort (404,message = "Store not found ")
        # return {"message": "Item Not fount"},404


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(404, message= "item not found")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message = "item not found")
