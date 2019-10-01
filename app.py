from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)


sneakers = [
    {'name': 'Air Jordan 4 Bred', 'brand': 'Air Jordan', 'price': '$190.00'},
    {'name': 'VaporMax Plus', 'brand': 'Nike', 'price': '$180.00'}
]

@app.route('/')
def sneakers_index():

    return render_template('sneakers_index.html', sneakers=sneakers)


if __name__ == '__main__':
    app.run(debug=True)
