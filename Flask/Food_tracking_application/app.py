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
    carbohydrate = db.Column(db.Float, nullable=False)  # Rename to 'carbohydrate' to match database
    fat = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False) 

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('day.html')

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
