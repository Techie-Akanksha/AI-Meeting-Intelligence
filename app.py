
import streamlit as st
import json
import logging

from services.llm_service import ask_llm


# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="MeetMind AI",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """<style>
        .page-title {
            text-align: center;
        }
        .page-subtitle {
            text-align: center;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
    </style>""",
    unsafe_allow_html=True
)

st.markdown( 
    '<h1 class="page-title">🧠 MeetMind AI</h1>',
    unsafe_allow_html=True
)

st.markdown( 
    '<p class="page-subtitle">Turn meeting transcripts into structured summaries key decisions, and actionable tasks.</p>',
    unsafe_allow_html=True
)


st.divider()



st.subheader("📄 Meeting Transcript")
st.caption(
    "Paste your meeting conversation below to generate "
    "a summary, decisions, and action items."
)

with st.container(border=True):
    transcript = st.text_area(
        "Enter your meeting transcript",
        height=200,
        placeholder=(
            "Example:\n"
            "Priya: Please prepare the project report by Friday.\n"
            "Rahul: Sure, I'll complete it by Friday."
        )
    )


# Clean transcript
def clean_transcript(text):
    return " ".join(text.split())


cleaned_transcript = clean_transcript(transcript)


# Prompt for meeting analysis
prompt = f"""
You are an AI Meeting Assistant.

Analyze the meeting transcript provided below.

Your tasks:
1. Generate a concise meeting summary.
2. Identify the main discussion points.
3. Identify key decisions actually made.
4. Identify concrete action items and their responsible persons.
5. Identify deadlines only if explicitly mentioned.

Rules:
- Use only information present in the transcript.
- Never invent facts, names, deadlines, decisions, or responsibilities.
- Assign responsibility only when explicitly stated.
- The person who mentions or suggests an action is not automatically responsible.
- A decision must be an actual choice or agreement, not just a suggestion.
- General ideas, possibilities, and topics for future discussion are not automatically decisions or action items.
- Include an action item only when a concrete task or commitment is clearly established.
- Phrases such as "we could consider" or "maybe we should" do not automatically establish a commitment.
- A clear team commitment can be an action item even if no individual owner is named.
- Use "Not specified" for the person or deadline only when a concrete action item exists but that detail is missing.
- If there are no discussion points, decisions, or action items, return an empty array [] for that field.
- Never put "Not specified" inside the discussion_points or decisions arrays.
- Keep the output concise.
- Return valid JSON only. Do not include Markdown fences or explanations.

Return the result using exactly this structure:

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


# Analyze meeting
if st.button("🚀 Analyze Meeting", type="secondary", use_container_width=True):
    if not transcript.strip():
        st.warning("Please enter a meeting transcript before analyzing.")

    else:
        with st.spinner("Analyzing the meeting..."):

            try:
                # Call the LLM
                result = ask_llm(prompt)

                # Convert JSON text into a Python dictionary
                meeting_data = json.loads(result)

                # Validate the response structure
                if not isinstance(meeting_data, dict):
                    raise ValueError("The response must be a JSON object.")

                list_fields = [
                    "discussion_points",
                    "decisions",
                    "action_items"
                ]

                for field in list_fields:
                    if not isinstance(meeting_data.get(field, []), list):
                        raise ValueError(
                            f"The '{field}' field must be a list."
                        )

                logger.info("Meeting analysis completed successfully.")

                # Display summary
                st.subheader("📝 Meeting Summary")
                st.write(
                    meeting_data.get("summary") or "No summary available."
                )

                # Display discussion points
                st.subheader("💬 Discussion Points")

                discussion_points = [
                    point
                    for point in meeting_data.get("discussion_points", [])
                    if isinstance(point, str)
                    and point.strip()
                    and point.strip().lower() != "not specified"
                ]

                if discussion_points:
                    for point in discussion_points:
                        st.write("•", point)
                else:
                    st.info("No discussion points identified.")

                # Display key decisions
                st.subheader("✅ Key Decisions")

                decisions = [
                    decision
                    for decision in meeting_data.get("decisions", [])
                    if isinstance(decision, str)
                    and decision.strip()
                    and decision.strip().lower() != "not specified"
                ]

                if decisions:
                    for decision in decisions:
                        st.write("•", decision)
                else:
                    st.info("No decisions identified in the transcript.")

                # Display action items
                st.subheader("📌 Action Items")

                action_items = meeting_data.get("action_items", [])

                # Keep only valid action-item objects
                valid_action_items = [
                    item
                    for item in action_items
                    if isinstance(item, dict)
                    and isinstance(item.get("task"), str)
                    and item["task"].strip()
                    and item["task"].strip().lower() != "not specified"
                ]

                if valid_action_items:
                    st.table(valid_action_items)
                else:
                    st.info("No confirmed action items identified.")

            except json.JSONDecodeError:
                logger.exception(
                    "Failed to parse the LLM response as JSON."
                )
                st.error(
                    "The AI returned an invalid response format. "
                    "Please try again."
                )

            except ValueError:
                logger.exception(
                    "The LLM response did not match the expected structure."
                )
                st.error(
                    "The AI returned an unexpected data structure. "
                    "Please try again."
                )

            except Exception:
                logger.exception(
                    "An error occurred during meeting analysis."
                )
                st.error(
                    "Something went wrong while analyzing the meeting. "
                    "Please try again."
                )
