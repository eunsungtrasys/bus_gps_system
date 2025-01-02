from flask import Flask, request, render_template, jsonify
from markupsafe import escape
from datetime import datetime, timedelta, date
import maria_db as db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
import onetimepass as otp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "TRASYS",
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8),
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
)

jwt = JWTManager(app)

@app.route("/login", methods = ["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    conn = db.dbconnect()
    data = request.get_json()
    id = data["id"]
    pw = data["pw"]
    check = db.login_check(conn, id, pw)
    if check:
        return jsonify({"result": True, "msg": "계정이 확인되었습니다."})
    else:
        return jsonify({"result": False, "msg": "잘못된 계정입니다."}), 401

@app.route("/otp", methods = ["POST"])
def otp_login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    conn = db.dbconnect()
    data = request.get_json()
    id = data["id"]
    pw = data["otp_pw"]
    secret_key = 'TRASYSABCDEFGHIJKLMNOPQRSTUVWXYZ'
    check = otp.valid_totp(pw, secret_key)
    if check:
        user_data = db.search_user(conn, id)
        client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        db.insert_access_history(conn, user_data[0][0], client_ip, datetime.now(), user_data[0][3])
        token = create_access_token(identity=id)
        return jsonify({"result": True, "access_token": token})
    else:
        return jsonify({"result": False, "msg": "잘못된 번호입니다."}), 401

@app.route("/access", methods = ["GET"])
@jwt_required()
def access_history():
    conn = db.dbconnect()
    first_date = datetime.strptime(request.args.get("first", str(date.today())), "%Y-%m-%d")
    last_date = datetime.strptime(request.args.get("last", str(date.today()+timedelta(days=1))), "%Y-%m-%d")
    history = db.search_access_history_date(conn, first_date, last_date)
    return jsonify({"result": history})

@app.route("/collect", methods = ["GET"])
@jwt_required()
def collect_history():
    conn = db.dbconnect()
    first_date = datetime.strptime(request.args.get("first", str(date.today())), "%Y-%m-%d")
    last_date = datetime.strptime(request.args.get("last", str(date.today()+timedelta(days=1))), "%Y-%m-%d")
    history = db.search_collect_history_date(conn, first_date, last_date)
    return jsonify({"result": history})

@app.route("/usage", methods = ["GET"])
@jwt_required()
def usage_history():
    conn = db.dbconnect()
    first_date = datetime.strptime(request.args.get("first", str(date.today())), "%Y-%m-%d")
    last_date = datetime.strptime(request.args.get("last", str(date.today()+timedelta(days=1))), "%Y-%m-%d")
    history = db.search_usage_history_date(conn, first_date, last_date)
    return jsonify({"result": history})


if __name__ == "__main__":
    # app.run()
    app.run('0.0.0.0', port=5000, debug=True)
    