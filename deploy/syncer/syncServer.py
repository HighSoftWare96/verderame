from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import os
import subprocess

app = Flask(__name__)
auth = HTTPBasicAuth()
user = { "$$admin": os.environ["USER_PASSWORD"] }

@auth.verify_password
def basic(username, password):
    if username in user and user[username] == password:
        return username


@app.route('/webhook', methods=['POST'])
@auth.login_required
def webhook():
    if request.method == 'POST':
        subprocess.run(["./sync.sh"])
        return 'Deploying...', 200
    else:
        return 'Not a valid request', 422

if __name__ == '__main__':
    port = 5000
    app.run(host='127.0.0.1', port=(port))
    print(f"Server running on port {port}")
