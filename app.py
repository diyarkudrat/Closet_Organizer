from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
import os
from datetime import datetime


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/SneakerCentral')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
sneakers = db.sneakers
streetwears = db.streetwears

db = client.get_default_database()
sneakers = db.sneakers
streetwears = db.streetwears

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

# streetwears = [
#     { 'brand': 'Gucci' },
#     { 'type': 'Shirt' }
# ]

@app.route('/sneakers/streetwears')
def streetwears_index():
    # `print('!!!!!!!!!!')`
    return render_template('streetwears_index.html', streetwears=streetwears.find())

@app.route('/sneakers/streetwears/new')
def streetwears_new():
    return render_template('streetwears_new.html', streetwear={}, title='New Streetwear')

@app.route('/sneakers/streetwears/submit', methods=['POST'])
def streetwears_submit():
    streetwear = {
        'name': request.form.get('name'),
        'brand': request.form.get('brand'),
        'type': request.form.get('type'),
        'size': request.form.get('size'),
        'color': request.form.get('color'),
        'price': request.form.get('price'),
        'created_at': datetime.now(),
        'photo_url': request.form.get('photo_url')
    }
    # print('!!!!!!!!')
    streetwear_id = streetwears.insert_one(streetwear).inserted_id
    print(streetwear_id)
    return redirect(url_for('streetwears_index', streetwear_id=streetwear_id))

@app.route('/sneakers/streetwears/<streetwear_id>')
def streetwears_show(streetwear_id):
    streetwear = streetwears.find_one({'_id': ObjectId(streetwear_id)})
    return render_template('streetwears_show.html', streetwear=streetwear)

@app.route('/sneakers/streetwears/<streetwear_id>/edit')
def streetwears_edit(streetwear_id):
    streetwear = streetwears.find_one({'_id': ObjectId(streetwear_id)})
    return render_template('streetwears_edit.html', streetwear=streetwear, title='Edit Streetwear')

@app.route('/sneakers/streetwears/<streetwear_id>', methods=['POST'])
def streetwears_update(streetwear_id):
    updated_streetwear = {
        'name': request.form.get('name'),
        'brand': request.form.get('brand'),
        'type': request.form.get('type'),
        'size': request.form.get('size'),
        'price': request.form.get('price'),
        'photo_url': request.form.get('photo_url')
    }
    streetwears.update_one(
        {'_id': ObjectId(streetwear_id)},
        {'$set': updated_streetwear}
    )
    return redirect(url_for('streetwears_show', streetwear_id=streetwear_id))

@app.route('/sneakers/streetwears/<streetwear_id>/delete', methods=['POST'])
def streetwears_delete(streetwear_id):
    streetwears.delete_one({'_id': ObjectId(streetwear_id)})
    return redirect(url_for('streetwears_index'))

@app.route('/search', methods=['POST'])
def search():
    searched_sneakers = sneakers.find()
    search = request.form.get('search')
    search_items = []

    for sneaker in searched_sneakers:
        if search.lower() in sneaker['name'].lower():
            search_items.append(sneaker)
        elif search.lower() in sneaker['brand'].lower():
            search_items.append(sneaker)
        elif search.lower() in sneaker['price'].lower():
            search_items.append(sneaker)
        elif search.lower() in sneaker['colorway'].lower():
            search_items.append(sneaker)
        elif search.lower() in sneaker['release_date'].lower():
            search_items.append(sneaker)
        else:
            print('No results')

    return render_template('sneakers_index.html', sneakers=search_items)

@app.route('/streetwears/search', methods = ['POST'])
def streetwears_search():
    searched_streetwears = streetwears.find()
    search = request.form.get('search')
    search_items = []

    for streetwear in searched_streetwears:
        if search.lower() in streetwear['name'].lower():
            search_items.append(streetwear)
        elif search.lower() in streetwear['brand'].lower():
            search_items.append(streetwear)
        elif search.lower() in streetwear['price'].lower():
            search_items.append(streetwear)
        elif search.lower() in streetwear['type'].lower():
            search_items.append(streetwear)
        elif search.lower() in streetwear['size'].lower():
            search_items.append(streetwear)
        else:
            print('No results')

    return render_template('streetwears_index.html', streetwears=search_items)







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
