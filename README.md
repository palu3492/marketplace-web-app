# Final Project
Flask web app for CSE400 final project.

## Project Details
1. **Project Type:** Plan A
2. **Group Member Name**: Aaron Eul
3. **Link to live Application**: 
4. **Link to Github Code Repository**: 
5. **List of Technologies/API's Used**:
    * Flask, Flask Login, Flask Mail, WTForms, Flask Migrate
    * Bootstrap
    * SQLite
    * Leaflet - interactive map library
    * Nominatim API - convert location to latitude and longitude
        * https://nominatim.org/release-docs/develop/api/Overview/
    * Google Maps Geometry Library - to compute distances between latitudes and longitudes
        * https://developers.google.com/maps/documentation/javascript/reference/geometry
6. **Detailed Description of the project**:
7. **List of Controllers and their short description**:
    * index
    * listing
    * new_listing
    * delete_listing
    * user
    * edit_profile
    * message
    * login
    * logout
    * register
8. **List of Views and their short description**:
    * index.html - Home page of the website, displays all listings for sale posted by users of the site.
    Listings show the title, price, and image of the product for sale and who posted the listing.
    * listing.html - Displays a listing's information: title, price, condition, description, and images.
    Also, shows who posted the listing with a link to where a user can message them.
    * _listing.html - (Sub-template) renders a listing box that contains the title, price, and condition of the
    product for sale. One of these listing boxes is created for each listing by iterating through the
    listings. Shown on the index and user pages.
    * _listings.html - (Sub-template) renders all the _listing.html listing boxes by iterating over all the
    listings and creating a group of filled in _listing.html listing boxes. This is displayed on the index
    and user page, that's why it's a sub-template, so it can just be inserted anywhere.
    * new_listing.html - A form for creating a new listing. The user creating a listing inputs in the
    title, price, condition, description, and any images of the product they're selling. All this information
    is then stored in the database from a POST request, along with the time stamp of when it was created.
    * delete_listing.html - When the author of a listing visits their listing they have the option to
    delete it. If they click delete they will be redirected to this delete_listing view which will delete their listing.
    A POST request will ask the server to remove all information about the listing from the database tables. 
    * user.html - Displays all the information about a user: name, profile image, location, when they were online last,
    link to message them, and a map showing their location. Also, all the listings they authored are shown.
    * edit_profile.html
    * message.html
    * login.html
    * logout.html
    * register.html
9. **List of Tables, their Structure and short description**:
    * User table - Holds all user data from when a user registers and this data can be changed on the edit profile page.
        * Columns: id, name, email, password_hash (plain-text password hashed for security), last_seen, city, state
    * Listing table - Holds data about listings for sale on site and associates them with author of listing.
        * Columns: id, title, price, condition (new, used), body (description of listing), timestamp (when it was created), user_id (author of listing)
    * Image table - Holds image locations for listings, which can have multiple images.
        * Columns: id, name, extension (.png, .jpg), instance (occurrence count of image name),
        src (where it's located on server), listing_id (listing it's associated with)
10. **References/Resources**:

    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    Used to setup initial app. Tutorial walked me through setting up database tables, user management, forms and routing.
    
    https://flask.palletsprojects.com/en/1.1.x/quickstart/
    Flask docs for learning Flask.
    
    https://flask-wtf.readthedocs.io/en/stable/
    Helped with using Flask WTForms.
    
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
    Helped with using SQLAlchemy.
    
    https://pythonhosted.org/Flask-Uploads/
    For learning how to do flask file uploads.
    
    https://flask-migrate.readthedocs.io/en/latest/
    For learning how to use Flask Migrate.

    https://exploreflask.com/en/latest/views.html#view-decorators
    For understanding routing.
    
    https://stackoverflow.com/questions/tagged/flask
    Used to find answers to problems I had in flask.

