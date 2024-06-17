from repositories.DataRepository import DataRepository
from flask import Flask, request, jsonify, redirect,render_template, url_for, flash
from flask_cors import CORS
import secrets
import sys
import os
import threading
import socket
from queue import Queue
from BLE_client import run

# Creating two Queues for communication between threads.
tx_q = None
rx_q = None

targetDeviceName=None
targetDeviceMac="D8:3A:DD:D9:6C:7F"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

app = Flask(__name__)
CORS(app)

app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return redirect("/signup", code=302)


# address to get all customers. (GET method)
@app.route('/users', methods=['GET'])
def users():
    # tx_q.put('   All Users    ')
    users = DataRepository.read_users()
    users.reverse()
    return render_template('users.html', users=users)


@app.route('/signup', methods=['GET'])
def signup():
    tx_q.put('  You need to       Sign up     ')
    return render_template('signup.html')

@app.route('/login/<user_id>', methods=['POST'])
def login(user_id):
    data = DataRepository.is_recorded(user_id)
    is_recorded = data[0]['recorded']

    if is_recorded == 0:
        return redirect(url_for('record_user', user_id=user_id))
    elif is_recorded == 1:
        return redirect(url_for('login_user', user_id=user_id))
    else:
        return redirect(url_for('users'))
    
@app.route('/login/<user_id>', methods=['GET'])
def login_user(user_id):
    data = DataRepository.is_recorded(user_id)
    is_recorded = data[0]['recorded']

    if is_recorded == 0:
        return redirect(url_for('record_user', user_id=user_id))
    elif is_recorded == 1:
        return render_template('login.html', user_id=user_id)
    else:
        return redirect(url_for('users'))

@app.route('/record/<user_id>', methods=['GET'])
def record_user(user_id):
    tx_q.put(f"  Please Enter   Your Password  ")

    return render_template('password.html', user_id=user_id)

is_logged_in = False
@app.route('/auth', methods=['POST'])
def auth_user():
    try:
        global is_logged_in

        tx_q.put('   Look into       the camera   ')

        data = request.get_json()  # Access the JSON data sent by the AJAX request
        user_id = data['userId']  # Extract the user ID

        response = DataRepository.get_name(user_id)

        task_thread = threading.Thread(target=run_task, args=("PREDICT", user_id))
        task_thread.start()

        task_thread.join()

        if not is_logged_in:
            print("Couldn't login")
            tx_q.put(" Couldn't login    Try again    ")
        else:
            honorific = f"{response[0]['honorific']} " if response[0]['honorific'] not in ('', '-') else ''
            tx_q.put(f"Welcome {honorific}{response[0]['firstname']}")

        return jsonify({'message': is_logged_in})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error response with status code

@app.route('/record/<user_id>', methods=['POST'])
def check_password(user_id):
    user_password = request.form['userPassword']
    data = DataRepository.get_password(user_id)

    if user_password == data[0]['password']:
        tx_q.put(f"  Let's record     Your face    ")
        return render_template('record.html', user_id=user_id)
    else:
        tx_q.put(f"   Incorrect        password    ")
        return render_template('password.html', user_id=user_id, error="Incorrect password")


def run_task(task_type, user_id):
    try:
        global is_logged_in
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 65432))
        client.send(f"{task_type} {user_id}".encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        
        if task_type == "PREDICT":
            is_logged_in = response
        
        client.close()
        return is_logged_in
    except Exception as e:
        return f"Exception occurred: {e}"

    
@app.route('/recording', methods=['POST'])
def recording():
    try:
        tx_q.put(f" Please rotate  your face a bit ")

        data = request.get_json()  # Access the JSON data sent by the AJAX request
        user_id = data['userId']  # Extract the user ID

        task_thread = threading.Thread(target=run_task, args=("CAPTURE", user_id))
        task_thread.start()

        task_thread.join()

        return jsonify({'message': 'Ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error response with status code
    
@app.route('/split', methods=['POST'])
def split():
    try:
        tx_q.put(f"Making a dataset")

        data = request.get_json()
        class_name = data['className']
        task_thread = threading.Thread(target=run_task, args=("SPLIT", class_name))

        task_thread.start()

        task_thread.join()

        return jsonify({'message': 'Ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/train', methods=['GET'])
def train():
    try:
        tx_q.put(f"Training a model")

        task_thread = threading.Thread(target=run_task, args=("TRAIN", None))
        task_thread.start()

        task_thread.join()

        return jsonify({'message': 'Ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error response with status code
    
@app.route('/best', methods=['POST'])
def best():
    try:
        tx_q.put(f"  Choosing the     best model   ")

        data = request.get_json()  # Access the JSON data sent by the AJAX request
        user_id = data['userId']  # Extract the user ID

        task_thread = threading.Thread(target=run_task, args=("BEST", user_id))
        task_thread.start()

        task_thread.join()

        DataRepository.set_recorded(user_id)

        flash('trained', 'trained')

        tx_q.put(f"   Model has     been trained!  ")
        
        redirect_url = url_for('users')
        return jsonify({'redirect_url': redirect_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error response with status code
    
# address to ADD a new customer (POST method for your FORM data)
@app.route('/users', methods=['POST'])
def add_user():
    # Use the data_from_form to get the data from the form
    # Use the name attributes from the <input> tags in your form as key
    honorific = request.form.get('honorific', '')
    
    the_new_id = DataRepository.create_user(request.form['userFirstName'], request.form['userLastName'], request.form['userPassword'], request.form['type'], honorific, 0)

    the_new_name = f"{request.form['userFirstName']} {request.form['userLastName']}"
    flash(the_new_name, 'name')
    flash(the_new_id, 'id')

    tx_q.put(f"User {request.form['userFirstName']} added with id {the_new_id}")
    
    return redirect(url_for('users'))

def init_ble_thread():
    # Creating a new thread for running a function 'run' with specified arguments.
    ble_client_thread = threading.Thread(target=run, args=(
        rx_q, tx_q, targetDeviceName, targetDeviceMac), daemon=True)
    # Starting the thread execution.
    ble_client_thread.start()

if __name__ == '__main__':
    tx_q = Queue()
    rx_q = Queue()

    init_ble_thread()

    tx_q.put('   Welcome to       FaceAuth    ')

    app.run(host='127.0.0.1', port=5000, debug=True)
