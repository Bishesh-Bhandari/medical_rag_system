from .retriever import get_retreiver
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda


FEW_SHOT_EXAMPLES = """
Example 1
Question: What are common symptoms of diabetes?
Retrieved context: Diabetes may cause increased thirst, frequent urination, fatigue, blurred vision, and unexplained weight loss.
Answer: Common symptoms of diabetes include increased thirst, frequent urination, tiredness, blurred vision, and unexplained weight loss. These symptoms should be discussed with a qualified healthcare professional, especially if they are new, worsening, or persistent.

Example 2
Question: Can lifestyle changes help manage type 2 diabetes?
Retrieved context: Lifestyle management for type 2 diabetes includes healthy eating, regular physical activity, weight management, and monitoring blood glucose.
Answer: Yes. Lifestyle changes can help manage type 2 diabetes. Helpful steps often include balanced meals, regular physical activity, weight management, and blood glucose monitoring. The exact plan should be personalized with a clinician.
"""


PROMPT_TEMPLATE = """
You are MedQuery AI, a medical information assistant for a student RAG project.
If a user message seems to just a greetings or a simple question that doesn't require the 
retrieved context, answer it directly without referencing the retrieved context.

For example, if the user says "Hi" or "Hello", 
you can respond with a simplet greeting like "Hello! How can I assist you today?" without referencing
the retrieved context. Or if the user says "Thanks" or "Thank you", you can respond with "You're welcome! 
If you have any more questions, feel free to ask." without referencing the retrieved context.

Rules:
- Answer only using the retrieved context when possible not with your own knowledge. If the retrieved context does not contain the answer, say that the information is not available in the retrieved context.
- If the context is not enough, say that the available document context is limited.
- Do not diagnose the user.
- Do not prescribe medication or dosage.
- Encourage the user to consult a qualified healthcare professional for personal medical advice.
- Use clear, simple language.
- Keep the answer concise but helpful.

Few-shot examples:
{few_shot_examples}

Retrieved context:
{retrieved_context}

User question:
{input}

Final answer:
"""

llm = ChatOllama(model = 'llama3')

def get_msg_content(msg):
    return msg.content

contextualize_system_prompt = (
"""Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question which can be understood \
without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."""
)

contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_system_prompt),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
])


contextualize_chain = (
    contextualize_prompt
    | llm 
    | get_msg_content 
)

qa_system_prompt = PROMPT_TEMPLATE

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

qa_chain = (
    qa_prompt
    | llm
    | get_msg_content
)

# Define the overall chain the uses both the retrieved documents and the chat history to answer the question

db_retriever = get_retreiver()

def history_aware_qa(input):
    # Rephrase the question if needed
    if input.get('chat_history'):
        question = contextualize_chain.invoke(input)
    else:
        question = input['input']

    # Get context from the retriever
    context = db_retriever.invoke(question)
    # print(context)
    
    # Get the final answer
    return qa_chain.invoke({
        **input,
         "retrieved_context": context,
        "few_shot_examples": FEW_SHOT_EXAMPLES
    })


chat_history_for_chain = InMemoryChatMessageHistory()
qa_with_history = RunnableWithMessageHistory(
    RunnableLambda(history_aware_qa),
    lambda _: chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def chatbot_response(user_input):
    result = qa_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "123"}},
    )
    return f"{result}"
