#!/usr/bin/python

from app import app
from flask import jsonify, request, Flask, json
from flaskext.mysql import MySQL

import traceback, warnings
import requests
import json
import urllib2

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'legion5'
app.config['MYSQL_DATABASE_DB'] = 'ahack'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def dataFormatter(code, message, data):
	resp = jsonify({
		'code': code,
		'message': message,
		'data': data
	})
	resp.status_code = code
	return resp

@app.route('/', methods=['GET', 'POST'])
def personList():
	return dataFormatter(200, "Success", [])

@app.route('/newuser', methods=['POST'])
def create_user():
	user_name = request.form.get('user_name', '')
	name = request.form.get('name', '')
	email = request.form.get('email', '')
	location = request.form.get('location', '')
	talk_points = request.form.get('talk_points', '')
	problem = request.form.get('problem', '')
	print name, email
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		cursor.execute("SELECT count(*) from user_details where user_name=%s", (user_name))
		data = cursor.fetchall()
		cursor.execute("INSERT INTO user_details VALUES (%s, %s, %s, %s, %s)", (user_name, name, email, location, talk_points))
		cursor.execute("INSERT INTO user_problems VALUES (%s, %s)", (user_name, problem))
		conn.commit()
		cursor.close()
		conn.close()
		return dataFormatter(200, "Success", [])
	except:
		cursor.close()
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

@app.route('/postmessage', methods=['POST'])
def save_message():
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		from_user = request.form.get('from_user', '')
		to_user = request.form.get('to_user', '')
		message = request.form.get('message', '')
		process_query(message, from_user)
		cursor.execute("INSERT INTO messages VALUES (%s, %s, %s)", (to_user, from_user, message))
		conn.commit()
		cursor.close()
		conn.close()
		return dataFormatter(200, "Success", [])
	except:
		cursor.close()
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

@app.route('/saveuserrating', methods=['POST'])
def save_rating():
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		user_name = request.form.get('user_name', '')
		cursor.execute("SELECT rating, rating_count from acc_intents where user_name=%s", (user_name))
		data = cursor.fetchall()
		rating = data[0][0]
		counter = data[0][1]
		new_rating = request.form.get('rate', '')
		scaled_new_rating = (rating*counter + new_rating)/(counter + 1)
		new_counter = counter + 1
		cursor.execute("update acc_intents set rating=%d where user_name=%s", (scaled_new_rating, user_name))
		cursor.execute("update acc_intents set rating_count=%d where user_name=%s", (new_rating, user_name))
		conn.commit()
		cursor.close()
		conn.close()
		return dataFormatter(200, "Success", [])
	except:
		cursor.close()
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

noIntent = [
    "I'm having trouble understanding you, could you rephrase your question?",
    "I didn't catch that, could you rephrase your query?",
    "Sorry, I didn't understand that. Try rephrasing your request."
]

@app.route("/no_intent", methods=['POST'])
def no_intent():
    message = random.choice(noIntent)
    return message

@app.route("/switch_status", methods=['POST'])
def switch_status():
	user_name = request.form.get('user_name', '')
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		cursor.execute("UPDATE online_users SET is_online=0 where user_name=%s", (user_name))
		conn.commit()
		cursor.close()
		conn.close()
		return dataFormatter(200, "Success", [])
	except:
		cursor.close()
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

@app.route("/online_user", methods=['GET'])
def online_user():
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		cursor.execute("SELECT user_name from online_users where is_online=1")
		data = cursor.fetchall()
		online_users = []
		for row in data:
			user = row[0]
			online_users.append(user)
		conn.commit()
		cursor.close()
		conn.close()
		return online_users
	except:
		cursor.close()
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

def process_query(query, user_name):
    try:
        response = requests.get(url='https://api.wit.ai/message?v=20170409&q='+query,headers={'Authorization': 'Bearer VT4JUXRFXXQTIQ53V3IE3IZPLSY34Z5H'})
    except:
        return {'alcohol' : 0.0, 'positive' : 0.0, 'negative' : 0.0, 'extra' : 0.0}
    dict_response = json.loads(response.text)

    intent = None
    confidence = None
    entities = None
    msg = None
    response = {'alcohol' : 0.0, 'positive' : 0.0, 'negative' : 0.0, 'extra' : 0.0}

    if dict_response['entities']['intent']:
    	entities = dict_response['entities']
    	try:
        	intent = dict_response['entities']['intent'][0]['value']
        	confidence = dict_response['entities']['intent'][0]['confidence']
        	response[intent] += confidence
        except:
        	pass
        try:
        	intent = dict_response['entities']['intent'][1]['value']
        	confidence = dict_response['entities']['intent'][1]['confidence']
        	response[intent] += confidence
        except:
        	pass
        try:
        	intent = dict_response['entities']['intent'][2]['value']
        	confidence = dict_response['entities']['intent'][2]['confidence']
        	response[intent] += confidence
        except:
        	pass
        try:
        	intent = dict_response['entities']['intent'][3]['value']
        	confidence = dict_response['entities']['intent'][3]['confidence']
        	response[intent] += confidence
        except:
        	pass

    if dict_response['entities']['intent'][0]['value'] is None or dict_response['entities']['intent'][0]['confidence'] < 0.2:
        response = {'alcohol' : 0.0, 'positive' : 0.0, 'negative' : 0.0, 'extra' : 0.0}
    conn = mysql.connect()
    try:
		cursor = conn.cursor()
		cursor.execute("SELECT alcohol, positive, negative, extra from acc_intents where user_name=%s", (user_name))
		data = cursor.fetchall()
		alcohol = data[0][0]
		positive = data[0][1]
		negative = data[0][2]
		extra = data[0][3]
		new_alcohol = alcohol + response['alcohol']
		new_positive = positive + response['positive']
		new_negative = negative + response['negative']
		new_extra = extra + response['extra']
		cursor.execute("update acc_intents set alcohol=%d, positive=%d, negative=%d, extra=%d where user_name=%s", (new_alcohol, new_positive, new_negative, new_extra, user_name))
		conn.commit()
		cursor.close()
		conn.close()
	except:
		cursor.close()
		conn.close()
    