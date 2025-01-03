from flask import Flask, request, render_template, jsonify
from markupsafe import escape
from datetime import datetime, timedelta, date
import maria_db as db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
import onetimepass as otp
from flask_cors import CORS
from flask_restx import Api, Resource, Namespace, fields, reqparse

app = Flask(__name__)

CORS(app)

app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "TRASYS",
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8),
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
)

jwt = JWTManager(app)

api = Api(
    app,
    version='0.1',
    title='API Doc',
    description='API',
    doc='/api'
)


login_ns = api.namespace(name='login', description='ID/PW 1차인증')
login_input = login_ns.model('login_input', {
    'id': fields.String(description='id', required=True, example='admin'),
    'pw': fields.String(description='pw', required=True, example='!es9830297')})
@login_ns.route('/')
@login_ns.expect(login_input)
class login(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})
        conn = db.dbconnect()
        data = request.get_json()
        id = data["id"]
        pw = data["pw"]
        check = db.login_check(conn, id, pw)
        if check:
            return jsonify({"result": True, "msg": "계정이 확인되었습니다."})
        else:
            return jsonify({"result": False, "msg": "잘못된 계정입니다."})


otp_ns = api.namespace(name='otp', description='OTP 2차인증')
otp_input = otp_ns.model('otp_input', {
    'id': fields.String(description='id', required=True, example='admin'),
    'otp_pw': fields.String(description='otp_pw', required=True, example='123456')})
@otp_ns.route('/')
@otp_ns.expect(otp_input)
class otp_login(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})
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
            return jsonify({"result": False, "msg": "잘못된 번호입니다."})


access_ns = api.namespace(name='access', description='접속기록 조회')
access_input = reqparse.RequestParser()
access_input.add_argument('first', type=str, default=str(date.today()), help='시작일')
access_input.add_argument('last', type=str, default=str(date.today()+timedelta(days=1)), help='끝일')
@access_ns.route("/")
@access_ns.expect(access_input)
class access_history(Resource):
    @jwt_required()
    def get(self):
        conn = db.dbconnect()
        first_date = datetime.strptime(request.args.get("first", str(date.today())), "%Y-%m-%d")
        last_date = datetime.strptime(request.args.get("last", str(date.today()+timedelta(days=1))), "%Y-%m-%d")
        history = db.search_access_history_date(conn, first_date, last_date)
        return jsonify({"result": history})


collect_ns = api.namespace(name='collect', description='위치정보 수집사실 조회')
collect_input = reqparse.RequestParser()
collect_input.add_argument('first', type=str, default=str(date.today()), help='시작일')
collect_input.add_argument('last', type=str, default=str(date.today()+timedelta(days=1)), help='끝일')
@collect_ns.route("/")
@collect_ns.expect(collect_input)
class collect_history(Resource):
    @jwt_required()
    def get(self):
        conn = db.dbconnect()
        first_date = datetime.strptime(request.args.get("first", str(date.today())), "%Y-%m-%d")
        last_date = datetime.strptime(request.args.get("last", str(date.today()+timedelta(days=1))), "%Y-%m-%d")
        history = db.search_collect_history_date(conn, first_date, last_date)
        return jsonify({"result": history})


usage_ns = api.namespace(name='usage', description='위치정보 이용제공사실 조회')
usage_input = reqparse.RequestParser()
usage_input.add_argument('first', type=str, default=str(date.today()), help='시작일')
usage_input.add_argument('last', type=str, default=str(date.today()+timedelta(days=1)), help='끝일')
@usage_ns.route("/")
@usage_ns.expect(usage_input)
class usage_history(Resource):
    @jwt_required()
    def get(self):
        conn = db.dbconnect()
        first_date = datetime.strptime(request.args.get("first", str(date.today())), "%Y-%m-%d")
        last_date = datetime.strptime(request.args.get("last", str(date.today()+timedelta(days=1))), "%Y-%m-%d")
        history = db.search_usage_history_date(conn, first_date, last_date)
        return jsonify({"result": history})


if __name__ == "__main__":
    # app.run()
    app.run('0.0.0.0', port=5000, debug=True)
    