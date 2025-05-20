from app import create_app, db
from app.auth.models import User
from app.style_transfer.models import StyleImage

app = create_app()

with app.app_context():
    # Create database tables
    db.create_all()
    print("Database initialized!")