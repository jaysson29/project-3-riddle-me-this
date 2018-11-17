import os
import json
import dj_database_url

from datetime import datetime
from flask import Flask, redirect, render_template, request, flash, jsonify, session

app = Flask(__name__)
app.secret_key = 'some_secret'
data = []
online_users = []

def write_to_file(filename, data):
    with open(filename, "a") as file:
        file.writelines(data)
        
def add_message(user, message):
    write_to_file("data/messages.txt", "({0}) - {1}\n".format(
            user.title(),
            message))
            
def get_all_messages():
    message = []
    with open("data/messages.txt", "r") as chat_messages:
        message = [row for row in chat_messages if len(row.strip()) > 0 ]
    return message
    
def add_users(user):
    write_to_file("data/user.txt", "({0}) - {1}\n".format(
        user.title(), user.title))
        
def get_all_users():
    users = []
    with open("data/user.txt", "r") as user_messages:
        users = user_messages.readlines()
    return users
    
    
@app.route('/', methods=["GET", "POST"])
def index():
    """Main Page"""
    # Get POST request
    if request.method == "POST":
        session["user"] = request.form["user"]
        online_users.append(request.form["user"])
        return redirect(request.form["user"])
        
    if "user" in session:
        if session["user"] not in online_users:
            online_users.append(session["user"])
        
        return redirect(request.form["user"])
        
    return render_template("main.html")
    
@app.route('/<user>', methods=["GET", "POST"])
def username(user):
    """Display chat messages"""
    if "user" not in session:
        return redirect("/")
        
    data = []
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
        
    riddle = 0
    
    if request.method == "POST":
        ###write_to_file("data/online_users.txt", user + "\n")###
        riddle = int(request.form["riddle"])
        
        user_response = request.form["message"].lower()
        
        if data[riddle]["answer"] == user_response:
            # Correct answer and go to next riddle.
            riddle += 1
        else:
            # Wrong answer
            add_message(user, user_response + "\n")
            
    if request.method == "POST":
        if user_response == "fiiiish" and riddle > 10:
            return render_template("endgame.html")
    
    message = get_all_messages()
    
    return render_template("riddle.html", chat_messages=message, data=data, users=online_users, riddle=riddle, user=session["user"])
    
@app.route('/players', methods=["GET", "POST"])
def players(user):
    """Display chat historal of players"""
    if request.method == "POST":
        add_users(request.form["user"] + "\n")
    user = get_all_users()
    return render_template("riddle.html", user=user)
    
@app.route("/logout")
def logout():
    user = session["user"]
    session.clear()
    if user in online_users:
        online_users.pop(online_users.index(user))
    return redirect("/")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)