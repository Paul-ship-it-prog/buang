from flask import Flask, render_template, request, redirect, url_for, session, flash
import os  # For generating a random secret key

app = Flask(__name__)

# Set a constant secret key (important for session management)
app.secret_key = os.environ.get('SECRET_KEY', 'your-development-secret-key')

# Simulated user database
users = {
    "test@example.com": {"password": "password123", "name": "Test User"}
}

# Questions database
questions = [
    {"question": "What is a database?", "options": ["A file system", "A collection of data", "A web application", "None of the above"], "answer": "A collection of data"},
    {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Structured Question Language", "Simple Query Language", "Structured Query Lab"], "answer": "Structured Query Language"},
    # Add more questions as needed...
]

@app.route('/')
# Home route to display the welcome message and the Proceed button
@app.route('/')
def home():
    return render_template('proceed.html')  # Welcome Page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle sign-up logic (save user to the database)
        flash("Sign up successful! Please log in.")
        return redirect(url_for('login'))  # After signup, redirect to login
    return render_template('signup.html')  # Sign Up Page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Logic for validating login credentials
        flash("Login successful!")
        return redirect(url_for('quiz'))  # Redirect to quiz after login
    return render_template('login.html')  # Login Page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email not in users:
            if len(password) < 8:
                flash('Password must be at least 8 characters long.', 'danger')
            elif "@" not in email or "." not in email:
                flash('Invalid email address.', 'danger')
            else:
                users[email] = {"password": password, "name": email.split('@')[0]}
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('login'))
        else:
            flash('Email already exists. Try logging in.', 'danger')
    return render_template('signup.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user' not in session:
        flash('Please log in to access the quiz.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Calculate the score
        score = 0
        for i, question in enumerate(questions):
            answer = request.form.get(f'question{i}')
            if answer == question['answer']:
                score += 1
        return redirect(url_for('result', score=score))

    return render_template('quiz.html', questions=questions)

@app.route('/result')
def result():
    if 'user' not in session:
        flash('Please log in to view your results.', 'danger')
        return redirect(url_for('login'))

    score = request.args.get('score', type=int, default=0)
    return render_template('result.html', score=score)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
