from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import csv
import logging
import traceback
import ollama
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(_name_)

app = Flask(_name_)

# Load books into a Pandas DataFrame
def load_books():
    try:
        df = pd.read_csv('books.csv')
        logger.debug(f"Successfully loaded {len(df)} books")
        return df
    except Exception as e:
        logger.error(f"Error loading books: {str(e)}")
        logger.error(traceback.format_exc())
        return pd.DataFrame()  # Return empty DataFrame in case of error

# Query LLaMA with Ollama
def query_llama(user_query, books):
    # Convert books dataframe to a structured text format
    book_list = "\n".join([f"{row['book_name']} - ${row['price']}, {row['quantity']} in stock" for _, row in books.iterrows()])

    prompt = f"""
    You are a friendly and knowledgeable AI assistant for a bookstore. Your job is to provide quick and helpful answers about book availability, pricing, and stock.  

    Here is the current book inventory:  
    {book_list}  

    The user asked: "{user_query}"  

    Respond in a natural, conversational manner. Keep your answer concise, engaging, and helpful. Avoid repeating the user's question—just provide the relevant information clearly and warmly.
    """


    try:
        response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        logger.error(f"Error querying LLaMA 3.1: {str(e)}")
        return "I'm sorry, but I couldn't retrieve that information right now."

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            logger.debug("Received POST request to root")
            logger.debug(f"Request values: {request.values}")
            resp = VoiceResponse()
            gather = Gather(input='speech', action='/handle-input', method='POST', speechTimeout='auto', enhanced='true')
            gather.say("Hello! I'm your book store assistant. You can ask me about available books or specific book prices. How can I help you today?")
            resp.append(gather)
            return str(resp)
        except Exception as e:
            logger.error(f"Error in root endpoint: {str(e)}")
            logger.error(traceback.format_exc())
            resp = VoiceResponse()
            resp.say("We're sorry, but there was an error. Please try again later.")
            return str(resp)
    return "Book Store Voice Assistant is running! Access /voice endpoint for Twilio integration."

@app.route("/voice", methods=['POST'])
def voice():
    try:
        logger.debug("Received voice request")
        logger.debug(f"Request values: {request.values}")
        
        resp = VoiceResponse()
        gather = Gather(input='speech', action='/handle-input', method='POST', speechTimeout='auto', enhanced='true')
        gather.say("Hello! I'm your book store assistant. You can ask me about available books or specific book prices. How can I help you today?")
        resp.append(gather)
        
        response = str(resp)
        logger.debug(f"Generated response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in voice endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        resp = VoiceResponse()
        resp.say("We're sorry, but there was an error. Please try again later.")
        return str(resp)

@app.route("/handle-input", methods=['POST'])
def handle_input():
    try:
        logger.debug("Received handle-input request")
        logger.debug(f"Request values: {request.values}")
        
        books = load_books()
        user_input = request.values.get('SpeechResult', '').lower()
        logger.debug(f"User input: {user_input}")
        
        resp = VoiceResponse()
        gather = Gather(input='speech', action='/handle-input', method='POST', speechTimeout='auto', enhanced='true')

        if not user_input:
            gather.say("I didn't catch that. Could you please repeat your question?")
        else:
            # Use Ollama to query book inventory with AI
            response_text = query_llama(user_input, books)
            gather.say(response_text)

        gather.say("Is there anything else you'd like to know?")
        resp.append(gather)
        
        response = str(resp)
        logger.debug(f"Generated response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in handle-input endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        resp = VoiceResponse()
        resp.say("We're sorry, but there was an error. Please try again later.")
        return str(resp)

if _name_ == "_main_":
    app.run(debug=True, port=5000)
