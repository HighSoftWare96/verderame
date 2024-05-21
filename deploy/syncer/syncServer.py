from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
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
