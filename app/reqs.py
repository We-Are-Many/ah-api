from app import app
from flask import jsonify, request, Flask, json
from flaskext.mysql import MySQL

import traceback, warnings
import requests
import json
import urllib2

mysql = MySQL()

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
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		cursor.execute("INSERT INTO user_details VALUES (%s, %s, %s, %s, %s)", (user_name, name, email, location, talk_points))
		conn.commit()
		conn.close()
		return dataFormatter(200, "Success", [])
	except:
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		cursor.execute("INSERT INTO user_problems VALUES (%s, %s)", (user_name, problem))
		conn.commit()
		conn.close()
		return dataFormatter(200, "Success", [])
	except:
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

@app.route('/postmessage', methods=['POST'])
def save_message():
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		conn.close()
	except:
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

@app.route('/fetchmessage', methods=['GET'])
def get_message():
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		conn.close()
	except:
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])

@app.route('/saveuserrating', methods=['POST'])
def save_rating():
	conn = mysql.connect()
	try:
		cursor = conn.cursor()
		conn.close()
	except:
		conn.close()
		return dataFormatter(500, "Database Disconnect", [])
