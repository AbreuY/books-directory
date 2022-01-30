"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException
from models import db, Books
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Create all tables
# with app.app_context():
#     db.create_all()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/books', methods=['POST', 'GET'])
@app.route('/books/<int:book_id>', methods=['PUT', 'GET', 'DELETE'])
def handle_books(book_id=None):
    if request.method == "GET":
        if book_id:
            one_book = Books.query.filter_by(id=book_id).one_or_none()
            if one_book is not None:
                return jsonify(one_book.serialize()), 200
            else: return jsonify({"msg":"Book not found!"}), 404
        elif book_id == 0:
            return jsonify({"msg":"Book not found!"}), 404
        books = Books.query.all()
        response = []
        for book in books:
            response.append(book.serialize())
        
        return jsonify(response), 200
    elif request.method == "POST":
        print(request.json)
        if request.json is None:
            return jsonify({'message':'The request was invalid'}), 400
        for key in request.json:
            if(request.json[key] == ""):
                return jsonify({"msg":"All fields should be filled!" }), 400
        
        body = request.json
        book = Books.create(body)
        return jsonify(book.serialize()), 201
    elif request.method == "PUT":
        for key in request.json:
            if(request.json[key] == ""):
                return jsonify({"msg":"All fields should be filled!" }), 400
        book = Books.query.filter_by(id=book_id).one_or_none()
        if book is not None:
             updated = book.update(request.json)
             print(request.json)
             if updated:
                 return jsonify({"message":"Book updated!", "Book":book.serialize()}), 200
             else:
                 return jsonify({"message":"Something went wrong!"}), 500
        return jsonify({"message":"Book does not exist!"}), 404

    elif request.method == "DELETE":
        book = Books.query.filter_by(id=book_id).one_or_none()
        if book is None:
            return jsonify({"message": "Book not found"}), 404
        deleted = book.delete()
        if deleted == False:
            return jsonify({"message":"Something happen try again!"}), 500
        return jsonify({"message":"Book deleted!"}), 204

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
