from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

app = Flask(__name__)

# Set up a secret key for your app
app.secret_key = 'themisdefensivesecretkey'

# Create a LoginManager instance
login_manager = LoginManager()
login_manager.init_app(app)

# Define a User class with UserMixin from flask_login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user ID
    # Return None if the user does not exist
    return User(user_id)

# A simple user database
users = {
    1: {'username': 'Baze University', 'password': 'BAZEUNIVERSITY', 'unique identifier': 'baze identifier', 'redirect_url': 'https://view.genial.ly/6468935c7efa7c0012a47703/interactive-image-baze-university-abuja-interactive-image'},
    2: {'username': 'Nile University', 'password': 'NILEUNIVERSITY', 'unique identifier': 'nile identifier', 'redirect_url': 'https://www.genial.ly/embed/123456'},
    3: {'username': 'British Nigerian Academy', 'password': 'BRITISHNIGERIANACADEMY', 'unique identifier': 'bna identifier', 'redirect_url': 'https://www.genial.ly/embed/7891011'}
}

# Define a route that renders your sign-in form
@app.route('/')
def signin():
    return render_template('index.html')

# Define a route that handles user authentication
@app.route('/login', methods=['POST'])
def login():
    # Retrieve the username and password from the form
    username = request.form['username']
    password = request.form['password']

    # Validate the username and password against your user database
    for user_id, user in users.items():
        if user['username'] == username and user['password'] == password:
            # Log the user in and redirect to the dashboard
            user_obj = User(user_id)
            login_user(user_obj)
            return redirect(url_for('dashboard'))

    # Display an error message if the username or password is incorrect
    return 'Invalid username or password.'

# Define a route that logs the user out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

# Define a route that requires authentication
@app.route('/dashboard')
@login_required
def dashboard():
    # Retrieve the logged-in user's unique identifier from the user database
    user_id = current_user.id
    user_data = users.get(user_id)

    if user_data and 'redirect_url' in user_data:
        redirect_url = user_data['redirect_url']
        return redirect(redirect_url)

    # Handle the case if the user does not exist or if no redirect URL is available
    return "Invalid user or no redirect URL available."

if __name__ == '__main__':
    app.run(debug=True)
