from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# In-memory user storage (for demo purposes only — resets on app restart)
users = {}

# Route to Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route to Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            flash("Email already registered.", "warning")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        users[email] = {
            'username': username,
            'password': hashed_password
        }

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Route to Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = email
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. Please try again.", "danger")
    
    return render_template('login.html')

# Route to Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
