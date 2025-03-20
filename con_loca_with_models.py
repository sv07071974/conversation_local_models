Do. SIMILAR THING for the following code 

"# Import required libraries
import requests  # For making HTTP requests to the Ollama API
import json     # For JSON data handling
import time     # For adding delays between API calls
from IPython.display import clear_output, display, HTML  # For notebook display formatting
from typing import List, Dict  # For type hints

# Define the API endpoint for Ollama local server
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}  # Set request headers for JSON data

# Define personality prompts for each chatbot model
# Each personality has a specific behavior pattern and response style
PERSONALITIES = {
    "gemma": """You are a chatbot who is very argumentative. You disagree with anything in the 
    conversation and you challenge everything, in a snarky way. Keep responses under 50 words.""",
    
    "qwen:7b": """You are a very polite, courteous chatbot. You try to agree with everything the other 
    person says, or find common ground. If others are argumentative, you try to calm them down. 
    Keep responses under 50 words.""",
    
    "mistral": """You are a neutral and analytical chatbot who tries to mediate discussions with 
    logic and reason. You aim to find balanced perspectives and encourage productive dialogue. 
    Keep responses under 50 words."""
}

def display_message(model: str, message: str):
    """
    Display a message with color-coded styling in the Jupyter notebook.
    
    Args:
        model (str): The name of the chatbot model
        message (str): The message content to display
    
    Note:
        - Uses different background colors for each personality type
        - Argumentative (gemma): Light red
        - Polite (qwen:7b): Light green
        - Neutral (mistral): Light blue
    """
    colors = {
        "gemma": "#FF9999",    # Light red for argumentative personality
        "qwen:7b": "#99FF99",  # Light green for polite personality
        "mistral": "#9999FF"   # Light blue for neutral personality
    }
    
    # Create HTML-formatted message with styling
    html = f"""
    <div style="margin: 10px 0; padding: 10px; border-radius: 5px; background-color: {colors.get(model.lower(), '#FFFFFF')}">
        <strong>{model.upper()}:</strong> {message}
    </div>
    """
    display(HTML(html))

def get_model_response(model: str, messages: List[Dict], retries: int = 3) -> str:
    """
    Get response from an Ollama model with retry mechanism for reliability.
    
    Args:
        model (str): The name of the model to query
        messages (List[Dict]): List of conversation messages
        retries (int): Number of retry attempts (default: 3)
    
    Returns:
        str: The model's response or error message
        
    Note:
        - Implements retry mechanism for handling temporary failures
        - Waits 1 second between retry attempts
    """
    for attempt in range(retries):
        try:
            # Prepare the request payload
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            # Send request to Ollama API
            response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
            if response.status_code == 200:
                return response.json()["message"]["content"]
            
        except Exception as e:
            if attempt == retries - 1:
                return f"{model} is currently unavailable: {str(e)}"
            time.sleep(1)  # Wait before retrying
    
    return f"Failed to get response from {model} after {retries} attempts."

def run_conversation(topic: str, turns: int = 3):
    """
    Run a multi-turn conversation between the models about a given topic.
    
    Args:
        topic (str): The conversation topic
        turns (int): Number of conversation turns (default: 3)
        
    Note:
        - Initializes separate conversation histories for each model
        - Updates all models with each other's responses
        - Includes delays between turns for readability
    """
    # Initialize conversation histories for each model with their personality prompts
    conversations = {
        model: [{"role": "system", "content": prompt}] 
        for model, prompt in PERSONALITIES.items()
    }
    
    # Display the conversation topic
    display(HTML(f"<h3>Conversation Topic: {topic}</h3>"))
    display(HTML("<hr>"))
    
    # Get initial responses from each model about the topic
    for model in conversations.keys():
        messages = conversations[model] + [
            {"role": "user", "content": f"The topic is: {topic}. Share your initial thoughts."}
        ]
        
        # Get and display the model's response
        response = get_model_response(model, messages)
        display_message(model, response)
        
        # Update all models' conversation histories with this response
        for conv in conversations.values():
            conv.append({"role": "user", "content": f"{model} said: {response}"})
    
    # Continue conversation for specified number of turns
    for turn in range(turns):
        display(HTML(f"<h4>Turn {turn + 1}</h4>"))
        
        # Get responses from each model
        for model in conversations.keys():
            response = get_model_response(model, conversations[model])
            display_message(model, response)
            
            # Update all models' conversation histories with this response
            for conv in conversations.values():
                conv.append({"role": "user", "content": f"{model} said: {response}"})
        
        time.sleep(1)  # Add delay between turns for readability

# Define conversation topics
topics = [
    "Should AI be used in education?",
    "Is social media good for society?",
    "Should we colonize Mars?",
    "Are electric vehicles the future of transportation?",
    "Should remote work be the new normal?"
]

# Example usage for a single topic
run_conversation("Should AI be used in education?", turns=2)
