import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the products and accelerators datasets
products_file_path = 'data/products.xlsx'
accelerators_file_path = 'data/accelerators.xlsx'

products_df = pd.read_excel(products_file_path)
accelerators_df = pd.read_excel(accelerators_file_path)

# Strip leading and trailing spaces from column names
products_df.columns = products_df.columns.str.strip()
accelerators_df.columns = accelerators_df.columns.str.strip()

# Merge the products and accelerators DataFrames based on 'Name' and 'Product'
merged_df = pd.merge(products_df, accelerators_df, left_on='Name', right_on='Product', how='inner')

# Handle missing values
merged_df['Category'] = merged_df['Category'].fillna('')
merged_df['Description'] = merged_df['Description'].fillna('')
merged_df['Short description'] = merged_df['Short description'].fillna('')
merged_df['Type'] = merged_df['Type'].fillna('')

# Combine relevant fields to create a comprehensive feature (Category + Description + Short description + Type)
merged_df['features'] = merged_df['Category'] + ' ' + merged_df['Description'] + ' ' + merged_df['Short description'] + ' ' + merged_df['Type']

# Initialize TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(merged_df['features'])

# Function to recommend accelerators for new customer input
def recommend_for_new_customer(customer_input, top_n=5):
    # Vectorize the customer input
    customer_input_tfidf = tfidf.transform([customer_input])

    # Compute cosine similarity between the input and all product features
    cosine_sim = cosine_similarity(customer_input_tfidf, tfidf_matrix)

    # Sort by similarity
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Check if no close matches were found
    if sim_scores[0][1] == 0:
        return "No close matches found for the input."

    # Get top N recommended accelerators
  # Get top N recommended accelerators
    top_indices = [i[0] for i in sim_scores[:top_n]]
    recommended_accelerators = merged_df[['Name_y', 'Name_x', 'Category', 'Short description']].iloc[top_indices].copy()

    # Create a human-readable sentence output with HTML formatting
    # recommendations_text = f"The top {top_n} recommended accelerators for '{customer_input}' are:<br /><ol>"
    recommendations_text = f"The top {top_n} recommended accelerators for you are:<br /><ol>"

    # Loop through the recommendations and add them as list items in the ordered list
    for _, row in recommended_accelerators.iterrows():
        # recommendations_text += f"<li>{row['Name_y']} (Product: {row['Name_x']}, Category: {row['Category']}): {row['Short description']}</li>"
        #recommendations_text += f"<li>Accelerator: {row['Name_y']} (Product: {row['Name_x']}, Category: {row['Category']}): Short description {row['Short description']}</li>"
        recommendations_text += f"<li>{row['Name_y']}, Short description: {row['Short description']}</li>"


    # Close the ordered list
    recommendations_text += "</ol>"

    # Return or print the final HTML-formatted string
    return recommendations_text
