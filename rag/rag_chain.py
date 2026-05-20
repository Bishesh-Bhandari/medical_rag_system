import os

from rag.retriever import get_similar_chunk


DEFAULT_MODEL = "gemini-1.5-flash"


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

Rules:
- Answer only using the retrieved context when possible.
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
{user_query}

Final answer:
"""


def build_medical_prompt(user_query: str, retrieved_context: str) -> str:
    """
    Builds the final prompt sent to the LLM.
    """
    return PROMPT_TEMPLATE.format(
        few_shot_examples=FEW_SHOT_EXAMPLES.strip(),
        retrieved_context=retrieved_context.strip(),
        user_query=user_query.strip(),
    )


def call_gemini_llm(prompt: str) -> str:
    """
    Calls Gemini using GEMINI_API_KEY from the environment.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "Gemini is not configured yet. Add your free Gemini API key as "
            "`GEMINI_API_KEY` in your environment, then restart the app."
        )

    try:
        import google.generativeai as genai
    except ImportError:
        return (
            "The Gemini package is not installed yet. Run "
            "`pip install google-generativeai` and restart the app."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(DEFAULT_MODEL)
    response = model.generate_content(prompt)

    return response.text


def answer_medical_query(user_query: str) -> str:
    """
    Retrieves relevant FAISS chunks, builds the prompt, and returns the LLM answer.
    """
    retrieved_context = get_similar_chunk(user_query)
    prompt = build_medical_prompt(user_query, retrieved_context)

    return call_gemini_llm(prompt)
