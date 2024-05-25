from flask import request
from os import path
from pathlib import Path
import subprocess

current_file_name=f"/{path.basename(__file__).replace('.py', '')}"
current_folder=path.dirname(path.abspath(__file__))
codebase_sync_script_path=Path(path.join(current_folder, '../../deploy/sync.sh')).resolve()

def codebase_routes(app, prefix = current_file_name):
    @app.route(path.join(prefix, 'webhook'), methods=['POST'])
    def webhook():
      if request.method == 'POST':
        subprocess.run([codebase_sync_script_path])
        return 'Deploying...', 200
      else:
        return 'Not a valid request', 422
      
      