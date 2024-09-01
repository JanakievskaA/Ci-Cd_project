from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# Connect to MongoDB using the environment variable
mongo_uri = os.getenv("MONGO_URI", "mongodb://db:27017/tasks")
client = MongoClient(mongo_uri)
db = client["tasks"]
todolist = db.todolist

@app.route("/")
def index():
    all_todolist = list(todolist.find())  # Fetch all documents
    return render_template("index.html", todolist=all_todolist)

@app.route("/add", methods=["POST"])
def add_task():
    task_name = request.form.get("taskname")
    task_time = request.form.get("tasktime")
    todolist.insert_one({"task": task_name, "time": task_time})
    return redirect("/")

@app.route("/delete/<id>")
def delete_task(id):
    todolist.delete_one({"_id": ObjectId(id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
