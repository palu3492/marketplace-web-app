from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ListingForm
from app.models import User, Listing, Image
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from datetime import datetime
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    listings = Listing.query.order_by(Listing.timestamp.desc()).all()
    images = {}
    for _listing in listings:
        print(_listing.price)
        images[_listing.id] = Image.query.filter_by(listing_id=_listing.id).first()
    return render_template("index.html", title='Home Page', listings=listings, images=images, page='Listings')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<id>')
def user(id):
    _user = User.query.filter_by(id=id).first_or_404()
    listings = Listing.query.filter_by(user_id=_user.id).order_by(Listing.timestamp.desc()).all()
    images = {}
    for _listing in listings:
        images[_listing.id] = Image.query.filter_by(listing_id=_listing.id).first()
    return render_template('user.html', user=_user, listings=listings, images=images)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.name)
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/new_listing', methods=['GET', 'POST'])
@login_required
def new_listing():
    form = ListingForm()
    if form.validate_on_submit():
        _listing = Listing(
            title=form.title.data,
            body=form.body.data,
            condition=form.condition.data,
            price=form.price.data,
            author=current_user
        )
        db.session.add(_listing)
        db.session.commit()
        # Image upload
        filename = secure_filename(form.image.data.filename)
        [filename, ext] = filename.split('.') # ['image', 'png']
        instance = 0
        db_image = Image.query.filter_by(name=filename).order_by(Image.instance.desc()).first()
        if db_image and db_image.instance is not None:
            instance = int(db_image.instance) + 1
        location = filename + str(instance) + '.' + ext
        form.image.data.save(os.path.join(app.config['IMAGES_FOLDER'], location))
        image = Image(
            name=filename,
            extension=ext,
            instance=instance,
            src=location,
            listing_id=_listing.id
        )
        db.session.add(image)
        db.session.commit()

        flash('Your post is now live!')
        return redirect(url_for('listing', id=_listing.id))
    return render_template("new_listing.html", title='New Listing', form=form)

@app.route('/listing/<id>')
def listing(id):
    # user = User.query.filter_by(username=username).first_or_404()
    _listing = Listing.query.filter_by(id=id).first_or_404()
    return render_template('listing.html', listing=_listing)