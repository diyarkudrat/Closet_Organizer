from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', msg = 'SneakerCentral')


if __name__ == '__main__':
    app.run(debug=True)
