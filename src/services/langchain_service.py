from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
import pandas as pd

# Load the accelerators and products data
accelerators_df = pd.read_excel('data/accelerators.xlsx')
products_df = pd.read_excel('data/products.xlsx')

# Merge accelerators and products on "Product" from accelerators_df and "Name" from products_df
merged_df = pd.merge(accelerators_df, products_df, how='left', left_on='Product', right_on='Name')

# LangChain setup for conversation
llm = OpenAI(openai_api_key='')

# Function to retrieve relevant accelerator/product information
def fetch_accelerator_data(accelerator_name):
    accelerator_info = merged_df[merged_df['Name_x'].str.contains(accelerator_name, case=False)]
    
    if not accelerator_info.empty:
        accelerator_desc = accelerator_info.iloc[0]['Short description']
        product_name = accelerator_info.iloc[0]['Product']
        product_category = accelerator_info.iloc[0]['Category'] if 'Category' in accelerator_info else "N/A"
        product_desc = accelerator_info.iloc[0]['Description']
        return f"Accelerator: {accelerator_name}\nShort Description: {accelerator_desc}\nRelated Product: {product_name}\nCategory: {product_category}\nProduct Description: {product_desc}"
    else:
        return f"Sorry, I couldn't find any information on {accelerator_name}."

# Create dynamic prompt template with context
def get_prompt_template(user_input, accelerator_context=""):
    prompt_template = f"""
    You are an assistant. Based on the user's query, provide either accelerator recommendations or detailed information about specific accelerators and related products.
    If the user asks for accelerators we offer, generate a list of accelerators from the provided data and ask them if they want some explanation on them.
    If the user asks for information on a specific accelerator, retrieve the details from the provided data.
    
    Accelerator and product data: {accelerator_context}
    
    User query: {user_input}
    Response:"""
    
    return prompt_template

# Function to process user input using LangChain
def process_user_input(user_input):
    # Check if user is asking about a specific accelerator
    relevant_accelerators = [name for name in merged_df['Name_x'] if name.lower() in user_input.lower()]
    
    # If there's a specific accelerator in the query, fetch its data
    if relevant_accelerators:
        accelerator_name = relevant_accelerators[0]  # Assume one for simplicity
        accelerator_context = fetch_accelerator_data(accelerator_name)
    else:
        accelerator_context = "No specific accelerator data provided."
    
    # Generate the prompt with the accelerator context
    prompt_text = get_prompt_template(user_input, accelerator_context)
    
    # Use the prompt with the LLM
    prompt = PromptTemplate(input_variables=["input"], template=prompt_text)
    chain = prompt | llm
    
    # Invoke the chain to get a response
    parsed_input = chain.invoke({"input": user_input})
    
    return parsed_input

# Example of chatting and getting recommendations or information
user_query = "Tell me about ActiveCampaign"

# Get response based on user query
response = process_user_input(user_query)

print(f"Response based on user query '{user_query}':\n{response}")
