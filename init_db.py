from app import create_app
from app import db
app = create_app()

# This script initializes the database and creates the necessary tables.    
with app.app_context():
    db.create_all()
    print("Database initialized and tables created.")