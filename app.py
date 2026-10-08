import streamlit as st
import json
from services.llm_service import ask_llm

st.title("MeetMind AI")
st.write("AI-powered Meeting Intelligence System")

transcript = st.text_area(
    "Enter your meeting transcript",
    height=200,
    placeholder="Paste your meeting transcript here..."
)


def clean_transcript(text):
    return " ".join(text.split())


cleaned_transcript = clean_transcript(transcript)

prompt = f"""
You are an AI Meeting Assistant.

Analyze the meeting transcript provided below.

Your tasks:
1. Generate a concise meeting summary.
2. Identify the main discussion points.
3. Identify key decisions made during the meeting.
4. Identify action items and the person responsible, if explicitly mentioned.
5. Identify deadlines only if explicitly mentioned.

Rules:
- Use only information present in the transcript.
- Do not invent facts, names, deadlines, decisions, or responsibilities.
- Assign responsibility only when the transcript explicitly assigns it.
- The person who mentions or suggests an action is not automatically responsible.
- Identify deadlines only when explicitly mentioned.
- If information is not available, write "Not specified".
- Keep the output clear and concise.

Return the result as valid JSON using exactly this structure:

{{
    "summary": "...",
    "discussion_points": [],
    "decisions": [],
    "action_items": [
        {{
            "task": "...",
            "person": "...",
            "deadline": "..."
        }}
    ]
}}

Meeting Transcript:
{cleaned_transcript}
"""

if st.button("Analyze Meeting"):

    if not transcript.strip():
        st.warning("Please enter a meeting transcript before analyzing.")

    else:
        with st.spinner("Analyzing the meeting..."):

            try:
                result = ask_llm(prompt)

                meeting_data = json.loads(result)

                st.subheader("📝 Meeting Summary")
                st.write(meeting_data["summary"])

                st.subheader("💬 Discussion Points")
                for point in meeting_data["discussion_points"]:
                    st.write("•", point)

                st.subheader("✅ Key Decisions")
                for decision in meeting_data["decisions"]:
                    st.write("•", decision)

                st.subheader("📌 Action Items")
                st.table(meeting_data["action_items"])

            except json.JSONDecodeError:
                st.error(
                    "The AI returned an invalid response format. Please try again."
                )

            except Exception:
                st.error(
                    "Something went wrong while analyzing the meeting. Please try again."
                )