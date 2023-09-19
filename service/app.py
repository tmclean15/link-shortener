from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import shortuuid
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000"])

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "shortenerdb")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(100), nullable=False, unique=True)

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_code = shortuuid.ShortUUID().random(length=6)
    new_link = Link(original_url=original_url, short_url=short_code)
    db.session.add(new_link)
    db.session.commit()
    return jsonify({'short_url': f"{request.url_root}{short_code}"}), 200

@app.route('/<short_code>')
def redirect_to_original(short_code):
    link = Link.query.filter_by(short_url=short_code).first()
    if link:
        return redirect(link.original_url)
    return "URL not found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
