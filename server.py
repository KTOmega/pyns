from flask import Flask, render_template, make_response, request
import config
import json
import db
import ns
import validate

app = Flask(__name__)

db.init()

def respond_json(data):
    resp = make_response(json.dumps(data), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.errorhandler(404)
def route_not_found(error):
    return ("wtf are you doing", 404)

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

    if creator == "" or email == "":
        return respond_json({"status": "error", "error": "Missing required fields"})

    if code != "_420_BlazeIt_0_":
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
    return render_template("index.html", data=db.get_all(), zone=config.zone)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
