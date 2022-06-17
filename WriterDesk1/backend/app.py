from app import db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    '''Functions that should run when shell context is created, database and User model is defined'''
    return{'db': db, 'User': User}
from app import create_app

app = create_app()
