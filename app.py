import os
from datetime import datetime, timedelta
import secrets
import string

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import validators

# ----- Config -----
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_urlsafe(16))
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'url_shortener.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----- Models -----
class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(12), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, nullable=True)
    clicks = db.Column(db.Integer, default=0)

    def is_expired(self):
        if self.expire_at is None:
            return False
        return datetime.utcnow() > self.expire_at

# ----- Helpers -----
ALPHABET = string.ascii_letters + string.digits

def generate_code(length=6):
    # Secure random code from letters+digits
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def generate_unique_code(length=6):
    for _ in range(10):
        code = generate_code(length)
        if not URLMapping.query.filter_by(short_code=code).first():
            return code
    # fallback to longer code if collisions
    while True:
        code = generate_code(length+2)
        if not URLMapping.query.filter_by(short_code=code).first():
            return code

# Ensure DB exists
# Ensure DB exists
with app.app_context():
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    db.create_all()


# ----- Routes -----
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('original_url', '').strip()
        custom_code = request.form.get('custom_code', '').strip()
        expiry_days = request.form.get('expiry_days', '').strip()

        # Validate URL
        if not original_url:
            flash('Please enter a URL', 'warning')
            return redirect(url_for('index'))
        if not validators.url(original_url):
            flash('Please enter a valid URL (include http:// or https://)', 'danger')
            return redirect(url_for('index'))

        # Expiry processing
        expire_at = None
        if expiry_days:
            try:
                days = int(expiry_days)
                if days > 0:
                    expire_at = datetime.utcnow() + timedelta(days=days)
            except ValueError:
                flash('Expiry days must be an integer', 'warning')
                return redirect(url_for('index'))

        # custom code or generate
        if custom_code:
            if len(custom_code) < 3 or len(custom_code) > 12:
                flash('Custom code must be 3-12 characters', 'warning')
                return redirect(url_for('index'))
            exists = URLMapping.query.filter_by(short_code=custom_code).first()
            if exists:
                flash('Custom code already taken. Try another.', 'danger')
                return redirect(url_for('index'))
            code = custom_code
        else:
            code = generate_unique_code(6)

        mapping = URLMapping(original_url=original_url, short_code=code, expire_at=expire_at)
        db.session.add(mapping)
        db.session.commit()

        short_url = request.host_url + code
        flash('Short URL created!', 'success')
        return render_template('index.html', created=True, short_url=short_url, mapping=mapping)

    # GET
    recent = URLMapping.query.order_by(URLMapping.created_at.desc()).limit(10).all()
    return render_template('index.html', recent=recent)

@app.route('/<code>')
def redirect_short(code):
    mapping = URLMapping.query.filter_by(short_code=code).first_or_404()
    if mapping.is_expired():
        return render_template('404.html', message='This short link has expired.'), 410
    mapping.clicks += 1
    db.session.commit()
    return redirect(mapping.original_url)

@app.route('/stats')
def stats():
    all_links = URLMapping.query.order_by(URLMapping.clicks.desc()).all()
    return render_template('stats.html', links=all_links)

# API: get stats for a code (JSON)
@app.route('/api/stats/<code>')
def api_stats(code):
    mapping = URLMapping.query.filter_by(short_code=code).first_or_404()
    return jsonify({
        'original_url': mapping.original_url,
        'short_code': mapping.short_code,
        'short_url': request.host_url + mapping.short_code,
        'created_at': mapping.created_at.isoformat(),
        'expire_at': mapping.expire_at.isoformat() if mapping.expire_at else None,
        'clicks': mapping.clicks,
        'expired': mapping.is_expired()
    })

# custom 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message='Short link not found.'), 404

if __name__ == '__main__':
    app.run(debug=True)
