from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
import os
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/SneakerCentral')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
sneakers = db.sneakers

app = Flask(__name__)


@app.route('/')
def sneakers_index():
    #Homepage
    return render_template('sneakers_index.html', sneakers=sneakers.find())

@app.route('/sneakers/<sneaker_id>/delete', methods = ['POST'])
def sneakers_delete(sneaker_id):
    #Able to delete an item
    sneakers.delete_one({'_id': ObjectId(sneaker_id)})
    return redirect(url_for('sneakers_index'))

@app.route('/sneakers/<sneaker_id>', methods = ['POST'])
def sneakers_update(sneaker_id):
    updated_sneaker = {
        'name': request.form.get('name'),
        'brand': request.form.get('brand'),
        'colorway': request.form.get('colorway'),
        'price': request.form.get('price'),
        'release_date': request.form.get('release_date'),
        # FIX INSERT PHOTO
        'photo_url': request.form.get('photos')
    }
    sneakers.update_one(
        {'_id': ObjectId(sneaker_id)},
        {'$set': updated_sneaker})
    return redirect(url_for('sneakers_show', sneaker_id=sneaker_id))

@app.route('/sneakers/<sneaker_id>/edit')
def sneakers_edit(sneaker_id):
    #able to edit an item
    sneaker = sneakers.find_one({'_id': ObjectId(sneaker_id)})
    return render_template('sneakers_edit.html', sneaker = sneaker)

@app.route('/sneakers/<sneaker_id>')
def sneakers_show(sneaker_id):
    #displays information of item user enters in
    sneaker = sneakers.find_one({'_id': ObjectId(sneaker_id)})
    return render_template('sneakers_show.html', sneaker = sneaker)

@app.route('/sneakers/new')
def sneaker_new():
    #page where you create an item
    return render_template('sneakers_new.html', sneaker = {}, name = 'New Shoe')

@app.route('/sneakers', methods=['POST'])
def sneaker_create():
    #inserts information entered in by user into the database
    sneaker = {
            'name': request.form.get('name'),
            'brand': request.form.get('brand'),
            'created_at': datetime.now(),
            'photo_url': request.form.get('photos'),
            'colorway': request.form.get('colorway'),
            'release_date': request.form.get('release_date'),
            'price': request.form.get('price')
    }
    print(sneaker)
    sneaker_id = sneakers.insert_one(sneaker).inserted_id
    return redirect(url_for('sneakers_show', sneaker_id=sneaker_id))

streetwears = [
    {'brand': 'Gucci', 'type': 'Shirt'},
    {'brand': 'Louis Vuitton', 'type': 'Jacket'}
]

@app.route('/streetwear')
def streetwears_index():
    return render_template('streetwears_index.html', streetwears=streetwears)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
