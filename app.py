import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, request, session, flash, url_for, redirect, make_response


# Use a service account
cred = credentials.Certificate('victory-222121-ccf57f90d574.json')
firebase_admin.initialize_app(cred)

# database connection
db = firestore.client()

# flask connection
app = Flask(__name__)


@app.route('/userLogin', methods=['GET', 'POST'])
def user_login():
    pass


@app.route('/userSignup', methods=['GET', 'POST'])
def user_signup():
    pass


@app.route('/jobPosting', methods=['GET', 'POST'])
def job_posting():
    pass


@app.route('/testing')
def testing():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
