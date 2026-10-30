# AI Meeting Intelligence — AI-Powered Meeting Intelligence System

Turn meeting transcripts, audio recordings, and video recordings into structured, actionable meeting reports.

**AI Meeting Intelligence** is a Python and Streamlit application that uses speech-to-text transcription and a large language model (LLM) to extract meeting summaries, discussion points, confirmed decisions, action items, additional insights, and open questions. Users can review the transcript before analysis and export results as TXT or PDF reports.

> **Project status:** Core application works locally. Large-recording processing, broader automated testing, and public deployment are planned improvements.

## Features

- **Three input modes:** paste a transcript, upload an audio recording, or upload a video recording.
- **Speech-to-text:** transcribe supported audio with Groq's Whisper API.
- **Video transcription:** extract a video's audio track with MoviePy, then transcribe it.
- **Transcript review:** edit recognized speech before running analysis.
- **Structured meeting analysis:** generate a summary, discussion points, confirmed decisions, action items, additional insights, and open questions.
- **Action-item details:** extract task, owner, and deadline where supported by the transcript; use `Not specified` when necessary.
- **Accuracy-focused prompts:** distinguish confirmed decisions from proposals and preserve uncertainty rather than inventing facts.
- **Response validation:** parse and validate structured JSON returned by the LLM.
- **Report downloads:** export meeting results to TXT and formatted PDF (ReportLab).
- **Input safeguards:** basic file-size validation, error handling, and application logging.

## Technology Stack

| Area | Technology |
| --- | --- |
| Language | Python |
| Web interface | Streamlit |
| LLM analysis | Groq API (`openai/gpt-oss-120b` in the current project configuration) |
| Speech-to-text | Groq Whisper (`whisper-large-v3-turbo`) |
| Video audio extraction | MoviePy |
| PDF reports | ReportLab |
| Configuration | python-dotenv |
| Validation and processing | Python, JSON |
| Diagnostics | Python `logging` |
| Version control | Git and GitHub |

## How It Works

```text
Paste transcript ───────────────────────┐
                                       │
Upload audio ──> Whisper transcription ├──> Review / edit transcript
                                       │                 │
Upload video ──> Extract audio ────────┘                 │
                   │                                     │
                   └──> Whisper transcription ───────────┘
                                                         │
                                                         v
                                                Clean transcript
                                                         │
                                                         v
                                                Groq LLM analysis
                                                         │
                                                         v
                                             Parse and validate JSON
                                                         │
                                                         v
                                             Display structured report
                                                         │
                                                         v
                                                Download TXT / PDF
```

The analysis is designed to extract only information supported by the supplied transcript. As with any LLM-based system, results should be reviewed for accuracy before use in consequential workflows.

## Report Sections

1. **Meeting Summary** — concise overview of the discussion.
2. **Discussion Points** — main topics covered.
3. **Key Decisions** — explicitly confirmed choices or agreements.
4. **Action Items** — concrete tasks, owners, and deadlines when available.
5. **Additional Meeting Insights** — relevant risks, blockers, requirements, milestones, dependencies, or other supported insights.
6. **Open Questions** — unresolved questions identified from the conversation.

## Project Structure

```text
AI Meeting Intelligence/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env                    # Local only; do not commit
├── test_validation.py
└── services/
    ├── llm_service.py
    ├── transcription_service.py
    ├── video_service.py
    ├── validation.py
    ├── file_validation.py
    └── report_service.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Techie-Akanksha/AI-Meeting-Intelligence.git
cd AI-Meeting-Intelligence
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure `requirements.txt` includes the project's current dependencies, including `streamlit`, `groq`, `python-dotenv`, `moviepy`, and `reportlab`. Video processing may require a working FFmpeg installation or MoviePy's compatible FFmpeg setup.

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` or share your API key publicly. The repository's `.gitignore` should exclude `.env` and other local artifacts.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Usage

1. Choose **Paste Transcript**, **Upload Audio**, or **Upload Video**.
2. Provide the meeting content. Audio and video uploads are transcribed before analysis.
3. Review and correct the transcript if needed.
4. Select **Analyze Meeting**.
5. Review the generated meeting sections.
6. Download the report as **TXT** or **PDF**.

## Validation and Testing

The project includes `test_validation.py` for structured-response validation. Run it according to the test file's implementation, for example:

```bash
python test_validation.py
```

Manual tests performed during development include transcript input, audio transcription, video transcription, action-item extraction, missing owners/deadlines, invalid JSON handling, and TXT/PDF exports. Basic upload-size validation has also been exercised with an oversized file.

**Still to improve:** automated coverage for media failures, larger recordings, report layout edge cases, and session-state behavior.

## Current Limitations

- The application currently applies a **25 MB input-file limit** to audio/video uploads.
- A compressed video can produce a larger extracted audio file; extracted-audio limits and large-recording processing need further work.
- Audio compression and chunked transcription for long recordings are **not yet implemented**.
- Speech recognition can mishear names, technical terminology, or speaker labels.
- LLM-generated insights can contain mistakes despite prompt constraints and JSON validation; review results before relying on them.
- Public deployment is **not yet confirmed**; the application has been tested locally.
- Meeting content is sent to an external API for transcription and/or analysis. Do not upload confidential recordings without appropriate authorization and review of the provider's data-handling terms.

## Planned Improvements

- Efficient audio encoding and chunked transcription for larger recordings.
- Additional automated tests and stronger session-state handling.
- Better progress feedback and media-processing error messages.
- Further PDF formatting and accessibility improvements.
- Secure public deployment and end-to-end deployment testing.

## What I Learned

Building AI Meeting Intelligence provided practical experience with integrating external AI APIs, converting unstructured speech and text into structured data, writing accuracy-focused prompts, validating LLM outputs, managing media files, handling errors, and generating downloadable reports. The project also reinforced modular Python design and incremental testing.

## Repository

[AI Meeting Intelligence on GitHub](https://github.com/Techie-Akanksha/AI-Meeting-Intelligence)

---

**Note:** This is a portfolio and learning project. It is not a substitute for human review of meeting decisions, commitments, or records.
