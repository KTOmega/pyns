from flask import Flask, render_template, make_response, request, session, url_for
import requests
import config
import json
import db
import ns
import random
import validate

app = Flask(__name__)
app.secret_key = config.secret_key

db.init()

delete_keys = {}

def random_string(length=16):
    alphabet = [chr(i) for i in range(48, 58)] # numbers
    alphabet += [chr(i) for i in range(65, 91)] # capitals
    alphabet += [chr(i) for i in range(97, 123)] # lower-case

    rand = random.SystemRandom()
    out = ""
    for i in range(length):
        out += rand.choice(alphabet)

    return out

def respond_json(data, code=200):
    resp = make_response(json.dumps(data), code)
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/personal/')
def route_personal():
    resp = make_response("", 301)
    resp.headers['Location'] = '/personal/index.html'
    return resp

@app.route('/personal/index.html')
def route_personal_index():
    return render_template('personal.html')

@app.errorhandler(404)
def route_not_found(error):
    return ("I'm not sure what you're trying to find here.", 404)

@app.route('/remove/<name>')
def route_delete(name):
    generic_error = "no"
    if not db.has(name):
        return generic_error
    
    if not name in delete_keys:
        delete_keys[name] = random_string(32)
    
    key = request.args.get('key', '')

    if key == "":
        requests.post(config.slack_webhook, json={
            "text": "Delete {}: {}".format(
                name, 
                "https://{}{}".format(
                    config.zone,
                    url_for('route_delete', name=name, key=delete_keys[name])
                )
                )
            }
        )
        return generic_error

    if delete_keys[name] != key:
        return generic_error

    ret = ns.delete(name)
    
    if not ret:
        return "something bad happened"

    db.delete(name)
    del delete_keys[name]
    return "ok"

@app.route('/add/<name>/<ip>')
def route_add(name, ip):
    if not validate.hostname(name):
        return respond_json({"status": "error", "error": "Invalid hostname, use only alphanumeric characters and dashes"})
    if not validate.ip(ip):
        return respond_json({"status": "error", "error": "Invalid IP address"})

    if db.has(name):
        return respond_json({"status": "error", "error": "Host is already taken"})

    creator = request.args.get('name', '')
    email = request.args.get('email', '')
    code = request.args.get('secret', '')
    nonce_recv = request.args.get('nonce', '')

    if creator == "" or email == "":
        return respond_json({"status": "error", "error": "Missing required fields"})

    if 'nonce' not in session or nonce_recv == "" or session['nonce'] != nonce_recv:
        return respond_json({"status": "error", "error": "Invalid nonce"})

    session.pop('nonce', None)

    if code != config.code:
        return respond_json({"status": "error", "error": "Invalid code"})

    db_entry = {
        "name": creator,
        "email": email,
        "host": name,
        "ip": ip
    }

    ret = ns.add(name, ip)

    if not ret:
        return respond_json({"status": "error", "error": "An unknown error occurred"})

    db.set(name, db_entry)
    return respond_json({"status": "ok"})

@app.route('/')
def main():
    random_nonce = random_string(32)
    session['nonce'] = random_nonce

    return render_template("index.html", data=db.get_all(), zone=config.zone, nonce=random_nonce)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
