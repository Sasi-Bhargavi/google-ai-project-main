&#x20;Epic 1 

1\. Model Selection StrategyInstead of using one massive, expensive model for everything, Epic 1 focuses on task-specific modularity. By utilizing lightweight models tailored to distinct features, the app achieves low latency (fast response times) and cost efficiency.



**Task Modules ----**  **Model Requirement --------  Suggested Gemini FamilyVariant**

**-------------------------------------------------------------------------------------**

Q\&A Chatbot        Fast, conversational        Gemini 1.5 Flash (Lightweight,

&#x20;                  text generation with        incredibly fast, and handles

&#x20;                  solid reasoning             massive context)

&#x20;                  capabilities. 

\--------------------------------------------------------------------------------------

Quiz Generation    Strict structured data      Gemini 1.5 Flash with Structured 

&#x20;                  parsing (e.g., generating   Outputs enabled to enforce exact 

&#x20;                  Multiple Choice Questions   schema matching

&#x20;                  in precise JSON format)

\---------------------------------------------------------------------------------------

Document           Massive token context        Gemini 1.5 Pro or Flash (both 

Summarization      window to ingest entire      natively support up to 1–2 

&#x20;                  textbooks, PDFs, or lecture  million tokens).

&#x20;                  notes without crashing.

\---------------------------------------------------------------------------------------     

2\. Modular Folder ArchitectureTo ensure a seamless frontend, backend, and AI integration that scales well as you add new features, a clean separation of concerns is critical. Below is the recommended modular folder layout for this stack:Plaintext



edugenie-assistant/

│

├── .streamlit/

│   └── secrets.toml          # Securely stores your Gemini API keys locally

│

├── assets/                   # Static model assets, images, or custom configurations

│   └── edugenie\_logo.png

│

├── core/                     # The AI Engine (Backend Logic)

│   ├── \_\_init\_\_.py

│   ├── client.py             # Initializes and authenticates the Google GenAI client

│   ├── prompt\_templates.py   # Stores system instructions and specialized prompts

│   └── models.py             # Task-specific functions (generate\_quiz, summarize\_doc)

│

├── ui/                       # Frontend Presentation Layers

│   ├── \_\_init\_\_.py

│   ├── chat\_interface.py     # Streamlit code for the conversational Q\&A screen

│   ├── quiz\_interface.py     # Streamlit layout for interactive testing and grading

│   └── summary\_interface.py  # File upload handlers and display logic

│

├── .gitignore                # Prevents secrets.toml and virtual environments from pushing to Git

├── app.py                    # Main Entry Point (Launches the Streamlit app sidebar/navigation)

├── requirements.txt          # Python package dependency list (streamlit, google-generativeai)

└── README.md                 # Project documentation and setup instructions





Why this structure works:

* **Separation of Concerns:** If you want to change how a prompt behaves or switch an AI model, you edit core/prompt\_templates.py or core/models.py. The frontend user interface code in ui/ remains entirely untouched.
* **Scalability:** If you decide to add a new feature later (like an "Essay Grader"), you simply create an essay\_interface.py in the UI folder and a matching function in the Core folder.



































