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
            'image': 'https://pixabay.com/get/gcbc6538a81cc7d4f4f0434ede2165e0eac2ce9e6c9ef38855ff1b1223b43ae9c8ad7e856db7d79ed6f885f1d3396c233a57067034f8f8e5e7a47f99fd1818fa6_1280.jpg'
        },
        {
            'name': 'Makeup Artistry',
            'description': 'Professional makeup for all occasions and events',
            'services': ['Bridal Makeup', 'Party Makeup', 'Corporate Look', 'Photo Shoot Makeup', 'Makeup Lessons'],
            'image': 'https://pixabay.com/get/ge393c8473f81869d31fc2c32b114f9473c65dfedd3cec9729339191b980cb5e3a24a56857fa002d910f7d0e82cad5bb0e486570955c3ede37dfe616e41895f0f_1280.jpg'
        },
        {
            'name': 'Facial Treatments',
            'description': 'Rejuvenating facial treatments for all skin types',
            'services': ['Deep Cleansing Facial', 'Anti-Aging Treatment', 'Hydrating Facial', 'Acne Treatment', 'Brightening Facial'],
            'image': 'https://pixabay.com/get/gbde627d5e095e1015b5e0aa8794b3576c2ef0a63311b2ae6203c00122124879ae8a0fd147b21c3a8c940677cc562162229bb29c4afcca67edf4e88a2b7bd5608_1280.jpg'
        },
        {
            'name': 'Hair Styling',
            'description': 'Professional hair styling and treatments',
            'services': ['Hair Cut & Style', 'Hair Coloring', 'Hair Treatment', 'Bridal Hair', 'Hair Extensions'],
            'image': 'https://pixabay.com/get/gd9504a0878d78ad700cd78b9e6b4e94b047bfa82d2b1084274f4533b2b3f2be4c0fce86c24b663061612d41df7e65dad9e0ae019f06d956e11d5f8e42eefac4d_1280.jpg'
        }
    ]
    return render_template('services.html', service_categories=service_categories)

@app.route('/portfolio')
def portfolio():
    portfolio_items = [
        {'category': 'makeup', 'image': 'https://pixabay.com/get/ge393c8473f81869d31fc2c32b114f9473c65dfedd3cec9729339191b980cb5e3a24a56857fa002d910f7d0e82cad5bb0e486570955c3ede37dfe616e41895f0f_1280.jpg', 'title': 'Bridal Makeup'},
        {'category': 'makeup', 'image': 'https://pixabay.com/get/ge4222f59fbb78a389f71a619e54fa8b3ad0768eb59f923c2f084fd5c955e82ea13929795871fa7c0be11ce682ee76bbb906734c1ca0803e7f8f56ff1ab95b54e_1280.jpg', 'title': 'Evening Look'},
        {'category': 'makeup', 'image': 'https://pixabay.com/get/gfa6240df893c64e0efe4fadbc091431b2ed82dcc4d14f23e1ddc51b121423249b3051cf5597538a89e8dd098ac0b4fcffd0d9a031467aab1fca4142760c05034_1280.jpg', 'title': 'Natural Glow'},
        {'category': 'nails', 'image': 'https://pixabay.com/get/gcbc6538a81cc7d4f4f0434ede2165e0eac2ce9e6c9ef38855ff1b1223b43ae9c8ad7e856db7d79ed6f885f1d3396c233a57067034f8f8e5e7a47f99fd1818fa6_1280.jpg', 'title': 'Floral Nail Art'},
        {'category': 'nails', 'image': 'https://pixabay.com/get/g0e6ad5ffd55094c17b9ffaaa3fd33aa38c419ed83dd18b8a3f9c633ae5d8527db308f7871f601ad1eb23641f949d9872856b7833119de384668bb88e3aad98dc_1280.jpg', 'title': 'French Manicure'},
        {'category': 'nails', 'image': 'https://pixabay.com/get/g59a8fc92938a72cf023097f694b8aab35208d0a34f85134aa3bbd0d16122310d8e2bfebf2e27dc9b5461d16a0028a4b1137fd73bc1155dde05e53baada4b493f_1280.jpg', 'title': 'Geometric Design'}
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
