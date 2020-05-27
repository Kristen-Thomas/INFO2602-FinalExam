#STUDENT ID - 816016203

from main import db, User, Post, UserReact, app

db.create_all(app=app)

bob = User(username="bob", email= "bob@mail.com")
bob.set_password("bobpass")
alice = User(username="alice", email = "alice@mail.com")
alice.set_password("alicepass")
users = [bob.toDict(), alice.toDict()]
db.session.add(bob)
db.session.add(alice)
db.session.commit()
print (users)

print('database initialized!')