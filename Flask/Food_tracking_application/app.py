from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='D:/Github/Backend_Project/Flask/Food_tracking_application')

# Configure the Flask app to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/Flask'

db = SQLAlchemy(app)

# Define a model for the food table
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbohydrate = db.Column(db.Float, nullable=False) 
    fat = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False) 

# Define a model for the log_data table
class LogData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index(): # Retrieve all food items from the database
    if request.method == 'POST':
        date_str = request.form.get("date")
        if date_str:  # Check if the date string is not empty
            entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            log_data = LogData(entry_date=entry_date)
            db.session.add(log_data)
            db.session.commit()
    log = LogData.query.order_by(LogData.entry_date.desc()).all()
    return render_template('home.html', log=log)

@app.route('/view/')
def view():
   # Fetch log entries and pass them to the template
    log_entries = LogData.query.all()
    return render_template('day.html', log_entries=log_entries)

@app.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        # Get form data
        food_name = request.form['food-name']
        protein = float(request.form['protein'])  # Convert to float
        carbohydrates = float(request.form['carbohydrate'])  # Convert to float
        fat = float(request.form['fat'])  # Convert to float
        calories = protein * 4 + carbohydrates * 4 + fat * 9
        # Create a new Food instance
        new_food = Food(name=food_name, protein=protein, carbohydrate=carbohydrates, fat=fat, calories=calories)
        
        # Add the instance to the session
        db.session.add(new_food)
        # Commit the session to persist the changes to the database
        db.session.commit()
    # Fetch all food items from the database
    results = Food.query.all()
    return render_template('add_food.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
