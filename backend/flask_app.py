from flask import Flask, request, render_template, jsonify
from markupsafe import escape
from datetime import datetime, timedelta, date
import postgresql as db
from mariadb import *
from flask_jwt_extended import *
from flask_jwt_extended.exceptions import *
import onetimepass as otp
from flask_cors import CORS
from flask_restx import Api, Resource, Namespace, fields, reqparse
from flask_request_validator import *
from flask_request_validator.exceptions import * 
from werkzeug.exceptions import *

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
@login_ns.route('')
@login_ns.expect(login_input)
class login(Resource):
    @validate_params(
        Param('id', JSON, str),
        Param('pw', JSON, str)
    )
    def post(self, valid: ValidRequest):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})
        conn = db.dbconnect()
        data = valid.get_json()
        id = data["id"]
        pw = data["pw"]
        check = db.login_check(conn, id, pw)
        if check:
            return jsonify({"result": True, "msg": "계정이 확인되었습니다."})
        else:
            return jsonify({"result": False, "msg": "잘못된 계정입니다."}), 401


otp_ns = api.namespace(name='otp', description='OTP 2차인증')
otp_input = otp_ns.model('otp_input', {
    'id': fields.String(description='id', required=True, example='admin'),
    'otp_pw': fields.String(description='otp_pw', required=True, example='123456')})
@otp_ns.route('')
@otp_ns.expect(otp_input)
class otp_login(Resource):
    @validate_params(
        Param('id', JSON, str),
        Param('otp_pw', JSON, str)
    )
    def post(self, valid:ValidRequest):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})
        conn = db.dbconnect()
        data = valid.get_json()
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


access_ns = api.namespace(name='access', description='접속기록 조회')
access_input = reqparse.RequestParser()
access_input.add_argument('first', type=str, default=str(date.today()), help='시작일')
access_input.add_argument('last', type=str, default=str(date.today()+timedelta(days=1)), help='끝일')
@access_ns.route("")
@access_ns.expect(access_input)
class access_history(Resource):
    @jwt_required()
    def get(self):
        conn = db.dbconnect()
        
        first_date_str = request.args.get("first", str(date.today()))
        last_date_str = request.args.get("last", str(date.today() + timedelta(days=1)))
        
        first_date = datetime.strptime(first_date_str, "%Y-%m-%d")
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")

        history = db.search_access_history_date(conn, first_date, last_date)
        return jsonify({"result": history})


collect_ns = api.namespace(name='collect', description='위치정보 수집사실 조회')
collect_input = reqparse.RequestParser()
collect_input.add_argument('first', type=str, default=str(date.today()), help='시작일')
collect_input.add_argument('last', type=str, default=str(date.today()+timedelta(days=1)), help='끝일')
@collect_ns.route("")
@collect_ns.expect(collect_input)
class collect_history(Resource):
    @jwt_required()
    def get(self):
        conn = db.dbconnect()
        
        first_date_str = request.args.get("first", str(date.today()))
        last_date_str = request.args.get("last", str(date.today() + timedelta(days=1)))
        
        first_date = datetime.strptime(first_date_str, "%Y-%m-%d")
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")

        history = db.search_collect_history_date(conn, first_date, last_date)
        return jsonify({"result": history})


usage_ns = api.namespace(name='usage', description='위치정보 이용제공사실 조회')
usage_input = reqparse.RequestParser()
usage_input.add_argument('first', type=str, default=str(date.today()), help='시작일')
usage_input.add_argument('last', type=str, default=str(date.today()+timedelta(days=1)), help='끝일')
@usage_ns.route("")
@usage_ns.expect(usage_input)
class usage_history(Resource):
    @jwt_required()
    def get(self):
        conn = db.dbconnect()
        
        first_date_str = request.args.get("first", str(date.today()))
        last_date_str = request.args.get("last", str(date.today() + timedelta(days=1)))
        
        first_date = datetime.strptime(first_date_str, "%Y-%m-%d")
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")

        history = db.search_usage_history_date(conn, first_date, last_date)
        return jsonify({"result": history})



@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description
    }).get_data(as_text=True)
    response.content_type = "application/json"
    return response, e.code

@app.errorhandler(Exception)
def handle_generic_exception(e):
    return jsonify({
        "code": 500,
        "name": "Internal Server Error",
        "description": str(e)
    }), 500

@app.errorhandler(RequestError)
def handle_validation_exception(e):
    return jsonify({
        "code": 400,
        "name": "Validation Error",
        "description": str(e)
    }), 400

@app.errorhandler(NoAuthorizationError)
def handle_no_auth_error(e):
    return jsonify({
        "code": 401,
        "name": "Authorization Error",
        "description": "Authorization token is missing or invalid."
    }), 401

@app.errorhandler(JWTDecodeError)
def handle_jwt_decode_error(e):
    return jsonify({
        "code": 401,
        "name": "JWT Decode Error",
        "description": "The token is invalid or malformed."
    }), 401

@app.errorhandler(RevokedTokenError)
def handle_revoked_token_error(e):
    return jsonify({
        "code": 401,
        "name": "Revoked Token",
        "description": "This token has been revoked and cannot be used."
    }), 401

@app.errorhandler(FreshTokenRequired)
def handle_fresh_token_required(e):
    return jsonify({
        "code": 401,
        "name": "Fresh Token Required",
        "description": "A fresh token is required to access this resource."
    }), 401
    
@app.errorhandler(DatabaseError)
def handle_database_error(e):
    return jsonify({
        "code": 500,
        "name": "Database Error",
        "description": "An error occurred while accessing the database. Please try again later."
    }), 500

@app.errorhandler(ValueError)
def handle_value_error(e):
    description = str(e)
    if "OTP" in description:
        name = "OTP Validation Error"
        message = "Invalid OTP code provided. Please try again."
    elif "date" in description:
        name = "Date Format Error"
        message = "The provided date format is invalid."
    else:
        name = "Value Error"
        message = description

    return jsonify({
        "code": 400,
        "name": name,
        "description": message
    }), 400

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({
        "code": 400,
        "name": "Bad Request",
        "description": "The request is invalid or missing required parameters."
    }), 400

@app.errorhandler(401)
def handle_unauthorized_error(e):
    return jsonify({
        "code": 401,
        "name": "Unauthorized",
        "description": "The ID or password is incorrect."
    }), 401
    
@app.errorhandler(403)
def handle_cors_error(e):
    return jsonify({
        "code": 403,
        "name": "CORS Error",
        "description": "Cross-Origin Request Blocked. Check your CORS configuration."
    }), 403

@app.errorhandler(404)
def handle_not_found(e):
    return jsonify({
        "code": 404,
        "name": "Not Found",
        "description": "The requested resource was not found on this server."
    }), 404

@app.errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({
        "code": 500,
        "name": "Internal Server Error",
        "description": "An unexpected error occurred. Please try again later."
    }), 500



if __name__ == "__main__":
    app.run('0.0.0.0', port=4000, debug=True)
    