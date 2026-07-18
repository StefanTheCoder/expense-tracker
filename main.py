from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

firebase_creds = json.loads(os.environ["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/")
def index():
    docs = db.collection("expenses").stream()
    expenses = [doc.to_dict() for doc in docs]
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    category = request.form["category"]
    note = request.form.get("note", "")

    db.collection("expenses").document().set({
        "amount": amount,
        "category": category,
        "note": note,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)