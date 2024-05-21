from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
import subprocess
from os import path

current_folder=path.dirname(path.abspath(__file__))
sync_path=path.join(current_folder, 'sync.sh')

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        subprocess.run([sync_path])
        return 'Deploying...', 200
    else:
        return 'Not a valid request', 422

if __name__ == '__main__':
    port = 5000
    app.run(host='127.0.0.1', port=(port))
    print(f"Server running on port {port}")
