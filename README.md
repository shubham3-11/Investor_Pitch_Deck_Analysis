# Pitch Deck Analysis App

A web application for investors to upload pitch decks (PDF), automatically extract and summarize content, score claims, and generate follow-up questions using LLMs.

## Tech Stack

- **Backend**: Python, FastAPI, SQLModel (SQLite), APScheduler, OpenAI API
- **Frontend**: React, TypeScript, Vite

## Setup and Running

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API Key

### Backend

1. Navigate to `backend` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your API key:
   Create a `.env` file in the `backend` directory:
   ```bash
   GEMINI_API_KEY="your-gemini-key"
   # or
   OPENAI_API_KEY="sk-..."
   ```

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
   The background job scheduler starts automatically with the app.

### Frontend

1. Navigate to `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

## Usage Flow

1. Open the frontend app.
2. Create a new "Startup" profile.
3. Go to the Startup details page and upload a PDF pitch deck.
4. The backend will accept the file and queue it for processing.
5. A background job (running every minute) will:
   - Extract text from the PDF.
   - Summarize the content using GPT-4o-mini.
   - Extract claims and score their plausibility.
   - Generate follow-up questions.
6. Refresh the Deck Analysis page to see the results once processing is complete.
