# =============================================================================
# MedQuery AI — Streamlit Chatbot Frontend (Redesigned)
# =============================================================================

import streamlit as st
import time
from rag.rag_chain import answer_medical_query   # ← backend import: DO NOT TOUCH


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
# CUSTOM CSS  (styling only — no layout HTML blocks)
# =============================================================================
def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Design tokens ────────────────────────────────────────────────── */
        :root {
            --bg-root:        #0b0c14;
            --bg-surface:     #12131f;
            --bg-card:        #1a1b2e;
            --bg-hover:       #1f2040;
            --border:         #2a2b45;
            --border-accent:  #4a3f7a;
            --accent:         #7c6af7;
            --accent-dim:     #2e2560;
            --accent-glow:    rgba(124,106,247,0.18);
            --green:          #4ade80;
            --orange:         #fb923c;
            --text-primary:   #e8e6f0;
            --text-secondary: #9d9bb8;
            --text-muted:     #5e5c7a;
            --user-bubble:    #1e1b3a;
            --bot-bubble:     #14152a;
            --font-body:      'Sora', sans-serif;
            --font-mono:      'JetBrains Mono', monospace;
            --radius-lg:      14px;
            --radius-md:      10px;
            --radius-sm:      6px;
            --shadow-card:    0 4px 24px rgba(0,0,0,0.45);
            --shadow-glow:    0 0 18px rgba(124,106,247,0.25);
        }

        /* ── Base reset ───────────────────────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: var(--font-body) !important;
            background-color: var(--bg-root) !important;
            color: var(--text-primary) !important;
        }

        #MainMenu, footer, header { visibility: hidden; }

        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 100% !important;
        }

        /* ── Left sidebar ─────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: var(--bg-surface) !important;
            border-right: 1px solid var(--border) !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 1.5rem 1.1rem;
        }

        /* ── Chat messages ────────────────────────────────────────────────── */
        [data-testid="stChatMessage"] {
            border-radius: var(--radius-lg) !important;
            padding: 0.85rem 1.1rem !important;
            margin-bottom: 0.7rem !important;
            border: 1px solid var(--border) !important;
            background: var(--bot-bubble) !important;
            box-shadow: var(--shadow-card) !important;
            font-size: 0.93rem !important;
            line-height: 1.7 !important;
        }

        [data-testid="stChatMessage"][data-role="user"] {
            background: var(--user-bubble) !important;
            border-color: var(--border-accent) !important;
        }

        /* ── Chat input ───────────────────────────────────────────────────── */
        [data-testid="stChatInput"] {
            border-top: 1px solid var(--border) !important;
            padding-top: 0.75rem !important;
        }

        [data-testid="stChatInput"] textarea {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-body) !important;
            font-size: 0.93rem !important;
            caret-color: var(--accent) !important;
            transition: border-color 0.2s, box-shadow 0.2s !important;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
            outline: none !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: var(--text-muted) !important;
        }

        /* ── Buttons ──────────────────────────────────────────────────────── */
        .stButton > button {
            background: var(--bg-card) !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            font-family: var(--font-body) !important;
            font-size: 0.83rem !important;
            font-weight: 500 !important;
            transition: all 0.18s !important;
        }

        .stButton > button:hover {
            background: var(--bg-hover) !important;
            border-color: var(--accent) !important;
            color: var(--accent) !important;
            box-shadow: var(--shadow-glow) !important;
        }

        /* ── Sidebar toggle ───────────────────────────────────────────────── */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999999 !important;
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 6px !important;
            margin: 10px !important;
            color: white !important;
        }

        [data-testid="collapsedControl"] svg { fill: white !important; }
        [data-testid="collapsedControl"]:hover {
            background-color: var(--accent) !important;
            border-color: var(--accent) !important;
        }

        /* ── Dividers ─────────────────────────────────────────────────────── */
        hr { border-color: var(--border) !important; margin: 0.85rem 0 !important; }

        /* ── Scrollbar ────────────────────────────────────────────────────── */
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: var(--bg-root); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent-dim); }

        /* ── Right column (search history panel) ─────────────────────────── */
        .search-history-header {
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.8rem;
        }

        .search-item {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.45rem;
            font-size: 0.78rem;
            color: var(--text-secondary);
            line-height: 1.4;
            cursor: default;
            transition: border-color 0.15s, background 0.15s;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .search-item:hover {
            border-color: var(--border-accent);
            background: var(--bg-hover);
            color: var(--text-primary);
        }

        .search-item-index {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            color: var(--text-muted);
            margin-right: 5px;
        }

        .search-empty {
            font-size: 0.78rem;
            color: var(--text-muted);
            font-style: italic;
            text-align: center;
            padding: 1.5rem 0;
        }

        /* ── Header elements ──────────────────────────────────────────────── */
        .mq-wordmark {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.3px;
        }

        .mq-badge {
            font-family: var(--font-mono);
            font-size: 0.62rem;
            background: var(--accent-dim);
            color: var(--accent);
            border: 1px solid var(--accent);
            border-radius: 4px;
            padding: 1px 7px;
            letter-spacing: 0.8px;
            vertical-align: middle;
            margin-left: 6px;
        }

        .mq-subtitle {
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-top: 0.1rem;
            margin-bottom: 1.1rem;
        }

        .disclaimer-bar {
            font-size: 0.74rem;
            color: var(--orange);
            border-left: 3px solid var(--orange);
            background: rgba(251,146,60,0.07);
            border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
            padding: 0.45rem 0.75rem;
            margin-bottom: 1rem;
        }

        /* ── Sidebar: section label ───────────────────────────────────────── */
        .sidebar-label {
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin: 1.1rem 0 0.45rem;
        }

        .sidebar-chip {
            display: inline-block;
            font-size: 0.72rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2px 10px;
            margin: 3px 2px;
            color: var(--text-secondary);
        }

        .status-dot {
            display: inline-block;
            width: 7px; height: 7px;
            border-radius: 50%;
            background: var(--green);
            margin-right: 5px;
            box-shadow: 0 0 6px var(--green);
        }

        /* ── Column separator ─────────────────────────────────────────────── */
        .col-separator {
            border-left: 1px solid var(--border);
            height: 100%;
            min-height: 400px;
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


# =============================================================================
# SIDEBAR  (left panel — tech stack, phases, clear button)
# =============================================================================
def render_sidebar():
    with st.sidebar:

        st.markdown(
            '<div class="mq-wordmark">🩺 MedQuery AI</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="status-dot"></span>'
            '<span style="font-size:0.78rem;color:#5e5c7a;">System online</span>',
            unsafe_allow_html=True,
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        # About
        st.markdown('<div class="sidebar-label">About</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:0.8rem;color:#9d9bb8;line-height:1.65;">'
            "MedQuery AI is a Retrieval-Augmented Generation system built as a "
            "BE major project. It grounds every answer in real medical literature, "
            "reducing hallucinations and improving reliability."
            "</div>",
            unsafe_allow_html=True,
        )

        # Tech stack
        st.markdown('<div class="sidebar-label">Tech Stack</div>', unsafe_allow_html=True)
        chips = ["Streamlit", "LangChain", "FAISS", "OpenAI API", "PyPDF", "sentence-transformers"]
        st.markdown(
            "".join(f'<span class="sidebar-chip">{c}</span>' for c in chips),
            unsafe_allow_html=True,
        )

        # Phases
        st.markdown('<div class="sidebar-label">Development Phases</div>', unsafe_allow_html=True)
        phases = {
            "✅ Phase 1": "Streamlit UI skeleton",
            "✅ Phase 2": "PDF loading + chunking",
            "✅ Phase 3": "FAISS vector store",
            "⬜ Phase 4": "Retriever integration",
            "⬜ Phase 5": "RAG + LLM",
            "⬜ Phase 6": "Deployment",
        }
        for label, desc in phases.items():
            color = "#4ade80" if label.startswith("✅") else "#5e5c7a"
            st.markdown(
                f'<div style="font-size:0.78rem;margin:5px 0;">'
                f'<span style="color:{color};font-weight:600;">{label}</span>'
                f' <span style="color:#5e5c7a;">— {desc}</span></div>',
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
# HEADER  (above chat column)
# =============================================================================
def render_chat_header():
    st.markdown(
        '<span style="font-size:1.55rem;font-weight:700;letter-spacing:-0.4px;">'
        '🩺 MedQuery AI'
        '</span>'
        '<span class="mq-badge">BETA</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="mq-subtitle">'
        "Evidence-based medical assistant · Retrieval-Augmented Generation"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="disclaimer-bar">'
        "⚠️ <strong>Medical Disclaimer:</strong> "
        "This is a research prototype. Always consult a qualified healthcare professional."
        "</div>",
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
# RIGHT PANEL — previous user searches derived from session state
# =============================================================================
def render_search_history_panel():
    st.markdown(
        '<div class="search-history-header">🔎 Previous Searches</div>',
        unsafe_allow_html=True,
    )

    # Extract only user messages (searches), most recent first
    user_queries = [
        m["content"]
        for m in st.session_state.messages
        if m["role"] == "user"
    ]

    if not user_queries:
        st.markdown(
            '<div class="search-empty">No searches yet.<br>Ask a question to get started.</div>',
            unsafe_allow_html=True,
        )
        return

    for i, q in enumerate(reversed(user_queries), 1):
        preview = q if len(q) <= 72 else q[:69] + "…"
        st.markdown(
            f'<div class="search-item">'
            f'<span class="search-item-index">#{i}</span>{preview}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:0.7rem;color:#5e5c7a;text-align:center;">'
        f'{len(user_queries)} search{"es" if len(user_queries) != 1 else ""} this session'
        f'</div>',
        unsafe_allow_html=True,
    )


# =============================================================================
# USER INPUT + BACKEND CALL  ← backend call preserved exactly
# =============================================================================
def handle_user_input():
    user_input = st.chat_input("Ask a medical question…")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching medical knowledge base…"):
                time.sleep(1.2)

                # ── BACKEND CALL — DO NOT MODIFY ──────────────────────────
                docs = answer_medical_query(user_input)
                # ─────────────────────────────────────────────────────────

                st.markdown(docs)

        st.session_state.messages.append({"role": "assistant", "content": docs})

        # Rerun so the right panel refreshes with the new query immediately
        st.rerun()


# =============================================================================
# MAIN  — three-column layout: sidebar (built-in) | chat | search history
# =============================================================================
def main():
    inject_custom_css()
    init_session_state()
    render_sidebar()

    # Two columns inside the main area:
    # col_chat  — wide center column for conversation
    # col_hist  — narrow right column for previous searches
    col_chat, col_hist = st.columns([3, 1], gap="large")

    with col_chat:
        render_chat_header()
        render_chat_history()
        handle_user_input()

    with col_hist:
        # Push the panel down to align with chat content
        st.markdown("<div style='height:5.5rem'></div>", unsafe_allow_html=True)
        render_search_history_panel()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
