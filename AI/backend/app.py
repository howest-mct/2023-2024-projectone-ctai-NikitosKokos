from repositories.DataRepository import DataRepository
from flask import Flask, request, jsonify, redirect,render_template, url_for, flash, session
from flask_cors import CORS
import secrets

app = Flask(__name__)
CORS(app)

app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return redirect("/signup", code=302)


# address to get all customers. (GET method)
@app.route('/users', methods=['GET'])
def users():
    users = DataRepository.read_users()
    return render_template('users.html', users=users)


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')
    
# address to ADD a new customer (POST method for your FORM data)
@app.route('/users', methods=['POST'])
def add_user():
    # Use the data_from_form to get the data from the form
    # Use the name attributes from the <input> tags in your form as key
    print(request.form.get('honorific', ''), 'honorific')
    honorific = request.form.get('honorific', '')
    print(honorific)
    users = DataRepository.read_users()
    the_new_id = DataRepository.create_user(request.form['userFirstName'], request.form['userLastName'], request.form['userPassword'], request.form['type'], honorific)
    # the_new_name = f"{request.form['userFirstName']} {request.form['userLastName']}"
    # return render_template('users.html', the_new_id=the_new_id, the_new_name=the_new_name, users=users)

    the_new_name = f"{request.form['userFirstName']} {request.form['userLastName']}"
    flash(f'User {the_new_name} has been successfully added with the id {the_new_id}!', 'success')

    return redirect(url_for('users'))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
