import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, KNNBasic
from collections import defaultdict

### Step 1: Prepare Collaborative Filtering Data ###
# Load the entitlements data
entitlements_file_path = 'data/entitlements.xlsx'
entitlements_df = pd.read_excel(entitlements_file_path)

# Create interaction data for collaborative filtering
interaction_df = entitlements_df[['Company', 'Product', 'Implemented']]

# Collaborative Filtering Preparation (Surprise KNNBasic)
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(interaction_df[['Company', 'Product', 'Implemented']], reader)
trainset = data.build_full_trainset()
sim_options = {'name': 'cosine', 'user_based': True}
algo = KNNBasic(sim_options=sim_options)
algo.fit(trainset)

### Step 2: Prepare Content-Based Filtering Data ###

# Load both products and accelerators datasets
products_file_path = 'data/products.xlsx'
accelerators_file_path = 'data/accelerators.xlsx'

products_df = pd.read_excel(products_file_path)
accelerators_df = pd.read_excel(accelerators_file_path)

# Strip leading/trailing spaces from column names
products_df.columns = products_df.columns.str.strip()
accelerators_df.columns = accelerators_df.columns.str.strip()

# Merge the products and accelerators DataFrames
merged_df = pd.merge(products_df, accelerators_df, left_on='Name', right_on='Product', how='inner')

# Handle missing values
merged_df['Category'] = merged_df['Category'].fillna('')
merged_df['Description'] = merged_df['Description'].fillna('')
merged_df['Short description'] = merged_df['Short description'].fillna('')
merged_df['Type'] = merged_df['Type'].fillna('')

# Combine relevant fields from both products and accelerators to create a comprehensive feature
merged_df['features'] = (
    merged_df['Category'] + ' ' +
    merged_df['Description'] + ' ' +
    merged_df['Short description'] + ' ' +
    merged_df['Type']
)

# TF-IDF vectorization for combined products and accelerators
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(merged_df['features'])

### Step 3: Define Recommendation Functions ###

# Function to recommend using collaborative filtering
def collaborative_filtering_recommendations(company, top_n=5):
    company_recommendations = []
    unique_products = interaction_df['Product'].unique()
    
    for product in unique_products:
        rating = algo.predict(company, product)
        company_recommendations.append((product, rating.est))
    
    # Sort recommendations by rating and return the top N
    company_recommendations.sort(key=lambda x: x[1], reverse=True)
    return [product for product, rating in company_recommendations[:top_n]]

# Function to recommend using content-based filtering with combined accelerators and products
def content_based_recommendations(customer_input, top_n=5):
    customer_input_tfidf = tfidf.transform([customer_input])
    cosine_sim = cosine_similarity(customer_input_tfidf, tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[:top_n]]
    return merged_df['Name_x'].iloc[top_indices]  # Return the product name

# Hybrid recommendation system combining both approaches
def hybrid_recommendations(company, customer_input, collaborative_weight=0.7, content_weight=0.3, top_n=5):
    # Collaborative filtering recommendations
    collaborative_recs = collaborative_filtering_recommendations(company, top_n)
    
    # Content-based filtering recommendations
    content_recs = content_based_recommendations(customer_input, top_n)
    
    # Combine the results (weighted)
    combined_recommendations = defaultdict(float)
    
    for product in collaborative_recs:
        combined_recommendations[product] += collaborative_weight
        
    for product in content_recs:
        combined_recommendations[product] += content_weight
    
    # Sort combined recommendations by weighted score
    final_recommendations = sorted(combined_recommendations.items(), key=lambda x: x[1], reverse=True)
    
    # Extract the top N product names
    top_products = [product for product, score in final_recommendations[:top_n]]

    # Format the output as a readable sentence
    # recommendations_sentence = f"The recommended products for {company} based on your input '{customer_input}' are: "
    recommendations_sentence = f"The recommended products for your company based on your input '{customer_input}' are: "
    recommendations_sentence += ', '.join([f"{i + 1}. {product}" for i, product in enumerate(top_products[:-1])])
    recommendations_sentence += f", and {top_n}. {top_products[-1]}."

    return recommendations_sentence
### Step 4: Test the Hybrid Recommendation System ###

# Example usage: Recommend for a specific company and customer input
#company = 'Alpha Accessories'  # Example company from interaction data
#customer_input = "I want to enhance customer support automation"  # Example input from customer

# Get hybrid recommendations
# hybrid_recs = hybrid_recommendations(company, customer_input)

# print(f"Hybrid recommendations for {company} based on input '{customer_input}':\n", hybrid_recs)
