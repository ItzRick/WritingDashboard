from app import app
from werkzeug.security import generate_password_hash

def signUp(data):

    hash = generate_password_hash('foobar')
    
    print("")
