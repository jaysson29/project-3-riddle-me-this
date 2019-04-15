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
        
def add_message(user, number, message):
    write_to_file("data/messages.txt", "({0})-{1}-{2}   \n".format(
            user.title(),
            number,
            message,))
            
def get_all_messages():
    message = []
    with open("data/messages.txt", "r") as chat_messages:
        message = [row for row in chat_messages if len(row.strip()) > 0 ]
    return message
    
@app.route('/', methods=["GET", "POST"])
def index():
    """Main Page"""
    # Get POST request
    if request.method == "POST":
        session["username"] = request.form["user"]
        if session["username"] not in online_users:
            online_users.append(session["username"])
        return redirect('/'+ request.form["user"])
    
    if "username" in session:
        if session["username"] not in online_users:
            online_users.append(session["username"])
        return redirect('/' + session["username"])
        
    return render_template("main.html")
    
@app.route('/<user>', methods=["GET", "POST"])
def username(user):
    """Display chat messages"""
    if "username" not in session:
        return redirect("/")
        
    data = []
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
        
    riddle = 0
    
    
    if request.method == "POST":
        ###write_to_file("data/online_users.txt", user + "\n")###
        riddle = int(request.form["riddle"])
        
        user_response = request.form["message"].lower()
        number = data[riddle]["number"]
        
        if data[riddle]["answer"] == user_response:
            # Correct answer and go to next riddle.
            riddle += 1
        else:
            # Wrong answer
            add_message(user,"riddle:" + str(number) , user_response + "\n")
            
    if request.method == "POST":
        if user_response == "fiiiish" and riddle > 10:
            return render_template("endgame.html")
    
    message = get_all_messages()
    firstL = range(data[riddle]["first"])
    secondL = range(data[riddle]["second"])
    thirdL = range(data[riddle]["third"])
    spaceS = data[riddle]["space"]
    
    return render_template("riddle.html", chat_messages=message, data=data, users=online_users, riddle=riddle, first=firstL, second=secondL, third=thirdL, space=spaceS, username=session["username"])
    
@app.route("/logout")
def logout():
    username = session["username"]
    session.clear()
    if username in online_users:
        online_users.pop(online_users.index(username))
    return redirect("/")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 0)), debug=True)