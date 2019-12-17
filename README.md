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
    be filtered using the filtering options. These listings are previews that link to the full listings, they
    also show who created the
    listing. The full listing pages show more information, they have a larger image and a full description of the listed
    product. Also, they show who created the listing and what city that person lives in.
    User profiles show each user's personal listings and a map showing where they live. They also have
    an edit profile button that lets them change their name, email, or location. Users can favorite listings
    and those listings will show up on their profiles. If a user wants to get in contact with another user
    they can send them a message which will send an email to that user's email on file. Many features require
    an account to use, like messaging and listing an item, so registering an account first is crucial.
    

7. **List of Controllers and their short description**:

    * index - Home page of the website, displays all listings for sale posted by users of the site.
    Renders index.html to show listings. It also renders a form that will use a POST request to filter listings.
    * listing - Uses supplied URL parameter 'id' to render a particular listing using listing.html.
    * new_listing - Renders a form for user to input new information for a new listing. A POST request will
    create a new listing in the database using the supplied info and adds a time stamp.
    * delete_listing - When the author of a listing visits their listing they have the option to
    delete it. If they click delete they will be redirected to this delete_listing controller which will delete their
    listing. A GET request will ask the server to remove all information about the listing (id from URL parameter)
    from the database tables.
    * user - Gets all the information for the user (user id supplied in URL parameter) and the user's listings from 
    the database and renders it using user.html.
    * edit_profile - Fills in edit_profile.html, which is a form, with a user's current information which can then be
    changed by submitting the form and that POST request will update the database to the new user information.
    * message - Renders a form for sending messages to other users using message.html. A post request from the form 
    will send an email using Gmail to the user that is defined by the URL parameter 'id'.
    * login - Renders a form from login.html and after a user enters their correct email and password they will be
    logged into the Flask user management system and then redirected to the home page.
    * logout - Logs the user out from Flask user management system.
    * register - Renders a form from register.html and a POST request from that form will create a new user in the
    database using the information from the form.
    * favorite - Sends a GET request with the URL parameter of a listing that the current user wants to favorite,
    the database will be updated, associating that favorited listing to the current user.

8. **List of Views and their short description**:
    
    * index.html - Renders all listings or filtered listings posted by users of the site.
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
    title, price, condition, description, and any images of the product they're selling. 
    * user.html - Displays all the information about a user: name, profile image, location, when they were online last,
    link to message them, and a map showing their location. Also, all the listings they authored and their favorites
    are shown.
    * edit_profile.html - A form for editing information about the logged-in user. A user can update their
    email, name, city, and state.
    * message.html - A form for sending a message to another user. Input a subject and message and an email
    with that information will be sent to that user's email.
    * login.html - A form for logging in. There is also a register button that will redirect to the register page. 
    * register.html - A form for registering an account. A new user enters their name, email, city, and state
    to create an account.
    
9. **List of Tables, their Structure and short description**:

    * User table - Holds all user data from when a user registers and this data can be changed on the edit profile page.
        * Columns: id, name, email, password_hash (plain-text password hashed for security), last_seen, city, state
    * Listing table - Holds data about listings for sale on site and associates them with author of the listing.
        * Columns: id, title, price, condition (new, used), body (description of listing), timestamp (when it was created), user_id (author of listing)
    * Image table - Holds image locations for listings. Listings can have multiple images.
        * Columns: id, name, extension (.png, .jpg), instance (occurrence count of image name),
        src (where it's located on server), listing_id (listing it's associated with)
    * Favorite table - Holds all favorited listings that users have favorited. Users can have many favorited listings.
        * Columns: id, listing_id, user_id

10. **References/Resources**:

    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    Used to setup the initial app. Tutorial walked me through setting up database tables, user management, forms and routing.
    
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

