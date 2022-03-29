"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'somesecret'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Renders home page"""

    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns data about all cupcakes"""

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns data about a specific cupcake
    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}"""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a new cupcake and return data about new cupcake
       Return JSON like:
       {cupcake: [{id, flavor, rating, size, image}]}"""

    data = request.json

    new_cupcake = Cupcake(
            flavor=data["flavor"], 
            size=data["size"], 
            rating=data["rating"], 
            image=data["image"] or None
            )

    db.session.add(new_cupcake)  
    db.session.commit()   
    response_json = jsonify(cupcake=new_cupcake.serialize()) 

    # POST requests should return HTTP status of 201 CREATED
    return (response_json, 201) 


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update an existing cupcake from data in request and return updated data
    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}"""

    data = request.json
    cupcake = Cupcake.query.get_or_404(id)
    # get updated properties or original if no change
    cupcake.flavor = data.get("flavor", cupcake.flavor) 
    cupcake.size = data.get("size", cupcake.size)
    cupcake.rating = data.get("rating", cupcake.rating) 
    cupcake.image = data.get("image", cupcake.image)
  
    db.session.add(cupcake)
    db.session.commit()   

    return jsonify(cupcake=cupcake.serialize()) 


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete existing cupcake and return confirmation message.
    Returns JSON of {message: "Deleted}"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")