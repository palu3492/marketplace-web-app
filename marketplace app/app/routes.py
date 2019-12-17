from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ListingForm, MessageForm, FilterForm
from app.models import User, Listing, Image, Favorite
from app.email import send_email
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from datetime import datetime
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    if form.validate_on_submit():
        listings = Listing.query
        if form.condition.data:
            listings = listings.filter(Listing.condition == form.condition.data)
        if form.price_min.data:
            listings = listings.filter(Listing.price >= float(form.price_min.data))
        if form.price_max.data:
            listings = listings.filter(Listing.price <= float(form.price_max.data))

        listings = listings.order_by(Listing.timestamp.desc()).all()
    else:
        listings = Listing.query.order_by(Listing.timestamp.desc()).all()
    listings = listings + listings + listings
    images = {}
    users = {}
    for _listing in listings:
        images[_listing.id] = Image.query.filter_by(listing_id=_listing.id).first()
        users[_listing.id] = _listing.author
    return render_template("index.html", title='Listings', listings=listings, images=images, users=users, user_info=True, form=form)

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
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You've been logged out")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, city=form.city.data, state=form.state.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You've been registered")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<id>')
def user(id):
    _user = User.query.filter_by(id=id).first_or_404()
    listings = Listing.query.filter_by(user_id=_user.id).order_by(Listing.timestamp.desc()).all()
    favorite_listings = []
    if _user == current_user:
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        for fav in favorites:
            _listing = Listing.query.filter_by(id=fav.listing_id).first()
            favorite_listings.append(_listing)
    images = {}
    for _listing in listings:
        images[_listing.id] = Image.query.filter_by(listing_id=_listing.id).first()
    return render_template('user.html', user=_user, listings=listings, images=images, title='View Profile', user_info=False, favorites=favorite_listings)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.state = form.state.data
        current_user.city = form.city.data
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('user', id=current_user.id))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.state.data = current_user.state
        form.city.data = current_user.city
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

        flash('Listing created')
        return redirect(url_for('listing', id=_listing.id))
    return render_template("new_listing.html", title='Create New Listing', form=form)

@app.route('/listing/<id>')
def listing(id):
    _listing = Listing.query.filter_by(id=id).first_or_404()
    _user = _listing.author
    image = Image.query.filter_by(listing_id=_listing.id).first()
    return render_template('listing.html', listing=_listing, title='View Listing', image=image, user=_user, current_user=current_user)

@app.route('/delete_listing/<id>')
@login_required
def delete_listing(id):
    _listing = Listing.query.filter_by(id=id)
    if _listing.first().author == current_user:
        Listing.query.filter_by(id=id).delete()
        Image.query.filter_by(listing_id=id).delete()
        db.session.commit()
        flash('Listing deleted')
        return redirect(url_for('index'))
    else:
        flash('You can only delete listings you authored')
        return redirect(url_for('listing', id=id))

@app.route('/message/<id>', methods=['GET', 'POST'])
@login_required
def message(id):
    _user = User.query.filter_by(id=id).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        form_subject = form.subject.data
        form_message = form.body.data
        recipient = _user.email
        _message = "<p>You've received a new message from <a href='"+app.config['HOST']+url_for('user', id=current_user.id)+"'>"+current_user.name+"</a> on Marketplace.</p>"
        _message += '<p>Subject: '+form_subject+'</p>'
        _message += '<p>Message: '+form_message+'</p>'
        _message += '<p><a href="'+app.config['HOST']+url_for('message', id=current_user.id)+'">Reply to '+current_user.name+' on Marketplace</a></p>'
        subject = "Message from "+current_user.name+" on Marketplace"
        send_email(subject, 'flasktestemail120@gmail.com', [recipient], _message, _message)
        flash('Message sent')
        return redirect(url_for('user', id=id))
    return render_template('message.html', title='Send Message', form=form, user=_user, current_user=current_user)

@app.route('/favorite/<id>')
@login_required
def favorite(id):
    favorited = Favorite.query.filter_by(listing_id=id, user_id=current_user.id).first()
    if not favorited:
        fav = Favorite(
            listing_id=id,
            user_id=current_user.id
        )
        db.session.add(fav)
        db.session.commit()
        flash('Added to favorites')
    else:
        flash('Already in your favorites')
    return redirect(url_for('listing', id=id))