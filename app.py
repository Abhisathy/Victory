import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, request, session, flash, url_for, redirect, make_response

# Use a service account
cred = credentials.Certificate('config.json')
firebase_admin.initialize_app(cred)

# database connection
db = firestore.client()

# flask connection
app = Flask(__name__)
app.secret_key = json.load(open('config.json', 'r')).get('project_id', 'qwerty')
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/userLogin', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        user_ref = db.collection('users').document(request.form.get('email'))
        try:
            user = user_ref.get()
        except Exception:
            err = 'User not found'
            return render_template('login.html', error=err)
        print(user.get('password'))
        if not pbkdf2_sha256.verify(request.form.get('password'), user.get('password')):
            err = 'Password or Username is incorrect.'
            return render_template('login.html', error=err)
        else:
            session['username'] = user.get('email')
            session['acc_type'] = user.get('acc_type')
            session['logged_in'] = True
            print(session)
            msg = 'You have been successfully logged'
            return redirect(url_for('dashboard', msg=msg))
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route('/userSignup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        try:
            user_details = {
                'full_name': request.form.get('full_name'),
                'email': request.form.get('email'),
                'password': pbkdf2_sha256.hash(str(request.form.get('password'))),
                'dob': '{}-{}-{}'.format(request.form.get("dob_mm"),
                                         request.form.get("dob_mm"),
                                         request.form.get("dob_yy")),
                'gender': request.form.get("gender"),
                'street': request.form.get("street"),
                'city':request.form.get("city"),
                'state':request.form.get("state"),
                'zip': request.form.get("zip"),
                'acc_type': request.form.get('acc_type'),
                'about': request.form.get('Highlight'),
                'pay_mode': request.form.get('payment-method'),
                'card_number': pbkdf2_sha256.hash(str(request.form.get('card-number'))),
                'pin': pbkdf2_sha256.hash(str('pin'))
            }
            user = db.collection('users').document(str(request.form.get('email')))
            user.set(user_details)
        except:
            err = "Unsuccessful! Try again"
            return render_template('signup.html', err=err)
        
        session['username'] = str(request.form.get('email'))
        session['acc_type'] = str(request.form.get('acc_type'))
        session['logged_in'] = True
        msg = 'You have been successfully logged'
        return redirect(url_for('dashboard', msg=msg))
    return render_template('signup.html')


@app.route('/jobPosting', methods=['GET', 'POST'])
def job_posting():
    if request.method=='POST':
        job_details = {
            'mem_uploaded':session['username'],
            'title':request.form.get('title'),
            'description':request.form.get('description'),
            'location':request.form.get('location'),
            'url': request.form.get('url')
        }

        jobs = db.collection('jobs').document(request.form.get('title'))
        jobs.set(job_details)
        return render_template('dashboard.html',msg='Job Posted')

        
    return render_template('dashboard.html',msg='Unable to post the job')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    msg = 'You have been successfully logged out.'
    return redirect(url_for('home', msg=msg))


@app.errorhandler(404)
def page_not_found(e):
    return ''


@app.route('/testing')
def testing():
    return ''


if __name__ == "__main__":
<<<<<<< Updated upstream
    app.run(host='0.0.0.0', debug=True)
=======
    app.run(host='0.0.0.0',debug=True)
>>>>>>> Stashed changes
