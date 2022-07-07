from flask import Flask, request, abort, jsonify, make_response
from flask_restx import  Resource, fields, Namespace
from main import db
from models import User
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


auth = Namespace('auth', description='name space for authentication')
signup_model = auth.model(
    'Signup_User', {
        'username': fields.String(),
        'email': fields.String(),
        'password': fields.String(),   
    }
)

login_model = auth.model(
    'Login_User', {
        'username': fields.String(),
        'password': fields.String()
    }
)


@auth.route('/signup')
class SignUp(Resource):
    @auth.expect(signup_model)
    def post(self):
        user_data = request.get_json()
        new_user = User(
            username=user_data.get('username'),
            email=user_data.get('email'),
            password= generate_password_hash(user_data.get('password'))
        )
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        response = make_response(jsonify({'message': "congrats, you signed up successfully"}), 201)
        return response

@auth.route('/login')
class Login(Resource):
    @auth.expect(login_model)
    def post(self):
        user_data = request.get_json()
        user = User.query.filter_by(username=user_data['username']).first()
        if user and check_password_hash(user.password, user_data.get('password')):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            
            return make_response(jsonify({'user':user.username,
                            'access_token':access_token,
                            'refresh_token':refresh_token,
                            'message': 'congrats'}), 200)
  
        return abort(status=400)



@auth.route('/refresh')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_username = get_jwt_identity()
        access_token = create_access_token(identity=current_username)
        return make_response(jsonify({'access_token':access_token}), 200)



