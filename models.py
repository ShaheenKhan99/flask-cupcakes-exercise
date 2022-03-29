"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to Flask App"""

    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """Cupcake model"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)


    def serialize(self):
        """Returns a dictionary representation of a single cupcake"""

        return {
          'id': self.id,
          'flavor': self.flavor,
          'size': self.size,
          'rating': self.rating,
          'image': self.image
        }

    def __repr__(self):
        return f"<Cupcake {self.id} flavor={self.flavor} size={self.size} rating={self.rating} image={self.image}>"

