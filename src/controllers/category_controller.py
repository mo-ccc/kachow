from main import db
from services import auth_service
import flask_jwt_extended
import flask
from models.Category import Category
from models.Thread import Thread
from schemas.Category_Schema import category_schema, categories_schema
from schemas.Thread_Schema import threads_schema

categories = flask.Blueprint("categories", __name__, url_prefix="/categories")

@categories.route("/", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_categories():
    all_categories = Category.query.all()
    output = categories_schema.dump(all_categories)
    return flask.jsonify(output)

@categories.route("/", methods=["POST"])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def create_category(jwt_user=None):
    response = flask.request.json
    data = category_schema.load(response)
    if jwt_user.role > 1:
        flask.abort(400, description="you do not have the required permissions for this")
    
    new_category = Category()
    new_category.name = data["name"]
    db.session.add(new_category)
    db.session.commit()
    
    return flask.jsonify(category_schema.dump(new_category))
    
@categories.route("/<category_id>", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_category(category_id):   
    category = Category.query.get(category_id)
    dump = category_schema.dump(category)
    threads = Thread.query.filter(Thread.categories.any(category_id=category_id)).all()
    threads_dump = threads_schema.dump(threads)
    output = {"category_info":dump, "threads":threads_dump}
    return flask.jsonify(output)
 
@categories.route("/<category_id>", methods=["PUT", "PATCH"])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def update_category(category_id, jwt_user=None):
    response = flask.request.json
    data = category_schema.load(response)
    if jwt_user.role > 1:
        flask.abort(400, description="you do not have the required permissions for this")
    
    category = Category.query.get(category_id)
    
    category.name = data["name"]
    db.session.commit()
    return flask.jsonify(category_schema.dump(category))
    
@categories.route("/<category_id>", methods=["DELETE"])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def delete_category(category_id, jwt_user=None):
    response = flask.request.json
    data = category_schema.load(response)
    if jwt_user.role > 1:
        flask.abort(400, description="you do not have the required permissions for this")
        
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return flask.jsonify(category_schema.dump(category))