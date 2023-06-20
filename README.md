# wolfapp
A django app with social Oauth to enable users to make and maintain a personal profile.

# Project Structure

* The wolfapp folder contains all the web settings pertaining to the Django framework
* The personalprofile folder contains the models and views for handling the user's
profile data
* The templates folder contains the html templates that are displayed in the browser
* The tests folder contains the unit tests that run on the code

# Setup
To install the app in your current repository.

    git clone https://github.com/wtheaker97/wolfapp.git

Create a virtual environment and activate it.

    python -m venv venv
    source venv/bin/activate

Install the requirements.

    pip install -r requirements.txt

Migrate the database.

    python manage.py migrate

# Running the app

Once you have done the setup, you should be able to run the server.

    python manage.py runserver

Once the server is running you can visit the site in your web browser at http://localhost:8000


# Testing

To run the test suite on the app just run the pytest command from the command line (within the venv).

    pytest

# Using the admin panel

First, you need to create a superuser. When prompted, give the user a memorable username and password
e.g. admin, password (only for development!).

    python manage.py createsuperuser

Whilst the server is running you should be able to access the admin panel at http://localhost:8000/admin

From the admin panel you can view/create/edit/delete data stored in the db.
