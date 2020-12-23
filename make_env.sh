python3 -m venv env
source env/bin/activate
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=80
