from flask import Flask, jsonify, abort
import pandas as pd
import os
import seaborn as sns

# Initialize the Flask app
app = Flask(__name__)

# Define the path for the Titanic CSV file
CSV_FILE_PATH = 'titanic_data.csv'

# Function to create the CSV file if it doesn't exist
def create_csv_if_not_exists():
    if not os.path.exists(CSV_FILE_PATH):
        # Load Titanic dataset from seaborn
        titanic = sns.load_dataset('titanic')
        # Select relevant columns
        titanic_subset = titanic[['survived', 'pclass', 'sex', 'age', 'fare', 'embarked']].dropna()
        # Save to CSV
        titanic_subset.to_csv(CSV_FILE_PATH, index=False)
        print(f"Created {CSV_FILE_PATH}")
    else:
        print(f"{CSV_FILE_PATH} already exists")

# Call this function when the app starts
create_csv_if_not_exists()

# Load the Titanic dataset from the CSV file
df = pd.read_csv(CSV_FILE_PATH)

# Convert dataframe to dictionary for easier processing
titanic_data = df.to_dict(orient='records')

# Get all passengers
@app.route('/api/passengers', methods=['GET'])
def get_passengers():
    return jsonify({'passengers': titanic_data})

# Get passenger by ID
@app.route('/api/passengers/<int:passenger_id>', methods=['GET'])
def get_passenger_by_id(passenger_id):
    passenger = next((p for p in titanic_data if p['passenger_id'] == passenger_id), None)
    if passenger is None:
        abort(404, description=f"Passenger with ID {passenger_id} not found")
    return jsonify({'passenger': passenger})

# Filter passengers by survival status (1 for survived, 0 for not survived)
@app.route('/api/passengers/survived/<int:status>', methods=['GET'])
def get_passengers_by_survival(status):
    if status not in [0, 1]:
        abort(400, description="Invalid survival status. Use 1 for survived and 0 for not survived")
    
    passengers = [p for p in titanic_data if p['survived'] == status]
    return jsonify({'passengers': passengers})

# Filter passengers by class (1st, 2nd, 3rd)
@app.route('/api/passengers/class/<int:class_num>', methods=['GET'])
def get_passengers_by_class(class_num):
    if class_num not in [1, 2, 3]:
        abort(400, description="Invalid class. Use 1, 2, or 3 for passenger class")
    
    passengers = [p for p in titanic_data if p['pclass'] == class_num]
    return jsonify({'passengers': passengers})

# Error handling for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': error.description}), 404

# Error handling for 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': error.description}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
