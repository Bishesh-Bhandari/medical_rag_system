# =============================================================================
# MedQuery AI — Streamlit Chatbot Frontend
# =============================================================================

import streamlit as st
import time
import random


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="MedQuery AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# CUSTOM CSS
# =============================================================================
def inject_custom_css():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

        :root {
            --bg-primary:   #0d1117;
            --bg-surface:   #161b22;
            --bg-card:      #1c2330;
            --border:       #30363d;
            --accent:       #2f81f7;
            --accent-dim:   #1a4a8f;
            --green:        #3fb950;
            --text-primary: #e6edf3;
            --text-muted:   #8b949e;
            --user-bubble:  #1f3a5c;
            --bot-bubble:   #1c2330;
            --font-body:    'DM Sans', sans-serif;
            --font-mono:    'DM Mono', monospace;
        }

        html, body, [class*="css"] {
            font-family: var(--font-body);
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }

        /* FIXED */
        #MainMenu, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 860px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .mq-title {
            font-size: 2.1rem;
            font-weight: 600;
            letter-spacing: -0.5px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.15rem;
        }

        .mq-subtitle {
            font-size: 0.92rem;
            color: var(--text-muted);
            margin-bottom: 1.8rem;
            line-height: 1.5;
        }

        .mq-badge {
            font-family: var(--font-mono);
            font-size: 0.7rem;
            background: var(--accent-dim);
            color: var(--accent);
            border: 1px solid var(--accent);
            border-radius: 4px;
            padding: 2px 8px;
            letter-spacing: 0.5px;
            vertical-align: middle;
        }

        [data-testid="stChatMessage"] {
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.6rem;
            border: 1px solid var(--border);
            background: var(--bot-bubble);
        }

        [data-testid="stChatMessage"][data-role="user"] {
            background: var(--user-bubble);
            border-color: var(--accent-dim);
        }

        [data-testid="stChatInput"] textarea {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            color: var(--text-primary) !important;
            font-family: var(--font-body) !important;
            font-size: 0.95rem !important;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px rgba(47,129,247,0.2) !important;
        }

        [data-testid="stSidebar"] {
            background-color: var(--bg-surface);
            border-right: 1px solid var(--border);
        }

        .sidebar-section-title {
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin: 1.2rem 0 0.5rem;
        }

        .sidebar-chip {
            display: inline-block;
            font-size: 0.78rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 3px 10px;
            margin: 3px 3px 3px 0;
            color: var(--text-muted);
        }

        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
            margin-right: 6px;
            box-shadow: 0 0 6px var(--green);
        }

        .disclaimer {
            font-size: 0.75rem;
            color: var(--text-muted);
            border-left: 3px solid #f0883e;
            background: rgba(240,136,62,0.08);
            border-radius: 0 6px 6px 0;
            padding: 0.5rem 0.75rem;
            margin-bottom: 1.2rem;
        }

        hr {
            border-color: var(--border);
            margin: 1rem 0;
        }

        /* SIDEBAR TOGGLE BUTTON */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999999 !important;

            background-color: #1c2330 !important;
            border: 1px solid #30363d !important;
            border-radius: 10px !important;

            padding: 6px !important;
            margin: 10px !important;

            color: white !important;
        }

        [data-testid="collapsedControl"] svg {
            fill: white !important;
            color: white !important;
        }

        [data-testid="collapsedControl"]:hover {
            background-color: #2f81f7 !important;
            border-color: #2f81f7 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# SESSION STATE
# =============================================================================
def init_session_state():

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I'm **MedQuery AI**, your evidence-based medical assistant. "
                    "Ask me anything about symptoms, medications, or medical conditions and I'll "
                    "retrieve relevant information from trusted medical literature.\n\n"
                    "_Note: I am not a substitute for professional medical advice._"
                ),
            }
        ]

    if "thinking" not in st.session_state:
        st.session_state.thinking = False


# =============================================================================
# TEMP BOT RESPONSE
# =============================================================================
def get_bot_response(user_query: str) -> str:

    placeholder_responses = [

        (
            "🔍 **Retrieval pipeline not connected yet.**\n\n"
            "In the final system, I would:\n"
            "1. Encode your query into a vector embedding\n"
            "2. Search the FAISS index for the most relevant medical document chunks\n"
            "3. Feed those chunks + your question into a grounded LLM prompt\n"
            "4. Return an evidence-based answer with source citations\n\n"
            "_Backend integration coming in Phase 2._"
        ),

        (
            "📄 **Placeholder response — backend not yet implemented.**\n\n"
            f"Your query has been received: _\"{user_query[:120]}\"_\n\n"
            "Once the RAG pipeline is connected, you'll see a cited answer "
            "drawn from peer-reviewed medical documents."
        ),

        (
            "⚙️ **RAG pipeline pending.**\n\n"
            "This skeleton UI is ready to receive real answers. "
            "The retriever, FAISS vector store, LangChain chain, and "
            "OpenAI API will be wired in the next development phase."
        ),
    ]

    return random.choice(placeholder_responses)


# =============================================================================
# SIDEBAR
# =============================================================================
def render_sidebar():

    with st.sidebar:

        st.markdown("## 🩺 MedQuery AI")

        st.markdown(
            '<span class="status-dot"></span>'
            '<span style="font-size:0.8rem;color:#8b949e;">UI skeleton active</span>',
            unsafe_allow_html=True,
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-section-title">About</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="font-size:0.83rem;color:#8b949e;line-height:1.6;">
            MedQuery AI is a Retrieval-Augmented Generation system built as a
            BE major project. It grounds every answer in real medical literature,
            reducing hallucinations and improving reliability.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section-title">Tech Stack</div>',
            unsafe_allow_html=True,
        )

        chips = [
            "Streamlit",
            "LangChain",
            "FAISS",
            "OpenAI API",
            "PyPDF",
            "sentence-transformers",
        ]

        html_chips = "".join(
            f'<span class="sidebar-chip">{chip}</span>' for chip in chips
        )

        st.markdown(html_chips, unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-section-title">Development Phases</div>',
            unsafe_allow_html=True,
        )

        phases = {
            "✅ Phase 1": "Streamlit UI skeleton",
            "✅ Phase 2": "PDF loading + chunking",
            "✅ Phase 3": "FAISS vector store",
            "⬜ Phase 4": "Retriever integration",
            "⬜ Phase 5": "RAG + LLM",
            "⬜ Phase 6": "Deployment",
        }

        for label, desc in phases.items():

            color = "#3fb950" if label.startswith("✅") else "#8b949e"

            st.markdown(
                f"""
                <div style="font-size:0.8rem;margin:4px 0;">
                    <span style="color:{color};font-weight:600;">{label}</span>
                    — <span style="color:#8b949e;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<hr>", unsafe_allow_html=True)

        if st.button("🗑️ Clear conversation", use_container_width=True):

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared. How can I help you today?",
                }
            ]

            st.rerun()


# =============================================================================
# HEADER
# =============================================================================
def render_chat_header():

    st.markdown(
        """
        <div class="mq-title">
            🩺 MedQuery AI <span class="mq-badge">BETA</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="mq-subtitle">
            Evidence-based medical assistant powered by Retrieval-Augmented Generation (RAG).
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="disclaimer">
            ⚠️ <strong>Medical Disclaimer:</strong>
            This is a research prototype.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# CHAT HISTORY
# =============================================================================
def render_chat_history():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# =============================================================================
# USER INPUT
# =============================================================================
def handle_user_input():

    user_input = st.chat_input(
        "Ask a medical question..."
    )

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("user"):

            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner("Searching medical knowledge base..."):

                time.sleep(1.2)

                bot_reply = get_bot_response(user_input)

            st.markdown(bot_reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )


# =============================================================================
# MAIN
# =============================================================================
def main():

    inject_custom_css()

    init_session_state()

    render_sidebar()

    render_chat_header()

    render_chat_history()

    handle_user_input()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":

    main()