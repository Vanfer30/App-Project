from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email is already registered
        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'error')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        print("User registered successfully:", new_user.email)  # Log successful registration

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('success'))
        
    print("Registration form submitted")  # Log form submission
        
    users = User.query.all()
        # Pass the updated list of users to the template
    return render_template('userregistration.html', users=users)
    
   
@app.route('/', methods=['POST', 'GET'])
def index():
    error = request.args.get('error')  # Check if there's an error query parameter
    return render_template('login.html', error=error)

@app.route('/validate', methods=['POST'])
def validate():
    email = request.form.get('email')
    password = request.form.get('password')

    # Query the database to check if the user exists and the password matches
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        # Valid credentials, set authenticated session and redirect to success page
        session['authenticated'] = True
        return redirect(url_for('success'))
    else:
        # Invalid credentials, redirect back to the login form with an error message
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('index', error=True))

@app.route('/success')
def success():
    if session.get('authenticated'):    
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))


@app.route('/products')
def products():
    if session.get('authenticated'):    
        return render_template('products.html')
    else:
        return redirect(url_for('index'))
    
@app.route('/customers')
def customers():
    if session.get('authenticated'):    
        return render_template('customers.html')
    else:
        return redirect(url_for('index'))
    

@app.route('/finance')
def finance():
    if session.get('authenticated'):    
        return render_template('finance.html')
    else:
        return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    if session.get('authenticated'):    
        return render_template('login.html')
    else:
        return redirect(url_for('/'))
    
if __name__ == '__main__':
    app.run(debug=True)

