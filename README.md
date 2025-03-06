# 📚Voz-AI: End-to-End Bookstore Voice Assistant with Knowledge Retrieval

This project made for **AiQOD Hackathon 2025**, is an **AI-powered voice assistant** designed to help customers inquire about books, availability, pricing, and stock at a bookstore. Customers can call the assistant, ask natural questions via voice, and receive **dynamic, AI-generated responses** based on real-time book inventory data. The system leverages:

- **Twilio Programmable Voice (Speech-to-Text & Text-to-Speech)**
- **Ollama with LLaMA 3.1** for natural language understanding and generation.
- **Contextual Memory and Friendly Learning** to improve user experience.
- **Flask Backend** for handling webhooks and inventory lookup.

---

## ✨ Key Features

### 🗣️ Voice Interface via Twilio
- Customers interact with the assistant entirely via voice.
- Twilio **Speech-to-Text (STT)** converts speech into text.
- Twilio **Text-to-Speech (TTS)** reads responses back to the caller.

### 📚 Real-Time Knowledge Retrieval
- Current book inventory is stored in `books.csv`.
- Questions about pricing, availability, and stock are answered using this **live data**.

### 🧠 Contextual Memory
- The assistant maintains **short-term memory** during a call session.
- If interrupted, it can recover gracefully and ask the user to repeat or clarify.
- It remembers the current topic within the session (e.g., book being discussed) to provide follow-up information smoothly.

### 🚪 Interruption Handling
- If the user interrupts the assistant while it's speaking, the assistant can pause and listen for the new input.
- This enhances the **natural flow** of conversation.

---

## 📂 Project Structure

```
📂 project-root/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── books.csv              # Sample book inventory
└── README.md              # This documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project-root
```

### 2. Set up Virtual Environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the Inventory Data (csv knowledge base of your choice, We have provided books.csv for bookstore inventory)

Create a `books.csv` file in the root folder with the following format:

```csv
book_name,price,quantity
The Great Gatsby,10.99,5
1984,8.99,10
Moby Dick,12.50,3
```

This is the data the assistant will reference when answering user queries.

---

## 🏃 Running the Application

### Start Flask App
```bash
python app.py
```

The app will run on:
```
http://localhost:5000
```

### Start Ollama
Ensure **Ollama** is running with the required LLaMA model:
```bash
ollama serve
```
You may also need to pull the model if it's not available:
```bash
ollama pull llama3.1
```

---

## 📞 Twilio Integration

### Set Up a Programmable Voice Number
1. Get a free trial **Twilio phone number**.
2. In Twilio Console, set the number’s **Voice Webhook URL** to:
    ```
    https://your-ngrok-url/voice
    ```
3. Use **ngrok** to expose your local Flask server if running locally:
    ```bash
    ngrok http 5000
    ```

---

## 📊 System Flow

1. 📞 **User Calls Twilio Number**  
   The assistant greets the user and invites them to ask a question about books.

2. 🗣️ **User Asks a Question**  
   Twilio converts **speech to text** and sends the transcript to `/handle-input`.

3. 📚 **Knowledge Retrieval & AI Response**  
   - The assistant queries `books.csv` for inventory.
   - The query and data are passed to **LLaMA 3.1** via Ollama.
   - The AI generates a friendly, natural response.

4. 🔊 **AI Response Read Back**  
   Twilio’s **TTS** reads the AI-generated response to the caller.

5. 🔄 **Context Management & Follow-ups**  
   The assistant offers to answer follow-up questions and maintains short-term memory about the current topic.

6. 🚪 **Graceful Interruption Handling**  
   If the user interrupts while the assistant is speaking, the assistant will stop, listen, and respond to the new query.

---



## 🔧 Example Call Flow

```
👤 User: "Hi, do you have The Great Gatsby?"
🤖 Assistant: "Yes! The Great Gatsby is available for $10.99, and we have 5 copies in stock. Would you like me to check another book?"
👤 User: "Actually, do you have 1984?"
🤖 Assistant: "Sure! 1984 is available for $8.99, with 10 copies in stock."
👤 User: (interrupts) "What about Moby Dick?"
🤖 Assistant: "Moby Dick is available for $12.50, and we have 3 copies left. Anything else I can help with?"
```

---

## 📦 Requirements

Dependencies (in `requirements.txt`):
```
flask==2.0.1
twilio==7.16.0
ollama==0.5.13
pandas==2.0.3
numpy==1.21.6
```

---

## 🚀 Future Enhancements

- ✅ Add **multi-language support** using Twilio’s language options.
- ✅ Multi type voice support for user experience.
- ✅ Deploy to cloud platforms 

---

## 📝 License

This project is licensed under the **MIT License**. Feel free to modify and extend it!

---

