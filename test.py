from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/practice"
mongo = PyMongo(app)

@app.route('/')
def home():
    return 'Welcome to my API!'

@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 + num2

    my_collection = mongo.db.numbers
    result_id = str(ObjectId())
    my_collection.insert_one({'_id': result_id, 'num1': num1, 'num2': num2, 'result': result})

    return jsonify({'result_id': result_id, 'result': result})

# Create operation
# @app.route('/add', methods=['POST'])
# def add_numbers():
#     data = request.get_json()
#     num1 = data['num1']
#     num2 = data['num2']
#     result = num1 + num2

#     my_collection = mongo.db.numbers
#     my_collection.insert_one({'num1': num1, 'num2': num2, 'result': result})

#     return jsonify({'result': result})

# Read operation
@app.route('/get/<id>', methods=['GET'])
def get_result(id):
    my_collection = mongo.db.numbers
    data = my_collection.find_one_or_404({'_id': id})
    return jsonify({'num1': data['num1'], 'num2': data['num2'], 'result': data['result']})

# Update operation
@app.route('/update/<id>', methods=['PUT'])
def update_result(id):
    my_collection = mongo.db.numbers
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 + num2
    my_collection.update_one({'_id': id}, {'$set': {'num1': num1, 'num2': num2, 'result': result}})
    return jsonify({'result': "updated successfully"})
    

# Delete operation
@app.route('/delete/<id>', methods=['DELETE'])
def delete_result(id):
    my_collection = mongo.db.numbers
    my_collection.delete_one({'_id': id})
    return jsonify({'result': 'Deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
