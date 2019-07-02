import sqlite3
from flask_restful import Resource, reqparse

class User:
	def __init__(self, _id, username, password): 
		self.id = _id
		self.username = username
		self.password = password


class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
			type=str,
			required=True,
			help="This field cannot be blank."

	)
	parser.add_argument('password',
			type=str,
			required=True,
			help="This field cannot be blank."

	)


	def post(self):
		data = UserRegister.parser.parse_args()

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {"message": "User created successfully."}, 201

