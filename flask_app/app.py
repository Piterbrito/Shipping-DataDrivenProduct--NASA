import os
import pandas as pd
import numpy as np
import pandas as pd
import pymongo
import json
from flask_pymongo import PyMongo
from flask import Flask, jsonify, render_template, request

import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scraper")
def scraperPage():
    return render_template("scraper.html")

@app.route('/scrape')
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/news", methods=['GET'])
def get_api1():
    # return render_template("api.html")
    api = mongo.db.mars

    output = []
    for x in api.find():
        print(x)
        output.append({'mars_news' : x['news_title'], 'mars_paragraph' : x['news_paragraph']}) 
    
    return jsonify({'result': output})



@app.route("/api/weather", methods=['GET'])
def get_api2():
    # return render_template("api.html")
    api = mongo.db.mars

    output = []
    for x in api.find():
        print(x)
        output.append({'mars_weather' : x['weather']}) 
    
    return jsonify({'result': output})

    
@app.route("/api/facts", methods=['GET'])
def get_api3():
    # return render_template("api.html")
    api = mongo.db.mars

    output = []
    for x in api.find():
        print(x)
        output.append({"mars_facts": x['facts']}) 
    
    return jsonify({'result': output})
    return jsonify({api})


if __name__ == "__main__":
    app.run(debug=True)
