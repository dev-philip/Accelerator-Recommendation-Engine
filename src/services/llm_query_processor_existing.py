import pandas as pd
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from src.hybrid_recommendation import hybrid_recommendations  # Import the function for existing customer recommendations

# Load the accelerators and products data
accelerators_df = pd.read_excel('data/accelerators.xlsx')
products_df = pd.read_excel('data/products.xlsx')

# Merge accelerators and products
merged_df = pd.merge(accelerators_df, products_df, how='left', left_on='Product', right_on='Name')

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", openai_api_key="")

# Define schema for output
class RouteQuery(TypedDict):
    """Route query to appropriate destination."""
    destination: Literal["recommendation", "product_info"]

# Define routing system prompt
def get_route_prompt() -> ChatPromptTemplate:
    """Returns the routing prompt template."""
    route_system = """
    You are a smart assistant that can route user queries. Based on the input, decide if the user needs:
    - "recommendation" if the query is about product suggestions.
    - "product_info" if the query is about product details.
    Respond only with one of these categories as the destination.
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", route_system),
            ("human", "{query}"),
        ]
    )

# Function to search for relevant accelerator/product information
def search_accelerator_data(user_input: str, df: pd.DataFrame) -> str:
    """Searches the DataFrame for relevant accelerator data."""
    # Filter the DataFrame to match user_input
    relevant_data = df[df['Name_x'].str.contains(user_input, case=False, na=False)]
    
    if not relevant_data.empty:
        # Format relevant rows into a human-readable context
        context = relevant_data.to_string(index=False, header=False)
    else:
        context = "No relevant data found."
    
    return context

# Function to create a dynamic prompt template
def get_prompt_template(user_input: str, context: str) -> str:
    """Generates a prompt with user query and relevant context."""
    prompt_template = f"""
    You are an assistant. Based on the user's query, provide any information about Accelerator and product data that you have.
    
    Accelerator and product data: {context}
    
    User query: {user_input}
    Response:
    """
    return prompt_template

# Function to fetch accelerator data
def fetch_accelerator_data(user_input: str) -> str:
    """Fetches accelerator data and generates a response."""
    # Search for relevant data
    context = search_accelerator_data(user_input, merged_df)
    
    # Generate the prompt with the accelerator context
    prompt_text = get_prompt_template(user_input, context)
    
    # Use the prompt with the LLM
    prompt = PromptTemplate(input_variables=["input"], template=prompt_text)
    chain = prompt | llm
    
    # Invoke the chain to get a response
    parsed_input = chain.invoke({"input": user_input})
    
    # Ensure the response is converted to a string
        # Extract and return only the content
    if hasattr(parsed_input, 'content'):
        return parsed_input.content
    else:
        return str(parsed_input)  # Fallback in case 'content' is not present


# Function to retrieve product information
def retrieve_product_info(user_input: str) -> str:
    """Retrieves product information based on user input."""
    return fetch_accelerator_data(user_input)

# Define recommendation logic
def recommend_product(company: str, query: str) -> str:
    """Simulates product recommendation logic."""
    # Replace with your recommendation algorithm
    return hybrid_recommendations(company, query)

# Routing logic
def route_query(query: str) -> RouteQuery:
    """Uses LLM to determine where the query should be routed."""
    route_prompt = get_route_prompt()
    routing_chain = route_prompt | llm.with_structured_output(RouteQuery)
    result = routing_chain.invoke({"query": query})
    return result

# Handling logic
def handle_query(routing_result: RouteQuery, company: str,  query: str) -> str:
    """Handles the query based on the routing result."""
    if routing_result["destination"] == "recommendation":
        return recommend_product(company, query)
    elif routing_result["destination"] == "product_info":
        return retrieve_product_info(query)
    else:
        raise ValueError(f"Unexpected destination: {routing_result['destination']}")

# Main logic
def process_query_existing(company: str, query: str) -> str:
    """Processes the user query end-to-end."""
    routing_result = route_query(query)
    return handle_query(routing_result, company, query)
