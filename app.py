import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "beauty-parlour-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///beauty_parlour.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize SQLAlchemy with custom base
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Import models and create tables inside app context
with app.app_context():
    import models  # make sure this file defines Inquiry model
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    service_categories = [
        {
            'name': 'Nail Art & Manicure',
            'description': 'Creative nail designs, gel manicures, and nail care treatments',
            'services': ['Gel Manicure', 'Nail Art Design', 'French Manicure', 'Nail Extensions', 'Nail Care Treatment'],
            'image': 'https://media.istockphoto.com/id/1334253013/photo/close-up-manicured-womans-hands-on-pink-background.jpg?s=2048x2048&w=is&k=20&c=WXqqd-gCtae5XgZuAtcLvY2gXbfJ7sCjgxWVbQnrfNU='
        },
        {
            'name': 'Makeup Artistry',
            'description': 'Professional makeup for all occasions and events',
            'services': ['Bridal Makeup', 'Party Makeup', 'Corporate Look', 'Photo Shoot Makeup', 'Makeup Lessons'],
            'image': 'https://media.istockphoto.com/id/1014165094/photo/portrait-of-a-woman-with-bright-colored-flying-hair-all-shades-of-purple-hair-coloring.jpg?s=2048x2048&w=is&k=20&c=dQjErMkgUkX7NY-5WhCJCkdmD8n7C9dV_9VuXneghzg='
        },
        {
            'name': 'Facial Treatments',
            'description': 'Rejuvenating facial treatments for all skin types',
            'services': ['Deep Cleansing Facial', 'Anti-Aging Treatment', 'Hydrating Facial', 'Acne Treatment', 'Brightening Facial'],
            'image': 'https://media.istockphoto.com/id/1255188868/photo/spa-therapist-putting-facial-mask-for-young-lady.jpg?s=2048x2048&w=is&k=20&c=QmF02de7ZAXi7Va0Y03v-r2GT6gUxSSzyJLxTs3cXSI='
        },
        {
            'name': 'Hair Styling',
            'description': 'Professional hair styling and treatments',
            'services': ['Hair Cut & Style', 'Hair Coloring', 'Hair Treatment', 'Bridal Hair', 'Hair Extensions'],
            'image': 'https://media.istockphoto.com/id/539953380/photo/girl-with-red-lipstick-and-short-hair-in-black-t-shirt.jpg?s=2048x2048&w=is&k=20&c=sKfyK8csXYbdIguASF3X2uFtFTAdoQ_XeygX1cSIFF0='
        }
    ]
    return render_template('services.html', service_categories=service_categories)

@app.route('/portfolio')
def portfolio():
    portfolio_items = [
        {'category': 'makeup', 'image': 'https://media.istockphoto.com/id/1334253013/photo/close-up-manicured-womans-hands-on-pink-background.jpg?s=2048x2048&w=is&k=20&c=WXqqd-gCtae5XgZuAtcLvY2gXbfJ7sCjgxWVbQnrfNU=', 'title': 'Bridal Makeup'},
        {'category': 'makeup', 'image': 'https://media.istockphoto.com/id/1014165094/photo/portrait-of-a-woman-with-bright-colored-flying-hair-all-shades-of-purple-hair-coloring.jpg?s=2048x2048&w=is&k=20&c=dQjErMkgUkX7NY-5WhCJCkdmD8n7C9dV_9VuXneghzg=', 'title': 'Evening Look'},
        {'category': 'makeup', 'image': 'https://media.istockphoto.com/id/1255188868/photo/spa-therapist-putting-facial-mask-for-young-lady.jpg?s=2048x2048&w=is&k=20&c=QmF02de7ZAXi7Va0Y03v-r2GT6gUxSSzyJLxTs3cXSI=', 'title': 'Natural Glow'},
        {'category': 'nails', 'image': 'https://https://media.istockphoto.com/id/539953380/photo/girl-with-red-lipstick-and-short-hair-in-black-t-shirt.jpg?s=2048x2048&w=is&k=20&c=sKfyK8csXYbdIguASF3X2uFtFTAdoQ_XeygX1cSIFF0=', 'title': 'Floral Nail Art'},
        {'category': 'nails', 'image': 'https://media.istockphoto.com/id/1493895602/photo/stage-kids-cute-sweet-dreams-podium-pink-playground-rainbow-circle-float-and-circle-wall.jpg?s=2048x2048&w=is&k=20&c=ZPjduA6EW7QuZrSfsR9-aROTt8AWHnZ7mJgw-s1bC4k=', 'title': 'French Manicure'},
        {'category': 'nails', 'image': 'https://media.istockphoto.com/id/1296431297/photo/a-beautiful-young-woman-with-long-hair-doing-makeup-for-a-wedding-or-photo-shoot.jpg?s=2048x2048&w=is&k=20&c=4vNafslyu33WucWPvZnD3_TPOZjdlENf7WQgMHkAsFs=', 'title': 'Geometric Design'}
    ]
    return render_template('portfolio.html', portfolio_items=portfolio_items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')

        if name and email and message:
            from models import Inquiry  # Import inside route to avoid circular import
            inquiry = Inquiry(name=name, email=email, phone=phone, service=service, message=message)
            db.session.add(inquiry)
            db.session.commit()

            flash('Thank you for your inquiry! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all required fields.', 'error')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
