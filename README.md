# MeetMind AI — Meeting Intelligence Workspace

MeetMind AI is an AI-powered meeting analysis application that transforms meeting transcripts into structured, actionable insights. It helps users review discussions, identify key decisions, and organize follow-up tasks without manually going through the entire transcript.

## Features

- **Meeting Summary:** Generates a concise summary of the meeting.
- **Discussion Points:** Extracts the main topics discussed.
- **Key Decisions:** Identifies decisions and agreements mentioned in the transcript.
- **Action Item Extraction:** Identifies tasks and their associated owners and deadlines when available.
- **Input Validation:** Prevents analysis when the transcript is empty.
- **Structured AI Output:** Uses JSON to organize meeting insights into separate fields.
- **Error Handling:** Handles invalid JSON responses and unexpected runtime or API errors.
- **Logging:** Records diagnostic information to help troubleshoot application errors.
- **Interactive Web Interface:** Built with Streamlit and styled with custom HTML and CSS.

## How It Works

1. **Enter a Transcript:** The user pastes a meeting transcript into the application.
2. **Preprocess the Text:** The application cleans unnecessary whitespace.
3. **Construct the Prompt:** A task-specific prompt instructs the language model to extract meeting insights using the transcript as its source.
4. **Generate Insights:** The application sends the prompt to the Groq API.
5. **Parse the Response:** Python's JSON module converts the model's JSON response into a Python data structure.
6. **Validate and Display Results:** The application checks the response structure and displays the summary, discussion points, decisions, and action items.
7. **Handle Errors:** Exceptions are logged, and user-friendly error messages are displayed when processing fails.

## Technology Stack

- **Programming Language:** Python
- **Frontend and UI:** Streamlit, HTML, CSS
- **LLM API:** Groq API
- **Language Model:** `openai/gpt-oss-120b`
- **JSON Processing:** Python `json` module
- **Logging:** Python `logging` module
- **Environment Configuration:** `python-dotenv`
- **Version Control:** Git and GitHub

## Project Structure

```text
AI Meeting Intelligence/
├── services/
│   └── llm_service.py
├── app.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

The `.env` file is used for local configuration and must not be committed to version control. The `app.log` file is generated at runtime and is excluded through `.gitignore`.

## Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- A Groq API key
- Git (optional, for cloning the repository)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Techie-Akanksha/MeetMind-AI.git
cd "AI Meeting Intelligence"
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY= your_groq_api_key_here
```

Replace the placeholder with your own API key. Keep the key private and never commit the `.env` file.

### 5. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL that you can open in your browser.

## Example Output

After analyzing a meeting transcript, MeetMind AI displays:

- Meeting Summary
- Discussion Points
- Key Decisions
- Action Items, including task, owner, and deadline where available

The extracted results depend on the transcript and the language model's response.

## Error Handling and Validation

The application includes:

- Empty transcript validation before making an API request
- JSON parsing error handling
- Response-structure validation
- General exception handling for unexpected failures
- Logging to support debugging

The model can occasionally misinterpret information or generate unsupported details. Outputs should be reviewed against the original transcript, especially before relying on extracted decisions or action items.

## Current Limitations

- The application requires an internet connection and a working Groq API key.
- The quality of extracted insights depends on the transcript and model response.
- The application does not guarantee that every generated decision, owner, or deadline is correct.
- Users should verify important action items against the original meeting transcript.

## Future Enhancements

- Upload meeting transcript files.
- Export meeting summaries and action items.
- Add transcript history and searchable records.
- Improve evidence-based validation of decisions and action items.
- Support additional transcript formats and languages.

## Security

- Store API credentials in environment variables.
- Keep `.env` out of Git.
- Avoid committing logs, virtual environments, and Python cache files.
- Review AI-generated content before using it for important decisions.

