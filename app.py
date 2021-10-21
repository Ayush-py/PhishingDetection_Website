from flask import Flask,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import pickle
from FeatureExtraction import predict

app = Flask(__name__,template_folder="templates")

@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")

@app.route("/about",methods=['GET'])
@cross_origin()
def about():
	return render_template("about.html")

@app.route("/blog",methods=['GET'])
@cross_origin()
def Blog():
	return render_template("Blog.html")

@app.route("/behindthescenes",methods=['GET'])
@cross_origin()
def bts():
	return render_template("services.html")

@app.route("/statistics",methods=['GET'])
@cross_origin()
def statistics():
	return render_template("Statistics.html")

@app.route("/detecturl",methods=['GET'])
@cross_origin()
def detecturl():
	return render_template("DetectURL.html")

@app.route("/predict",methods=['GET', 'POST'])
@cross_origin()
def prediction():
	if request.method == "POST":
		url = request.form['url']
		try:
			status = predict(url)
			status = int(status[0])
		except:
			return render_template("DetectURL.html")
		finally:	
			if  status == 0:
				return render_template("result.html",leg=status,name=url)
			else:
				return render_template("result.html",leg=status,name=url)
	return render_template("DetectURL.html")

if __name__=='__main__':
	app.run(debug=True)

