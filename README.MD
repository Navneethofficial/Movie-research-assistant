# 🎬 Movie Research Assistant

A Python-based RAG (Retrieval-Augmented Generation) application that helps users discover information about movies and TV shows, including ratings, cast details, release dates, and trailers.

<p align="center">
  <img src="assets/icon.png" alt="Movie Assistant Icon" width="120">
</p>

## 📋 Overview

Movie Research Assistant is a desktop application that combines modern LLM capabilities with specialized search tools to provide comprehensive information about films and television shows. The system retrieves information from multiple sources and presents it in a clean, intuitive interface.

## ✨ Features

* **Intelligent Queries**: Ask natural language questions about any movie or TV show
* **Comprehensive Movie Data**: Get IMDB ratings, release dates, directors, and cast information
* **Trailer Integration**: Automatically finds and links to official trailers on YouTube
* **Google Search Integration**: Uses the Google Custom Search API for accurate and reliable movie-related information
* **Conversation History**: Full record of your conversation with the assistant
* **Multiple LLM Support**: Switch between different language models based on your needs

## 🔧 Technologies

* **Python & Tkinter**: Lightweight GUI framework for desktop applications
* **RAG Architecture**: Combines search tools with LLM capabilities
* **Groq API**: Fast and efficient LLM inference
* **Google Custom Search API**: Replaces DuckDuckGo for high-quality movie-related web search
* **YouTube API**: For discovering official trailers and video content

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* API keys for:

  * **Groq** (for LLM access)
  * **YouTube API** (for trailer search)
  * **Google Custom Search API + CSE ID** (primary search engine for movies)
  * **(Optional) OMDB API** (for direct structured movie metadata)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/Navneethofficial/Movie-research-assistant.git
   cd movie-research-assistant
   ```

2. Create a virtual environment:
   `python -m venv venv`

3. Activate the environment:

   * Windows: `venv\Scripts\activate`
   * Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:
   `pip install -r requirements.txt`

5. Copy `.env.example` to `.env` and insert your API keys

6. Run the application:
   `python main.py`

## 💻 Usage

1. Type your movie-related question into the input field
2. Hit Enter or press the "Search" button
3. The assistant will:

   * Search for relevant information using **Google Custom Search API**
   * Find a trailer using the **YouTube API**
   * Process retrieved data using the LLM
   * Generate a detailed and accurate response
   * Display all retrieved search results in the conversation history

Example queries:

* **"Who directed Inception and when was it released?"**
* **"Tell me about The Batman"**

## 🧠 How It Works

The application uses a Retrieval-Augmented Generation (RAG) approach:

1. The user's query is processed by the `ConversationManager`
2. Multiple search tools extract relevant information:

   * **Google Search Tool** retrieves movie details, articles, ratings, etc.
   * **YouTube Search Tool** locates the movie's official trailer
3. All retrieved information is assembled into a unified context
4. The Groq-hosted LLM generates a detailed, natural-language response
5. Both raw search results and the final generated answer are shown to the user

## 📁 Project Structure

```
project/
├── main.py               # Application entry point
├── assets/
│   └── icon.png          # Application icon
├── core/
│   ├── conversation.py   # Manages conversation flow and tool calling
│   ├── llm.py            # Interface with Groq LLM API
│   └── search.py         # Search tool implementations (Google + YouTube)
└── ui/
    ├── app.py            # Main application window
    ├── components.py     # UI components and widgets
    └── styles.py         # Application styling and themes
```

## 📸 Screenshots

<p align="center">
  <img src="assets/scr1.png" width="45%" />
  <img src="assets/scr2.png" width="45%" />
</p>

---

## 🛠️ Customization

### Changing the LLM Model

Use the dropdown menu in the interface to switch between these available models:

* **llama-3.1-8b-instant**
* **meta-llama/llama-4-scout-17b-16e-instruct**
* **meta-llama/llama-4-maverick-17b-128e-instruct**

The selected model will automatically be used to generate answers for your movie queries.

---

### Adding New Search Tools

To add a new search tool:

1. Create a new class inheriting from `SearchTool` in `search.py`
2. Implement the `search` method
3. Register the tool inside `RAGApp.setup_tools()` in `app.py`

## 🔜 Future Enhancements

* Image support for high-resolution posters
* Movie comparison engine
* Advanced filtering and ranking of search results

---

