
import streamlit as st
import json
import logging
import html

from services.llm_service import ask_llm


# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="MeetMind AI",
    page_icon="🧠",
    layout="wide",
)


# --------------------------------------------------
# 2. Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .mm-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0 22px 0;
        border-bottom: 1px solid #30343d;
        margin-bottom: 24px;
        overflow: visible;
    }

    .mm-brand-icon {
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: #253449;
        color: #a5c8ff;
        flex-shrink: 0;
    }

    .mm-brand-name {
        font-size: 1.45rem;
        font-weight: 700;
        color: #f4f6fa;
        line-height: 1.5;
        padding-top: 2px;
    }

    .mm-brand-subtitle {
        font-size: 0.85rem;
        color: #9ca6b5;
        margin-top: 2px;
    }

    .mm-card {
        border: 1px solid #30343d;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 18px;
    }

    .mm-section-heading {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.08rem;
        font-weight: 650;
        color: #f4f6fa;
        margin-bottom: 14px;
    }

    .mm-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .mm-icon-blue {
        color: #78a9ff;
    }

    .mm-icon-green {
        color: #5cc8a1;
    }

    .mm-summary {
        color: #d9dee8;
        line-height: 1.75;
        font-size: 0.96rem;
    }

    .mm-list-item {
        padding: 13px 0;
        border-bottom: 1px solid #30343d;
        color: #d9dee8;
        line-height: 1.6;
        font-size: 0.92rem;
        overflow-wrap: anywhere;
    }

    .mm-list-item:first-child {
        padding-top: 4px;
    }

    .mm-list-item:last-child {
        border-bottom: none;
        padding-bottom: 2px;
    }

    .mm-empty {
        color: #9ca6b5;
        padding: 8px 0;
        font-size: 0.9rem;
    }

    .mm-task {
        padding: 14px 0;
        border-bottom: 1px solid #30343d;
    }

    .mm-task:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }

    .mm-task-title {
        color: #f0f3f8;
        font-size: 0.94rem;
        font-weight: 550;
        line-height: 1.6;
        margin-bottom: 7px;
        overflow-wrap: anywhere;
    }

    .mm-task-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 18px;
        color: #aab4c3;
        font-size: 0.82rem;
    }

    .mm-task-meta span {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .mm-task-icon {
        color: #8da2bf;
        display: inline-flex;
        align-items: center;
        flex-shrink: 0;
    }

    .mm-count {
        margin-left: auto;
        color: #b8d2ff;
        background: #253449;
        padding: 4px 9px;
        border-radius: 20px;
        font-size: 0.76rem;
        font-weight: 600;
        white-space: nowrap;
    }

    @media (max-width: 640px) {
        .mm-brand-name {
            font-size: 1.2rem;
        }

        .mm-card {
            padding: 14px;
        }

        .mm-section-heading {
            font-size: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 4. Application Header
# --------------------------------------------------


st.markdown(
    """
    <div class="mm-header">
        <div class="mm-brand-icon">
            <svg width="27" height="27" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor"
                 stroke-width="1.7" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M12 18V5"/>
                <path d="M9 8a3 3 0 1 1 6 0"/>
                <path d="M8 14a4 4 0 0 1-1-7.9"/>
                <path d="M16 14a4 4 0 0 0 1-7.9"/>
                <path d="M8 14a4 4 0 0 0 4 4"/>
                <path d="M16 14a4 4 0 0 1-4 4"/>
                <path d="M5 11a3 3 0 0 0 3 3"/>
                <path d="M19 11a3 3 0 0 1-3 3"/>
            </svg>            
        </div>
        <div>
            <div class="mm-brand-name">MeetMind AI</div>
            <div class="mm-brand-subtitle">
                Meeting intelligence workspace
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 5. Transcript Input
# --------------------------------------------------

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


# --------------------------------------------------
# 6. Transcript Cleaning
# --------------------------------------------------

def clean_transcript(text):
    """Remove unnecessary whitespace from the transcript."""
    return " ".join(text.split())


# --------------------------------------------------
# 7. Prompt Engineering
# --------------------------------------------------

def create_prompt(cleaned_text):
    """Create the prompt used to analyze the meeting."""

    return f"""
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
- Do not classify a task as a confirmed decision or action item merely because someone says the team "should" do it. Require clear evidence of an actual agreement, commitment, or assigned task. A statement that explicitly assigns a task or deadline can count as a commitment even if no one else responds.

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
{cleaned_text}
"""


# --------------------------------------------------
# 8. Reusable Rendering Functions
# --------------------------------------------------

def render_items(items):
    """Render text items with bottom borders and no bullets."""

    if not items:
        return (
            '<div class="mm-empty">'
            'Nothing identified in this section.'
            '</div>'
        )

    return "".join(
        f'<div class="mm-list-item">{html.escape(item)}</div>'
        for item in items
    )


def clean_text_items(items):
    """Keep valid text items and remove placeholder values."""

    return [
        item.strip()
        for item in items
        if isinstance(item, str)
        and item.strip()
        and item.strip().lower() != "not specified"
    ]


# --------------------------------------------------
# 9. Analyze Meeting
# --------------------------------------------------

if st.button(
    "🚀 Analyze Meeting",
    type="secondary",
    use_container_width=True
):

    if not transcript.strip():
        st.warning("Please enter a meeting transcript before analyzing.")

    else:
        cleaned_transcript = clean_transcript(transcript)
        prompt = create_prompt(cleaned_transcript)

        with st.spinner("Analyzing the meeting..."):

            try:
                # Call the LLM
                result = ask_llm(prompt)

                # Parse JSON response
                meeting_data = json.loads(result)

                # Validate the main response
                if not isinstance(meeting_data, dict):
                    raise ValueError(
                        "The response must be a JSON object."
                    )

                # Validate list fields
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

                logger.info(
                    "Meeting analysis completed successfully."
                )

                # ------------------------------------------
                # Meeting Summary
                # ------------------------------------------

                summary = meeting_data.get("summary")

                if not isinstance(summary, str) or not summary.strip():
                    summary = "No summary available."

                st.markdown(
                    f"""
                    <div class="mm-card">
                        <div class="mm-section-heading">
                            <span class="mm-icon">
                                <svg width="21" height="21"
                                     viewBox="0 0 24 24"
                                     fill="none" stroke="currentColor"
                                     stroke-width="1.8"
                                     stroke-linecap="round"
                                     stroke-linejoin="round">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16
                                             a2 2 0 0 0 2 2h12
                                             a2 2 0 0 0 2-2V8z"/>
                                    <path d="M14 2v6h6"/>
                                    <path d="M8 13h8"/>
                                    <path d="M8 17h8"/>
                                </svg>
                            </span>
                            Meeting Summary
                        </div>
                        <div class="mm-summary">
                            {html.escape(summary)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ------------------------------------------
                # Discussion Points and Key Decisions
                # ------------------------------------------

                discussion_points = clean_text_items(
                    meeting_data.get("discussion_points", [])
                )

                decisions = clean_text_items(
                    meeting_data.get("decisions", [])
                )

                col1, col2 = st.columns(2, gap="medium")

                with col1:
                    st.markdown(
                        f"""
                        <div class="mm-card">
                            <div class="mm-section-heading">
                                <span class="mm-icon mm-icon-blue">
                                    <svg width="22" height="22"
                                         viewBox="0 0 24 24"
                                         fill="none" stroke="currentColor"
                                         stroke-width="1.8"
                                         stroke-linecap="round"
                                         stroke-linejoin="round">
                                        <path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8
                                                 8.5 8.5 0 0 1-7.6 4.7
                                                 8.4 8.4 0 0 1-3.8-.9L3 21
                                                 l1.9-5.7a8.4 8.4 0 0 1-.9-3.8
                                                 8.5 8.5 0 0 1 4.7-7.6
                                                 8.4 8.4 0 0 1 3.8-.9h.5
                                                 a8.5 8.5 0 0 1 8 8z"/>
                                        <path d="M8 11h.01"/>
                                        <path d="M12 11h.01"/>
                                        <path d="M16 11h.01"/>
                                    </svg>
                                </span>
                                Discussion Points
                            </div>
                            {render_items(discussion_points)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="mm-card">
                            <div class="mm-section-heading">
                                <span class="mm-icon mm-icon-green">
                                    <svg width="22" height="22"
                                         viewBox="0 0 24 24"
                                         fill="none" stroke="currentColor"
                                         stroke-width="1.8"
                                         stroke-linecap="round"
                                         stroke-linejoin="round">
                                        <circle cx="12" cy="12" r="10"/>
                                        <path d="m8 12 2.5 2.5L16 9"/>
                                    </svg>
                                </span>
                                Key Decisions
                            </div>
                            {render_items(decisions)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # ------------------------------------------
                # Action Items
                # ------------------------------------------
                action_items = [
                    item
                    for item in meeting_data.get("action_items", [])
                    if isinstance(item, dict)
                    and isinstance(item.get("task"), str)
                    and item["task"].strip()
                    and item["task"].strip().lower() != "not specified"
                ]

                action_rows = ""

                for item in action_items:
                    task = html.escape(str(item.get("task", "")).strip())
                    person = html.escape(str(item.get("person") or "Not specified"))
                    deadline = html.escape(str(item.get("deadline") or "Not specified"))

                    action_rows += f"""
                    <div class="mm-task">
                        <div class="mm-task-title">{task}</div>
                        <div class="mm-task-meta">
                            <span>
                                <span class="mm-task-icon">
                                    <svg width="16" height="16" viewBox="0 0 24 24"
                                        fill="none" stroke="currentColor"
                                        stroke-width="1.8" stroke-linecap="round"
                                        stroke-linejoin="round">
                                        <circle cx="12" cy="8" r="4"/>
                                        <path d="M5 21v-2a7 7 0 0 1 14 0v2"/>
                                    </svg>
                                </span>
                                {person}
                            </span>
                            <span>
                                <span class="mm-task-icon">
                                    <svg width="16" height="16" viewBox="0 0 24 24"
                                        fill="none" stroke="currentColor"
                                        stroke-width="1.8" stroke-linecap="round"
                                        stroke-linejoin="round">
                                        <rect x="3" y="4" width="18" height="17" rx="2"/>
                                        <path d="M16 2v4M8 2v4M3 10h18"/>
                                    </svg>
                                </span>
                                {deadline}
                            </span>
                        </div>
                    </div>
                    """


                st.markdown(
                    f"""
                    <div class="mm-card">
                        <div class="mm-section-heading">
                            <span class="mm-icon">
                                <svg width="22" height="22" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor"
                                    stroke-width="1.8" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <path d="M9 6h11"/>
                                    <path d="M9 12h11"/>
                                    <path d="M9 18h11"/>
                                    <path d="m3 6 1 1 2-2"/>
                                    <path d="m3 12 1 1 2-2"/>
                                    <path d="m3 18 1 1 2-2"/>
                                </svg>
                            </span>
                            Action Items
                            <span class="mm-count">{len(action_items)} tasks</span>
                        </div>
                        {
                            action_rows
                            if action_rows
                            else '<div class="mm-empty">No confirmed action items identified.</div>'
                        }
                    </div>
                    """,
                    unsafe_allow_html=True
                )


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

            except Exception as e:
                logger.exception(
                    "An error occurred during meeting analysis."
                )
                st.error(
                    "Something went wrong while analyzing the meeting. "
                    "Please try again."
                )
