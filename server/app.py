#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        q = Camper.query.all()
        
        camper_dict = [camper.to_dict(only=('id', 'name', 'age')) for camper in q]

        response = make_response(camper_dict, 200)
        return response
    
    def post(self):
       data = request.get_json()

       try:
            
            new_camper = Camper(
                name = data.get('name'),
                age = data.get('age')
                
            )
        
            db.session.add(new_camper)
            db.session.commit()
       except:
           return make_response({"errors": "validation errors"}, 400)
           
           
       
       response = make_response(new_camper.to_dict(), 201)

       return response




api.add_resource(Campers, '/campers')

class OneCamper(Resource):
    def get(self, id):

        q = Camper.query.filter(Camper.id==id).first()

        if not q:
            return make_response({'error': 'Camper not found'}, 404)
        
        response = make_response(q.to_dict(), 200)
        return response
    
    def patch(self, id):
        q = Camper.query.filter(Camper.id==id).first()

        if not q:
            return make_response({'error': 'Camper not found'}, 404)
        
        data = request.get_json()
        try:

            for attr in data:
                setattr(q, attr, data.get(attr))

        
                db.session.add(q)
                db.session.commit()
        except:
            return make_response({"errors": ["validation errors"]},400)



        response = make_response(q.to_dict(), 202)

        return response

    
api.add_resource(OneCamper, '/campers/<int:id>')

class Activities(Resource):
   def get(self):
        q = Activity.query.all()
        
        activity_dict = [activity.to_dict(only=('id', 'name', 'difficulty')) for activity in q]

        response = make_response(activity_dict, 200)
        return response
   
api.add_resource(Activities, '/activities')

class ActivityByID(Resource):
    def delete(self,id ):
        q = Activity.query.filter(Activity.id==id).first()

        if not q:
            return make_response({'error': 'Activity not found'}, 404)
       
        db.session.delete(q)
        db.session.commit()
    

        return make_response({}, 204)
    
api.add_resource(ActivityByID, '/activities/<int:id>')


class SignUps(Resource):

    def post(self):
        data = request.get_json()
        
        try:   
            new_signup = Signup(
                camper_id = data.get('camper_id'),
                activity_id = data.get('activity_id'),
                time = data.get('time')
            
        )

        
            db.session.add(new_signup)
            db.session.commit()

        except:
            return make_response({"errors": ["validation errors"]}, 400)

            
       
        response = make_response(new_signup.to_dict(), 201)

        return response
api.add_resource(SignUps, '/signups')
  
      

if __name__ == '__main__':
    app.run(port=5555, debug=True)
