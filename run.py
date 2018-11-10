import os
import json
import dj_database_url

from datetime import datetime
from flask import Flask, redirect, render_template, request, flash, jsonify

app = Flask(__name__)
app.secret_key = 'some_secret'
data = []

def write_to_file(filename, data):
    with open(filename, "w") as file:
        file.writelines(data)
        
def add_message(user, message):
    write_to_file("data/users.txt", "({0}) - {1}\n".format(
            user.title(), "w"))
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
    with open("data/users.txt", "r") as user_messages:
        users = user_messages.readlines()
    return users
    
@app.route('/users/online', methods=["GET"])
def online_users():
    online_users_file = open("data/online_users.txt")
    online_users = [row for row in online_users_file if len(row.strip()) > 0]
    online_users_file.close()
    
    return jsonify(online_users)
    
@app.route('/', methods=["GET", "POST"])
def index():
    """Main Page"""
    # Get POST request
    if request.method == "POST":
        write_to_file("data/user.txt", request.form["user"] + "\n")
        write_to_file("data/online_users.txt", request.form["user"] + "\n")
        return redirect(request.form["user"])
    return render_template("main.html")
    
@app.route('/<user>', methods=["GET", "POST"])
def username(user):
    """Display chat messages"""
    data = []
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
        
    riddle = 0
    
    if request.method == "POST":
        write_to_file("data/online_users.txt", user + "\n")
        
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
    
    online_users_file = open("data/online_users.txt")
    online_users = [row for row in online_users_file if len(row.strip()) > 0]
    online_users_file.close()
    
    return render_template("riddle.html", username=user, chat_messages=message, data=data, online_users=online_users, riddle=riddle)
    
@app.route('/players', methods=["GET", "POST"])
def players(user):
    """Display chat historal of players"""
    if request.method == "POST":
        add_users(request.form["user"] + "\n")
    user = get_all_users()
    return render_template("riddle.html", username=user)
    
@app.route('/<user>/<message>')
def send_message(user, message):
    add_message(user, message)
    return redirect(user)
    
@app.route('/<user>/log_off', methods=["POST"])
def log_user_off(user):
    online_users_file = open("data/online_users.txt")
    online_users = [row for row in online_users_file if len(row.strip()) > 0 and row.strip() !=user]
    online_users_file.close()
    
    with open("data/online_users.txt", "w") as online_users_file:
        for user in online_users:
            online_users_file.write('%s\n' % user)
            
    return;
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)