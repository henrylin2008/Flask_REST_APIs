from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jj'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth 

items = []

class Item(Resource):
	@jwt_required()
	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item is not None else 404 

	def post(self, name): 
		if next(filter(lambda x: x['name'] == name, items), None) is not None: 
			return {'message': "An item with name '{}' already exist".format(name)}, 400 

		data = request.get_json() # (force=True) or slience=True 
		item = {'name': name, 'price': data['price']}
		items.append(item)
		return item, 201


	@jwt_required()
	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item deleted'}


	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()
		# Once again, print something not in the args to verify everything works
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)
		return item

class ItemList(Resource): 
	def get(self): 
		return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)