import datetime
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = 'bilka'


# Load users from the JSON file
def load_users():
    with open('clients.json', 'r') as f:
        return json.load(f)

users = load_users()
user_cookies = {}

# Define the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='This field is required')])
    password = PasswordField('Password', validators=[
        DataRequired(message='This field is required'),
        Length(min=4, max=10, message='Password must be between 4 and 10 characters')
    ])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

# Define the change password form
class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(message='This field is required')])
    submit = SubmitField('Change Password')

# Define the add cookie form
class AddCookieForm(FlaskForm):
    cookie_key = StringField('Key', validators=[DataRequired(message='This field is required')])
    cookie_value = StringField('Value', validators=[DataRequired(message='This field is required')])
    cookie_expiry = IntegerField('Expiry (seconds)', validators=[DataRequired(message='This field is required')])
    submit = SubmitField('Add Cookie')

# Define the delete cookie form
class DeleteCookieForm(FlaskForm):
    delete_cookie_key = StringField('Key to Delete', validators=[DataRequired(message='This field is required')])
    submit = SubmitField('Delete Cookie')

# Define the delete all cookies form
class DeleteAllCookiesForm(FlaskForm):
    submit = SubmitField('Delete All Cookies')

# Define the index route
@app.route('/')
def index():
    return redirect(url_for('login'))

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and users[username]['password'] == password:
            session['username'] = username
            if form.remember.data:
                session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('info'))
        else:
            flash('User does not exist or incorrect password', 'danger')

    return render_template('login.html', form=form)

# Define the info route
@app.route('/info', methods=['GET', 'POST'])
def info():
    username = session.get('username', None)
    add_cookie_form = AddCookieForm()
    delete_cookie_form = DeleteCookieForm()
    delete_all_cookies_form = DeleteAllCookiesForm()
    change_password_form = ChangePasswordForm()

    if username:
        user_info = users.get(username, None)
        if user_info:
            cookies = get_user_cookies()
            return render_template('info.html', user_info=user_info, cookies=cookies,
                                   add_cookie_form=add_cookie_form,
                                   delete_cookie_form=delete_cookie_form,
                                   delete_all_cookies_form=delete_all_cookies_form,
                                   change_password_form=change_password_form)
    return redirect(url_for('login'))

# Define the logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('message', None)
    user_cookies.clear()
    return redirect(url_for('login'))

# Define the add cookie route
@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    form = AddCookieForm(request.form)
    if form.validate():
        username = session.get('username', None)
        if username:
            key = form.cookie_key.data
            value = form.cookie_value.data
            expiry = int(form.cookie_expiry.data)
            user_cookies[key] = {"value": value, "expiry": expiry, "creation_time": str(datetime.datetime.now())}
            flash(f"Cookie '{key}' added successfully.", 'success')
    return redirect(url_for('info'))

# Define the delete cookie route
@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    form = DeleteCookieForm(request.form)
    if form.validate():
        username = session.get('username', None)
        if username:
            key = form.delete_cookie_key.data
            if key in user_cookies:
                user_cookies.pop(key)
                flash (f"Cookie '{key}' deleted successfully.", 'success')
                
    return redirect(url_for('info'))

# Define the delete all cookies route
@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    username = session.get('username', None)
    if username:
        user_cookies.clear()
        flash("All cookies deleted successfully.", 'success')
    return redirect(url_for('info'))

# Define a helper function to get user cookies
def get_user_cookies():
    cookies_list = []
    for key, cookie in user_cookies.items():
        expiry_time = datetime.datetime.strptime(cookie['creation_time'], '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(
            seconds=cookie['expiry'])
        cookies_list.append({
            'key': key,
            'value': cookie['value'],
            'expiry': expiry_time,
            'creation_time': cookie['creation_time']
        })
    return cookies_list

# Define the change password route
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        username = session.get('username', None)
        if username:
            new_password = form.new_password.data
            if new_password:
                change_user_password(username, new_password)
                flash("Password changed successfully.", 'success')
    return redirect(url_for('info'))

# Define a helper function to change user password
def change_user_password(username, new_password):
    with open('clients.json', 'r+') as f:
        users = json.load(f)
        if username in users:
            users[username]['password'] = new_password
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
