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

@app.route('/sneakers/new')
def sneaker_new():
    return render_template('sneakers_new.html')

@app.route('/sneakers', methods=['POST'])
def sneaker_create():
    sneaker = {
            'name': request.form.get('name'),
            'price': request.form.get('price'),
            'photo': request.form.get('Photos').split()
    }
    sneakers.insert_one(sneaker)
    return redirect(url_for('sneakers_index'))



if __name__ == '__main__':
    app.run(debug=True)
