#STUDENT ID: 816016203

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model): #got this from lab 5
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password":self.password
      }
    
    #hashes the password parameter and stores it in the object
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    #Returns true if the parameter is equal to the object's password property
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    #To String method
    #def __repr__(self):
        #return '<User {}>'.format(self.username)  

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    text = db.Column(db.String(225), nullable=False)
    #reacts = db.Column(db.UserReact, nullable=False)
    reacts = db.relationship('UserReact', backref='userreact', lazy=True)
    
    def getTotalLikes (self):
        numLikes = 0
        for react in self.reacts:
            if react == 'like': 
                numLikes += 1
        return numLikes

    def getTotalDislikes (self):
        numDislikes = 0
        for react in self.reacts:
            if react == 'dislike': 
                numDislikes += 1
        return numDislikes
    
    def toDict(self):
        return{
            "id": self.id,
            "userId": self.userId,
            "text": self.text,
            "reacts": self.reacts,
            "Likes": self.numLikes,
            "Dislikes": self.numDislikes
        }

class UserReact(db.Model):
    #userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    userId = db.Column('userId', db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'), nullable= False)
    react = db.Column(db.String(50), nullable = False)

