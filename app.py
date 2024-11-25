from flask import Flask, request, jsonify
from src.content_based_filtering import recommend_for_new_customer  # Import the function for new customer recommendations
from src.hybrid_recommendation import hybrid_recommendations  # Import the function for existing customer recommendations
import pandas as pd
from flask_cors import CORS
from src.services.llm_query_processor import process_query
from src.services.llm_query_processor_new import process_query_new
from src.services.llm_query_processor_existing import process_query_existing

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Base URL route ("/")
@app.route('/')
def home():
    return "Welcome to the Flask App!"

# /hello route
@app.route('/hello')
def hello():
    return "Hello, World!"

# API route to process new user recommendations
@app.route('/api/recommend/new-user', methods=['POST'])
def recommend_newuser():
    # Get the data from the POST request
    data = request.get_json()
    user_query = data.get('user_query')
    
    # Validate the user query input
    if not user_query:
        return jsonify({'error': 'Missing user query'}), 400
    
    # Get recommendations using the content-based filtering algorithm
    try:
        recommendations = process_query_new(user_query)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/existing-user', methods=['POST'])
def recommend_existinguser():
    data = request.get_json()
    user_query = data.get('user_query')
    company = data.get('company_name')

    if not user_query or not company:
        return jsonify({'error': 'Missing user query or company name'}), 400
    
    try:
        # Get recommendations in sentence format
        recommendations_sentence = process_query_existing(company, user_query)
        return jsonify({'recommendations': recommendations_sentence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Load the companies from the Excel file
def load_companies():
    companies_file_path = 'data/companies.xlsx'  # Replace with the actual path to your Excel file
    companies_df = pd.read_excel(companies_file_path)
    
    # Assuming the Excel file has a column named "Company" with company names
    company_names = companies_df['Name'].tolist()
    return company_names

# Create a GET endpoint to return all the companies
@app.route('/company', methods=['GET'])
def get_companies():
    try:
        companies = load_companies()
        return jsonify({'companies': companies})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/query', methods=['POST'])
def handle_user_query():
    try:
        data = request.json
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Process the query using the logic from the service
        response = process_query(query)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port= 5000)
