#!python

import traceback, warnings
import requests

from flask import Flask, jsonify, json

from app import app

app.run(debug = True)

mysql = MySQL()

@app.route('/')
def main():
	return 

@app.route('/postmessage', methods=['POST'])
def save_message():
	conn = mysql.connect()

@app.route('/fetchmessage', methods=['GET'])
def get_message():
	conn = mysql.connect()

@app.route('/saveuserrating', methods=['POST'])
def save_rating():
	conn = mysql.connect()
