from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import urllib.parse
from waitress import serve

app = Flask(__name__)

# update it with your mongodb username password and uri
username = 'user'
password = 'password'
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)
app.config['MONGO_URI'] = f'mongodb+srv://{escaped_username}:{escaped_password}@mongodbcluster'

mongo = PyMongo(app)

app.secret_key = 'MySuperSecretKey'

# app routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/resume')
def resume():
    return render_template("resume.html")


@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route('/terms')
def terms():
    return render_template("terms.html")


@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    try:
        # Access form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        country = request.form['country']
        message = request.form['message']

        # Insert data into MongoDB
        mongo.db.user_data.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'country': country,
            'message': message
        })

        # Optionally, redirect the user to a thank you page
        return render_template('thank_you.html')

    except Exception as e:
        # Handle the error
        print("An error occurred:", str(e))
        return "An error occurred while processing your request. Please try again later.", 500


if __name__ == "__main__":
    mode = "development" # Change it to production if you want to run on waitress server
    if mode == "production":
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(debug=True, host="0.0.0.0", port=5000)
