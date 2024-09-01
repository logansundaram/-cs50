import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, jsonify

# Configure application
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///agenda.db")


@app.route("/", methods=["GET", "POST"])
def home():
    agenda = db.execute("SELECT * FROM agenda")
    return render_template("table.html", agenda=agenda)

@app.route("/agenda", methods=["POST"])
def agenda():
    if request.method == "POST":
        """Push new task"""

        if request.is_json:
            try:
                print("isjson")
                data = request.get_json()  # Get the JSON data from the request
                description = data['description']
                day = data['day']
                status = data['status']
                id = data['id']

                # Insert the data into the SQLite database
                db.execute("INSERT INTO agenda (id, description, day, status) VALUES (?, ?, ?, ?)", id, description, day, status)


            except Exception as e:
                return jsonify({"error": str(e)}), 400





        return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        """Push new task"""
        if request.is_json:
            try:
                print("isjson")
                data = request.get_json()  # Get the JSON data from the request
                row = data["count"]

                # Insert the data into the SQLite database
                db.execute("DELETE FROM agenda where id = (?)", row)


            except Exception as e:
                return jsonify({"error": str(e)}), 400

    return redirect("/")


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        """Push new task"""
        if request.is_json:
            try:
                print("isjson")
                data = request.get_json()  # Get the JSON data from the request
                row = data["count"]
                status = data["status"]

                # Insert the data into the SQLite database
                db.execute("UPDATE agenda SET status = (?) WHERE id = (?)", status, row)


            except Exception as e:
                return jsonify({"error": str(e)}), 400

    return redirect("/")

