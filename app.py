from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, request, session, flash, url_for, redirect, make_response

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
