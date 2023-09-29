For creating this Restfull API web app

Steps
 - create a folder for project
 - create python flask environment "python -m  venv flask
 - activate the environment flask\Scripts\activate
 - Now install some required pip install  flask, pip install    request, pip install sqlite or for mysql pip install Flask-MSQLdb
 - create a python file 
 - create folder there are two types 1. for templates like html
                                    2 . script
 - In template folder create html files.
 - Come to python file and 
 ------------code-------------
from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

I am writting two code for the given problem 
1. I am connected sqllite that file name is - "app.py"
2. I m connected throw sql throw xammp server in my local host file name - "appsql.py"