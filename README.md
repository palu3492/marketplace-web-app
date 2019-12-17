# CSCI 4131 Final Project
Flask web app for CSCI 4131 final project.

## Project Details
1. **Project Type:** Plan A
2. **Group Member Name**: Aaron Eul
3. **Link to live Application**: https://final-project-eul-4131.herokuapp.com/
4. **Link to Github Code Repository**: https://github.com/Aeul/final-project-eul-4131
5. **List of Technologies/API's Used**:

    * Flask, Flask Login, Flask Mail, WTForms, Flask Migrate, Flask Moment
    * Bootstrap
    * SQLite
    * jQuery - for updating DOM
    * Leaflet - interactive map library
    * Nominatim API - convert location to latitude and longitude
        * https://nominatim.org/release-docs/develop/api/Overview/
    * Google Maps Geometry Library - to compute distances between latitudes and longitudes
        * https://developers.google.com/maps/documentation/javascript/reference/geometry

6. **Detailed Description of the project**:

    A fully functioning and feature-packed marketplace app that connects buyers and sellers together.
    Users can list products for sale and browse other user's listings. Each user has their own profile page
    that displays information about them and a link to contact them.
    On the home page, all the listings on the site are shown and they can
    be filtered using the filtering options. A preview of each listing is shown along with who created the
    listing. Listing pages show more information, they have a larger image and a full description of the listed
    product. Also, they show who created the listing and what city that person lives in.
    User profiles show each user's personal listings and a map showing where they live. They also have
    an edit profile button that lets them change their name, email, or location. Users can favorite listings
    and those listings will show up on their profiles. If a user wants to get in contact with another user
    they can send them a message which will send an email to that user's email on file.

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
    * favorite

8. **List of Views and their short description**:

    There is basically a view for each controller.
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
    * edit_profile.html - A form for editing information about the logged in user. A user can update their
    email, name, city, and state.
    * message.html - A form for sending a message to another user. Input a subject and message and an email
    with that information will be send to that user's email by issuing a POST request to the server.
    * login.html - A form for logging in. After a user enters their correct email and password they
    will be redirected to the home page. There is also a register button that lets
    unregistered users register an account. 
    * logout.html - This page simply logs out the logged in user and redirects them to the home page.
    * register.html - A form for registering an account. A new user enters their name, email, city, and state
    to create an account. A POST request will ask the server to add the new user to the database.
    
9. **List of Tables, their Structure and short description**:

    * User table - Holds all user data from when a user registers and this data can be changed on the edit profile page.
        * Columns: id, name, email, password_hash (plain-text password hashed for security), last_seen, city, state
    * Listing table - Holds data about listings for sale on site and associates them with author of listing.
        * Columns: id, title, price, condition (new, used), body (description of listing), timestamp (when it was created), user_id (author of listing)
    * Image table - Holds image locations for listings, which can have multiple images.
        * Columns: id, name, extension (.png, .jpg), instance (occurrence count of image name),
        src (where it's located on server), listing_id (listing it's associated with)
    * Favorite table - Holds all favorited listings that users have favorited.
        * Columns: id, listing_id, user_id

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
    For learning how to do Flask file uploads.
    
    https://flask-migrate.readthedocs.io/en/latest/
    For learning how to use Flask Migrate.
    
    https://pythonhosted.org/Flask-Mail/ To learn about Flask Mail.

    https://exploreflask.com/en/latest/views.html#view-decorators
    For understanding routing.
    
    https://stackoverflow.com/questions/tagged/flask
    Used to find answers to problems I had in Flask.
    
    https://leafletjs.com/examples/quick-start/
    For setting up Leaflet map.

