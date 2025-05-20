from app import db
from datetime import datetime
import os


class StyleImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_image = db.Column(db.String(255), nullable=False)
    style_image = db.Column(db.String(255), nullable=False)
    result_image = db.Column(db.String(255), nullable=True)
    style_prompt = db.Column(db.String(255), nullable=True)
    style_strength = db.Column(db.Float, default=0.75)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<StyleImage {self.id}>'