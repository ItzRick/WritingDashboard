#!/bin/sh
flask db upgrade
# If the ADMIN_USERNAME and ADMIN_PASSWORD environment variabels are set, create an admin account:
if ! [ -z "$ADMIN_USERNAME" ] || [ -z "$ADMIN_PASSWORD" ]; then
echo "creating admin"
touch addAdmin.py
cat >> addAdmin.py << EOF
from app import create_app
app = create_app()
from app.models import User
from app import db
with app.app_context():
    u = User(username='${ADMIN_USERNAME}', password_plaintext='${ADMIN_PASSWORD}', role='admin')
    db.session.add(u) 
    db.session.commit()
    print("created admin")
    del app
EOF
python addAdmin.py
rm addAdmin.py
fi
gunicorn -b :5000 --workers=${NUMWORKERS} --threads=${NUMTHREADS} wsgi:app