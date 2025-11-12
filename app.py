from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os



app = Flask(__name__)

# Load environment variables
load_dotenv()

# Connect to MongoDB Atlas
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["student_db"]
collection = db["students"]

@app.route("/submissions")
def show_submissions():
    data = list(collection.find({}, {"_id": 0}))  # exclude MongoDB’s internal _id field
    return jsonify(data)


# --- API Route ---
@app.route("/api")
def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

# --- Form Page ---
@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name")
        course = request.form.get("course")
        try:
            collection.insert_one({"name": name, "course": course})
            return redirect(url_for("success"))
        except Exception as e:
            error_message = str(e)
    return render_template("form.html", error=error_message)

# --- Success Page ---
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
