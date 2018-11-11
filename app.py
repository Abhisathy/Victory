import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, request, session, flash, url_for, redirect, make_response

# Use a service account
cred = credentials.Certificate('victory-222122-8264af68af1c.json')
firebase_admin.initialize_app(cred)

# database connection
db = firestore.client()

# flask connection
app = Flask(__name__)
app.secret_key = json.load(open('victory-222122-8264af68af1c.json', 'r')).get('project_id', 'qwerty')
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('signup.html')


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
            session['doctor'] = True
            session['logged_in'] = True
            msg = 'You have been successfully logged'
            return redirect(url_for('user_login', msg=msg))
    return render_template('login.html')


@app.route('/userSignup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        print(request.form.get('email'))
        user_details = {
            'full_name' : request.form.get('full_name'),
            'email': request.form.get('email'),
            'password': pbkdf2_sha256.hash(str(request.form.get('password'))),
            'dob':'{}-{}-{}'.format(request.form.get("dob_mm"),request.form.get("dob_mm"),request.form.get("dob_yy")),
            'gender':request.form.get("gender"),
            'acc_type': request.form.get('acc_type'),
            'about':request.form.get('Highlight'),
            'pay_mode':request.form.get('payment-method'),
            'card_number':pbkdf2_sha256.hash(str(request.form.get('card-number'))),
            'pin':pbkdf2_sha256.hash(str('pin'))
            
        }

        user = db.collection('users').document(str(request.form.get('email')))
        user.set(user_details)
        session['username'] = user.get('email')
        session['acc_type'] = request.form.get('acc_type')
        session['logged_in'] = True
        msg = 'You have been successfully logged'
        return redirect(url_for('dashboard', msg=msg))

    return render_template('signup.html',message="Unsuccessful! Try again")



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
