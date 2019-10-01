from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.SneakerCentral
sneakers = db.sneakers


app = Flask(__name__)


# sneakers = [
#     {'name': 'Air Jordan 4 Bred', 'brand': 'Air Jordan', 'price': '$190.00'},
#     {'name': 'VaporMax Plus', 'brand': 'Nike', 'price': '$180.00'}
# ]

@app.route('/')
def sneakers_index():

    return render_template('sneakers_index.html', sneakers=sneakers.find())


if __name__ == '__main__':
    app.run(debug=True)
