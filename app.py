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
app.secret_key = json.load(open('victory-222121-ccf57f90d574.json', 'r')).get('project_id', 'qwerty')
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/userLogin', methods=['GET', 'POST'])
def user_login():
    request.form.get('username')
    request.form.get('password')
    if request.method == 'POST':
        user = db.collection('users')
        docs = user.get()
        print(docs)
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

        pbkdf2_sha256.verify(request.form.get('password'), password)


@app.route('/userSignup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        print(request.form)
        user_details = {
            'username': request.form.get('username'),
            'password': pbkdf2_sha256.hash(str(request.form.get('password'))),
            'acc_type': request.form.get('acc_type')
        }
        user = db.collection('users').document(request.form.get('acc_type'))
        user.set(user_details)
    return render_template('index.html')


@app.route('/jobPosting', methods=['GET', 'POST'])
def job_posting():
    pass


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    msg = 'You have been successfully logged out.'
    return redirect(url_for('home', msg=msg))


@app.errorhandler(404)
def page_not_found(e):
    pass


@app.route('/testing')
def testing():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
