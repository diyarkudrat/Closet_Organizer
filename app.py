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

@app.route('/sneakers/<sneaker_id>/delete', methods = ['POST'])
def sneakers_delete(sneaker_id):
    sneakers.delete_one({'_id': ObjectId(sneaker_id)})
    return redirect(url_for('sneakers_index'))

@app.route('/sneakers/<sneaker_id>', methods = ['POST'])
def sneakers_update(sneaker_id):
    updated_sneaker = {
        'name': request.form.get('name'),
        'brand': request.form.get('brand'),
        # FIX INSERT PHOTO
        'photo': request.form.get('photos')
    }
    sneakers.update_one(
        {'_id': ObjectId(sneaker_id)},
        {'$set': updated_sneaker})
    return redirect(url_for('sneakers_show', sneaker_id=sneaker_id))

@app.route('/sneakers/<sneaker_id>/edit')
def sneakers_edit(sneaker_id):
    sneaker = sneakers.find_one({'_id': ObjectId(sneaker_id)})
    return render_template('sneakers_edit.html', sneaker = sneaker)

@app.route('/sneakers/<sneaker_id>')
def sneakers_show(sneaker_id):
    sneaker = sneakers.find_one({'_id': ObjectId(sneaker_id)})
    return render_template('sneakers_show.html', sneaker = sneaker)

@app.route('/sneakers/new')
def sneaker_new():
    return render_template('sneakers_new.html', sneaker = {}, name = 'New Shoe')

@app.route('/sneakers', methods=['POST'])
def sneaker_create():
    sneaker = {
            'name': request.form.get('name'),
            'brand': request.form.get('brand'),
            # 'photo': request.form.get('Photos').split()
    }
    sneaker_id = sneakers.insert_one(sneaker).inserted_id
    return redirect(url_for('sneakers_show', sneaker_id=sneaker_id))



if __name__ == '__main__':
    app.run(debug=True)
