from unicodedata import name
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_jwt_extended import jwt_required
from main import db
from models import Recipe

recipe = Namespace('recipe', description='namespace for recipes')



reciepe_models = recipe.model(
    'Reciepe',{
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String()
    }
)


@recipe.route('/hello')
class Hello(Resource):
    def get(self):
        return {'message': 'How are you Muhammad Nasr'}

@recipe.route('/recipes')
class ReciepesResources(Resource):
    @recipe.marshal_list_with(reciepe_models)
    def get(self):
        """ return all reciepes"""
        all_reciepes = Recipe.query.all()
        return all_reciepes
   
      
    @recipe.marshal_with(reciepe_models)
    #@jwt_required()
    def post(self):
        data = request.get_json()
        new_reciepe = Recipe(
            title=data.get('title'),
            description=data.get('description')
        )
        db.session.add(new_reciepe)
        db.session.commit()
        return data, 201


@recipe.route('/recipe/<id>')
class ReciepeResource(Resource):
    @recipe.marshal_with(reciepe_models)
    @jwt_required()
    def get(self, id):
        """return specific reciepe by id"""
        reciepe = Recipe.query.get(id)
        return reciepe

    @recipe.marshal_with(reciepe_models)
    @jwt_required()
    def put(self, id):
        reciepe = Recipe.query.get(id)
        print(id)
        data = request.get_json()
        reciepe.title = data.get('title')
        reciepe.description = data.get('description')
        db.session.commit()
        return reciepe



    @recipe.marshal_with(reciepe_models)
    #@jwt_required()
    def delete(self, id):
        reciepe = Recipe.query.get(id)
        db.session.delete(reciepe)
        db.session.commit()
        return jsonify({'message', 'delete successfully'})