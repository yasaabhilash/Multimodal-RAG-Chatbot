🤖 Multimodal RAG Chatbot

An intelligent, conversational AI chatbot that combines Retrieval-Augmented Generation (RAG) with multimodal capabilities to understand and retrieve information from both documents and images.

Upload your own files, ask questions in natural language, and get context-aware answers grounded in your data, complete with source references.


📸 Screenshots
Chat Interface

Document Q&A and image understanding in one conversation. Every answer lists the sources it was drawn from (file name and page).

Chat Interface

<img width="549" height="950" alt="conversational-memory" src="https://github.com/user-attachments/assets/1a5d9a21-1d28-46cc-b51f-46e5b4fd9b72" />

Conversational Memory

The chatbot follows up on earlier messages, reasons over retrieved policy content, and remembers details shared in the conversation.

Conversational Memory


<img width="1337" height="1031" alt="upload-and-image-query" src="https://github.com/user-attachments/assets/f4948714-f396-4cbf-9bd2-288245cf0419" />

Uploading Documents and Images

Files are uploaded straight from the interface, then become searchable through chat.

Upload and Image Query


<img width="731" height="942" alt="chat-interface" src="https://github.com/user-attachments/assets/1670906c-8d4e-4367-bbae-801c80994f35" />


🚀 Features
Conversational AI: Handles natural conversation, greetings, compliments, and contextual follow-up questions.
Multimodal Retrieval: Processes both textual documents and images to find relevant information.
Document Processing: Supports PDF, DOCX, and XLSX files.
Image Understanding: Analyzes uploaded images and answers questions such as "What did you see in this image?"
Semantic Search: Retrieves information by meaning and context rather than keyword matching.
Source Attribution: Responses list the file and page they were retrieved from.
Context-Aware Responses: Answers are grounded in retrieved content rather than generated from scratch.
Chat Management: Create new chats, rename, archive, unarchive, and delete conversations, with history preserved per session.
Modular Architecture: Document processing, retrieval, image processing, and response generation are independent components.
Modern UI: Interactive React-based chat interface with a dark theme.
🏗️ System Architecture
text
                 USER
                  |
                  v
          REACT FRONTEND
                  |
                  v
            FASTAPI BACKEND
                  |
          +-------+-------+
          |               |
          v               v
   DOCUMENT PIPELINE  IMAGE PIPELINE
          |               |
          v               v
   TEXT EXTRACTION    IMAGE PROCESSING
          |               |
          v               v
   CHUNKING &         VISUAL FEATURE
   EMBEDDINGS         EXTRACTION
          |               |
          v               v
   VECTOR STORAGE     IMAGE INDEX
          |               |
          +-------+-------+
                  |
                  v
           RETRIEVAL SYSTEM
                  |
                  v
          CONTEXT GENERATION
                  |
                  v
             LLM / VISION
                  |
                  v
          CONTEXTUAL RESPONSE
                  |
                  v
             USER INTERFACE
🛠️ Technology Stack
Component	Technology
Backend	Python, FastAPI
Frontend	React.js, Vite
API Communication	REST APIs
Document Processing	PDF, DOCX, XLSX processing
AI / NLP	Embeddings, LLMs, RAG
Image Processing	Python-based image processing and vision models
Dependency Management	pip, npm
Version Control	Git, GitHub
📂 Project Structure
text
Multimodal-RAG-Chatbot/
│
├── backend/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   ├── registry/
│   ├── main.py
│   ├── rag.py
│   ├── chat_manager.py
│   ├── config.py
│   └── image_processor.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── screenshots/
│
├── requirements.txt
└── README.md
⚙️ Installation and Setup
Prerequisites
Python 3.11
Node.js and npm
Git
1. Clone the Repository
bash
git clone https://github.com/yasaabhilash/Multimodal-RAG-Chatbot.git
cd Multimodal-RAG-Chatbot
2. Set Up the Backend

Create and activate a virtual environment:

bash
python -m venv venv

Windows:

powershell
venv\Scripts\activate

macOS / Linux:

bash
source venv/bin/activate

Install dependencies:

bash
pip install -r requirements.txt

Start the FastAPI backend:

bash
uvicorn backend.main:app --reload
3. Set Up the Frontend

Open a second terminal:

bash
cd frontend
npm install
npm run dev

Open the local URL shown in the terminal to use the application.

Note: Configure model settings, API credentials, and backend/frontend connection URLs in the appropriate configuration files (e.g. backend/config.py) before running the application.

💡 How It Works
Upload: Users upload documents or images through the React interface.
Processing: The backend extracts text from documents and processes visual content from images.
Indexing: Processed content is converted into searchable representations and stored in the relevant indexes.
Querying: Users ask questions in natural language.
Retrieval: The retrieval system finds the most relevant text chunks and images.
Generation: The language model uses the retrieved context to produce a grounded answer.
Conversation: The response, along with its sources, is returned to the frontend so the conversation can continue.
🎯 Project Objective

To build a conversational AI system that goes beyond traditional text-only chatbots by combining document retrieval, image understanding, and contextual conversation in a single application, making it more intuitive to interact with your own data through natural language.

🔮 Future Improvements
Improve multimodal retrieval accuracy, especially choosing the right image when several are indexed.
Add support for additional document formats.
Optimize indexing and retrieval performance.
Enhance conversational memory and context management.
Improve response grounding and source attribution (including page numbers for all file types).
Add user authentication and personalized workspaces.
👨‍💻 Author

Abhilash Yasa

GitHub: @yasaabhilash

Built as an exploration of Retrieval-Augmented Generation, multimodal AI, and conversational systems.
