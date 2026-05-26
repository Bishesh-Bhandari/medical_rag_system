import streamlit as st
from rag.rag_chain import chatbot_response


st.set_page_config(
    page_title="MedQuery AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am MedQuery AI. Ask me a medical question and I will "
                    "answer using the available medical document context.\n\n"
                    "**Note:** This is not a substitute for professional medical advice."
                ),
            }
        ]


def render_sidebar():
    with st.sidebar:
        st.title("🩺 MedQuery AI")
        st.caption("Medical RAG Assistant")

        st.divider()

        st.markdown("### About")
        st.write(
            "MedQuery AI is a Retrieval-Augmented Generation system that answers "
            "medical questions using retrieved document context."
        )

        st.markdown("### Tech Stack")
        st.write("Streamlit · LangChain · FAISS · Ollama · HuggingFace Embeddings")

        st.divider()

        if st.button("🗑️ Clear conversation", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared. How can I help you today?",
                }
            ]
            st.rerun()


def render_header():
    st.title("🩺 MedQuery AI")
    st.caption("Evidence-based medical assistant using RAG")

    st.warning(
        "Medical Disclaimer: This is a student research prototype. "
        "Always consult a qualified healthcare professional for personal medical advice."
    )


def render_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    user_input = st.chat_input("Ask a medical question...")

    if user_input:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching medical knowledge base..."):
                try:
                    response = chatbot_response(user_input)
                except Exception as e:
                    response = f"Something went wrong:\n\n`{e}`"

                st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )


def main():
    init_session_state()
    render_sidebar()
    render_header()
    render_chat_history()
    handle_user_input()


if __name__ == "__main__":
    main()