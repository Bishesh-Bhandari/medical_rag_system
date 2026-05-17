# =============================================================================
# MedQuery AI — Streamlit Chatbot Frontend
# Phase 1: UI Skeleton (No backend / RAG integration yet)
#
# HOW TO RUN:
#   pip install streamlit
#   streamlit run app.py
#
# EXPECTED OUTPUT:
#   A clean, professional medical chatbot UI opens in your browser at
#   http://localhost:8501
#
# FUTURE INTEGRATION NOTE:
#   Search for the comment "# [BACKEND HOOK]" throughout this file.
#   Every such comment marks exactly where RAG pipeline code will plug in later.
# =============================================================================

import streamlit as st
import time
import random

# =============================================================================
# PAGE CONFIG
# Must be the very first Streamlit call. Sets browser tab title, icon, and
# the sidebar layout behaviour.
# =============================================================================
st.set_page_config(
    page_title="MedQuery AI",
    page_icon="🩺",
    layout="wide",                 # wide layout = more room for the chat area
    initial_sidebar_state="expanded",
)


# =============================================================================
# CUSTOM CSS — Professional medical AI look
# Streamlit renders markdown/HTML inside st.markdown, so we inject CSS here
# to override default Streamlit styles without touching any config file.
# =============================================================================
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* ── Google Fonts ─────────────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

        /* ── Root palette ─────────────────────────────────────────────────── */
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

        /* ── Global ───────────────────────────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: var(--font-body);
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }

        /* ── Hide Streamlit chrome we don't need ──────────────────────────── */
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Main container width cap ─────────────────────────────────────── */
        .block-container {
            max-width: 860px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* ── Title block ──────────────────────────────────────────────────── */
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

        /* ── Chat message bubbles ─────────────────────────────────────────── */
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

        /* ── Chat input bar ───────────────────────────────────────────────── */
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

        /* ── Sidebar ──────────────────────────────────────────────────────── */
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
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--green);
            margin-right: 6px;
            box-shadow: 0 0 6px var(--green);
        }

        /* ── Disclaimer banner ────────────────────────────────────────────── */
        .disclaimer {
            font-size: 0.75rem;
            color: var(--text-muted);
            border-left: 3px solid #f0883e;
            background: rgba(240,136,62,0.08);
            border-radius: 0 6px 6px 0;
            padding: 0.5rem 0.75rem;
            margin-bottom: 1.2rem;
        }

        /* ── Divider ──────────────────────────────────────────────────────── */
        hr { border-color: var(--border); margin: 1rem 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# SESSION STATE INITIALISATION
#
# st.session_state persists across Streamlit re-runs (which happen on every
# user interaction). Without it, every chat message would vanish on the next
# widget interaction.
#
# We initialise two keys:
#   messages  — the ordered list of chat turns [{role, content}, …]
#   thinking  — a bool flag so we can show a "thinking" animation
# =============================================================================
def init_session_state():
    if "messages" not in st.session_state:
        # Pre-load a system greeting so the chat doesn't open blank
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
# PLACEHOLDER RESPONSE GENERATOR
#
# This function currently returns a canned response.
#
# [BACKEND HOOK — PHASE 2]
# Replace the body of this function with:
#   1. Call the ingestion/retriever to get top-k chunks from FAISS
#   2. Build a grounded prompt: system + retrieved chunks + user query
#   3. Send to OpenAI / LangChain chain / ReAct agent
#   4. Return the final answer string (+ optionally source citations)
#
# Signature will stay the same so no UI code needs to change.
# =============================================================================
def get_bot_response(user_query: str) -> str:
    """
    Phase 1: returns a placeholder string.
    Phase 2: will call RAG pipeline and return a grounded answer.
    """
    # [BACKEND HOOK] ── replace everything below with actual RAG call ──────────
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
            "Your query has been received: _\"{}\"_\n\n"
            "Once the RAG pipeline is connected, you'll see a cited answer "
            "drawn from peer-reviewed medical documents."
        ).format(user_query[:120]),
        (
            "⚙️ **RAG pipeline pending.**\n\n"
            "This skeleton UI is ready to receive real answers. "
            "The retriever, FAISS vector store, LangChain chain, and "
            "OpenAI API will be wired in the next development phase."
        ),
    ]
    return random.choice(placeholder_responses)
    # [END BACKEND HOOK] ────────────────────────────────────────────────────────


# =============================================================================
# SIDEBAR
# =============================================================================
def render_sidebar():
    with st.sidebar:
        # Brand
        st.markdown("## 🩺 MedQuery AI")
        st.markdown(
            '<span class="status-dot"></span>'
            '<span style="font-size:0.8rem;color:#8b949e;">UI skeleton active</span>',
            unsafe_allow_html=True,
        )
        st.markdown("<hr>", unsafe_allow_html=True)

        # ── About ──────────────────────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-section-title">About</div>', unsafe_allow_html=True
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

        # ── Tech stack ─────────────────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-section-title">Tech Stack</div>',
            unsafe_allow_html=True,
        )
        chips = [
            "Streamlit", "LangChain", "FAISS",
            "OpenAI API", "PyMuPDF", "sentence-transformers",
        ]
        html_chips = "".join(
            f'<span class="sidebar-chip">{c}</span>' for c in chips
        )
        st.markdown(html_chips, unsafe_allow_html=True)

        # ── Development phases ─────────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-section-title">Development Phases</div>',
            unsafe_allow_html=True,
        )
        phases = {
            "✅ Phase 1": "Streamlit UI skeleton",
            "⬜ Phase 2": "PDF ingestion pipeline",
            "⬜ Phase 3": "FAISS vector store",
            "⬜ Phase 4": "RAG chain + LLM",
            "⬜ Phase 5": "ReAct agent + memory",
            "⬜ Phase 6": "Evaluation & deployment",
        }
        for label, desc in phases.items():
            color = "#3fb950" if label.startswith("✅") else "#8b949e"
            st.markdown(
                f'<div style="font-size:0.8rem;margin:4px 0;">'
                f'<span style="color:{color};font-weight:600;">{label}</span>'
                f' — <span style="color:#8b949e;">{desc}</span></div>',
                unsafe_allow_html=True,
            )

        # ── Future features ────────────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-section-title">Planned Features</div>',
            unsafe_allow_html=True,
        )
        features = [
            "📚 Multi-PDF ingestion",
            "🔎 Semantic retrieval (FAISS)",
            "🤖 ReAct agent reasoning",
            "🧠 Conversation memory",
            "📌 Source citations in answers",
            "📊 Confidence scoring",
        ]
        for f in features:
            st.markdown(
                f'<div style="font-size:0.8rem;color:#8b949e;margin:3px 0;">{f}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Clear chat ─────────────────────────────────────────────────────
        if st.button("🗑️ Clear conversation", use_container_width=True):
            # Reset messages to just the greeting
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Conversation cleared. How can I help you today?"
                    ),
                }
            ]
            st.rerun()

        st.markdown(
            '<div style="font-size:0.7rem;color:#484f58;margin-top:1rem;text-align:center;">'
            "MedQuery AI · BE Major Project · Phase 1"
            "</div>",
            unsafe_allow_html=True,
        )


# =============================================================================
# MAIN CHAT AREA
# =============================================================================
def render_chat_header():
    st.markdown(
        '<div class="mq-title">🩺 MedQuery AI '
        '<span class="mq-badge">BETA</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="mq-subtitle">'
        "Evidence-based medical assistant powered by Retrieval-Augmented Generation (RAG). "
        "Ask about symptoms, medications, diagnoses, or medical literature."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="disclaimer">'
        "⚠️ <strong>Medical Disclaimer:</strong> MedQuery AI is a research prototype. "
        "It does <em>not</em> provide professional medical advice, diagnosis, or treatment. "
        "Always consult a qualified healthcare provider."
        "</div>",
        unsafe_allow_html=True,
    )


def render_chat_history():
    """
    Iterate over st.session_state.messages and render each turn.

    st.chat_message("user")      → right-aligned bubble with user avatar
    st.chat_message("assistant") → left-aligned bubble with bot avatar

    [BACKEND HOOK — PHASE 5]
    When conversation memory is added (e.g. ConversationBufferMemory from
    LangChain), the messages list here can be synced with the LangChain
    memory object so the LLM has full context.
    """
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def handle_user_input():
    """
    Captures the chat input, appends to history, generates a response,
    and appends that too. Streamlit re-runs the script top-to-bottom on
    every interaction — session_state ensures nothing is lost between runs.

    [BACKEND HOOK — PHASE 2/3/4]
    Replace `get_bot_response(user_input)` with your RAG chain call:
        response = rag_chain.invoke({"query": user_input, "history": ...})
    The rest of the UI code stays exactly the same.
    """
    user_input = st.chat_input(
        "Ask a medical question… e.g. 'What are the symptoms of Type 2 diabetes?'"
    )

    if user_input:
        # ── 1. Append user message to history ─────────────────────────────
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        # ── 2. Display user message immediately ───────────────────────────
        with st.chat_message("user"):
            st.markdown(user_input)

        # ── 3. Show typing indicator while "thinking" ──────────────────────
        with st.chat_message("assistant"):
            with st.spinner("Searching medical knowledge base…"):
                # Simulate retrieval latency (remove once backend is live)
                time.sleep(1.2)

                # [BACKEND HOOK] ── swap this line with real RAG call ──────
                bot_reply = get_bot_response(user_input)
                # [END BACKEND HOOK] ────────────────────────────────────────

            st.markdown(bot_reply)

        # ── 4. Append assistant reply to history ───────────────────────────
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )


# =============================================================================
# ENTRY POINT
# =============================================================================
def main():
    inject_custom_css()
    init_session_state()
    render_sidebar()
    render_chat_header()
    render_chat_history()
    handle_user_input()


if __name__ == "__main__":
    main()