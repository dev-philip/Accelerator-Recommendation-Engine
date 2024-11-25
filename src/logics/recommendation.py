import pandas as pd
from collections import defaultdict

from src.hybrid_recommendation import collaborative_filtering_recommendations, content_based_recommendations

# Load your dataset with accelerator information
products_df = pd.read_excel('data/products.xlsx')

# Function to fetch information about a specific accelerator
def get_accelerator_info(accelerator_name):
    accelerator_info = products_df[products_df['Name'].str.contains(accelerator_name, case=False)]
    
    if not accelerator_info.empty:
        description = accelerator_info.iloc[0]['Description']
        category = accelerator_info.iloc[0]['Category']
        return f"Accelerator: {accelerator_name}\nCategory: {category}\nDescription: {description}"
    else:
        return f"Sorry, I couldn't find information on the accelerator '{accelerator_name}'."

# Hybrid recommendation system combining collaborative filtering and content-based filtering
def hybrid_recommendations(company, customer_input, collaborative_weight=0.7, content_weight=0.3, top_n=5):
    collaborative_recs = collaborative_filtering_recommendations(company, top_n)  # Implement this
    content_recs = content_based_recommendations(customer_input, top_n)  # Implement this
    
    combined_recommendations = defaultdict(float)
    for product in collaborative_recs:
        combined_recommendations[product] += collaborative_weight
    for product in content_recs:
        combined_recommendations[product] += content_weight
    
    final_recommendations = sorted(combined_recommendations.items(), key=lambda x: x[1], reverse=True)
    return [product for product, score in final_recommendations[:top_n]]
