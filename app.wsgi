import os
import sys

PROJECT_DIR = os.path.dirname(__file__)

venv_activate = os.path.join(PROJECT_DIR, 'venv', 'bin', 'activate_this.py')

with open(venv_activate, 'r') as activator:
        exec(activator.read(), dict(__file__=venv_activate))

sys.path.append(PROJECT_DIR)

import server

application = server.app

