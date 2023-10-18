from flask import Flask
from flask_restful import Api
from resources.store import StoreResource, StoreListResource 
from resources.item import ItemResource, ItemListResource
app = Flask(__name__)
api = Api(app)

api.add_resource(StoreResource, '/store/<string:store_id>')
api.add_resource(StoreListResource, '/store')
api.add_resource(ItemResource, "/item/<string:item_id>")
api.add_resource(ItemListResource, "/item")

if __name__ == " __main__":
    app.run(debug=True)
