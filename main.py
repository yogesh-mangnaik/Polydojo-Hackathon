from flask import Flask, render_template, request
import json
from app import processMail
import os
import pickle
import pandas as pd
import csv

fields = {}

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
	return render_template("home.html")

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
	data = request.data.decode('utf-8')
	d = json.loads(data)
	valueList = d['responseList']
	for i in valueList:
		value = i['val']
		label = i['label']
		fields[label] = value
	myData = [[fields['ID Number'], fields['Name'], fields['Email']]]
	with open('users.csv', 'a') as file:
		writer = csv.writer(file)
		writer.writerows(myData)
	# processMail(fields)
	return render_template("home.html")

@app.route('/confirmation/', methods=['POST', 'GET'])
def confirm():
	requestData = request.data.decode('utf-8')
	d = json.loads(requestData)
	valueList = d['responseList']
	fields = {}
	for i in valueList:
		value = i['val']
		label = i['label']
		fields[label] = value
	data = pd.read_csv('users.csv')
	idn = fields['ID Number']
	
	ids = data['id']
	emails = data['email']
	names = data['name']
	l = len(data)
	for i in range(l):
		if int(idn) == int(ids[i]):
			details = {}
			details["name"] = names[i]
			details["email"] = emails[i]
			details['status'] = fields['Approve']
			processMail(details)
			break
	
	return render_template("home.html")

if __name__ == '__main__':
   app.run(debug = True)

